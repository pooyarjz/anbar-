from django.core.management.base import BaseCommand, CommandError
from inventory.models import Item, InventorySnapshot, CodeConsumption
import pandas as pd

class Command(BaseCommand):
    help = 'Import inventory data from the provided Excel file (anbar.xlsx format).'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, required=True, help='Path to Excel file')
        parser.add_argument('--only-base', action='store_true', help='Import only base columns (faster)')

    def handle(self, *args, **opts):
        path = opts['path']
        only_base = opts['only_base']
        self.stdout.write(self.style.WARNING(f'Reading: {path}'))
        raw = pd.read_excel(path, header=None)

        # Detect header row
        candidate_headers = None
        for i in range(min(5, len(raw))):
            row_vals = raw.iloc[i].astype(str).fillna("")
            if any(lbl in " ".join(row_vals.tolist()) for lbl in ["مواد اولیه", "ورودی کل", "موجودی انبار"]):
                candidate_headers = i
                break
        if candidate_headers is None:
            candidate_headers = 0

        df = raw.copy()
        df.columns = df.iloc[candidate_headers].astype(str).tolist()
        df = df.iloc[candidate_headers+1:].reset_index(drop=True)
        df.columns = [c.strip().replace("\n"," ").replace("\r"," ") for c in df.columns]

        base_cols = [c for c in ["مواد اولیه","ورودی کل نهاده","ورودی کل منهای افت","موجودی انبار"] if c in df.columns]
        if not base_cols:
            raise CommandError("Base columns not found in the Excel file.")

        inv = df[base_cols].copy()
        inv.columns = inv.columns.tolist()
        name_col = inv.columns[0]

        # Create/update items and snapshots
        created_items = 0
        created_snaps = 0
        for _, row in inv.iterrows():
            name = str(row[name_col]).strip()
            if not name or name.lower() == 'nan':
                continue
            item, _created = Item.objects.get_or_create(name=name)
            if _created:
                created_items += 1
            snap = InventorySnapshot(
                item=item,
                total_input=pd.to_numeric(row[base_cols[1]], errors='coerce') if len(base_cols)>1 else None,
                input_minus_waste=pd.to_numeric(row[base_cols[2]], errors='coerce') if len(base_cols)>2 else None,
                stock=pd.to_numeric(row[base_cols[3]], errors='coerce') if len(base_cols)>3 else None,
            )
            snap.save()
            created_snaps += 1

        self.stdout.write(self.style.SUCCESS(f'Items created: {created_items}, Snapshots: {created_snaps}'))

        if not only_base:
            code_cols = [c for c in df.columns if "کد مصرف شده" in c]
            if len(code_cols) > 0:
                first_row = df.iloc[0]
                code_map = {col: str(first_row[col]).strip() if str(first_row[col]).strip() not in ['', 'nan'] else col for col in code_cols}
                # Convert to long but in chunks to reduce memory
                step = 200
                total_written = 0
                for i in range(0, len(code_cols), step):
                    chunk_cols = code_cols[i:i+step]
                    melt_df = df[[name_col] + chunk_cols].copy()
                    melt_df = melt_df.rename(columns=code_map)
                    long_df = melt_df.melt(id_vars=[name_col], var_name="code", value_name="amount")
                    long_df["amount"] = pd.to_numeric(long_df["amount"], errors="coerce")
                    long_df = long_df.dropna(subset=["amount"])
                    long_df = long_df[long_df["amount"] != 0]
                    for _, r in long_df.iterrows():
                        it, _ = Item.objects.get_or_create(name=str(r[name_col]).strip())
                        CodeConsumption.objects.update_or_create(item=it, code=str(r["code"]), defaults={{"amount": r["amount"]}})
                        total_written += 1
                self.stdout.write(self.style.SUCCESS(f'Code consumption rows imported: {total_written}'))
            else:
                self.stdout.write(self.style.WARNING('No code-consumption columns detected; skipped.'))

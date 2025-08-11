# اپ حرفه‌ای مدیریت انبار (Django + DRF + Postgres)

## اجرای سریع با Docker
```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
# سپس وارد ادمین شوید:
# http://localhost:8000/admin/
```
## ایمپورت از اکسل شما
فایل `anbar.xlsx` را در مسیر پروژه قرار دهید و اجرا کنید:
```bash
docker compose cp anbar.xlsx web:/app/
docker compose exec web python manage.py import_anbar_excel --path /app/anbar.xlsx --only-base
```
(برای وارد کردن ستون‌های کد مصرف‌شده، `--only-base` را حذف کنید. در صورت حجیم‌بودن فایل، پردازش بخش‌بخش انجام می‌شود.)

## API ها
- `GET /api/items/?q=...` لیست اقلام
- `POST /api/transactions/` ثبت ورودی/خروجی
- `GET /api/stock/` موجودی لحظه‌ای (اسنپ‌شات آخر + تراکنش‌های بعد)

## توسعه
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## نقش‌ها و دسترسی‌ها
- **Django Admin** برای مدیریت کامل
- API ها نیاز به احراز هویت دارند (SessionAuth). در صورت نیاز JWT اضافه می‌شود.


## گزارش‌ها و نمودارها
- داشبورد وب در مسیر `/reports/` (Chart.js + Bootstrap)
- API گزارش‌ها:
  - GET /api/reports/consumption/?group_by=code|item|date|item_code&item_id=&from=&to=
  - GET /api/reports/movement/?item_id=&from=&to=
برای دسترسی، ابتدا لاگین کنید (SessionAuth).


## داشبورد و خرید
- داشبورد در `/dashboard/`: نمایش KPIها، موجودی تقریبی، اقلام زیر حداقل، تراکنش‌های اخیر
- ثبت خرید در `/purchase/new/`: با ثبت، خودکار تراکنش IN ایجاد می‌شود

نکته: برای حداقل موجودی، مقدار `min_stock` را برای هر کالا در ادمین تنظیم کنید.

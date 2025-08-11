
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Item, Transaction, InventorySnapshot, CodeConsumption, Supplier, PurchaseOrder, PurchaseItem
from .serializers import ItemSerializer, TransactionSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('name')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

class StockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        latest = {}
        for snap in InventorySnapshot.objects.order_by('item_id','-created_at').values('item_id','stock','created_at'):
            latest.setdefault(snap['item_id'], snap)
        rows = []
        for item in Item.objects.all():
            base = latest.get(item.id)
            base_stock = float(base['stock']) if base and base['stock'] is not None else 0.0
            since = base['created_at'] if base else None
            tx = Transaction.objects.filter(item=item)
            if since:
                tx = tx.filter(happened_at__gt=since)
            in_sum = tx.filter(ttype='IN').aggregate(s=Sum('qty'))['s'] or 0
            out_sum = tx.filter(ttype='OUT').aggregate(s=Sum('qty'))['s'] or 0
            rows.append({'item_id': item.id, 'item_name': item.name, 'stock': base_stock + float(in_sum) - float(out_sum)})
        return Response(rows)

class ImportStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        return Response({
            'items': Item.objects.count(),
            'snapshots': InventorySnapshot.objects.count(),
            'transactions': Transaction.objects.count()
        })

# Dashboard
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'inventory/dashboard.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # KPIs
        total_items = Item.objects.count()
        total_stock = 0.0
        # calculate current stock via StockView logic (simple approximate using latest snapshot + net tx)
        latest = {}
        for snap in InventorySnapshot.objects.order_by('item_id','-created_at').values('item_id','stock','created_at'):
            latest.setdefault(snap['item_id'], snap)
        low_stock = []
        for item in Item.objects.all():
            base = latest.get(item.id)
            base_stock = float(base['stock']) if base and base['stock'] is not None else 0.0
            since = base['created_at'] if base else None
            tx = Transaction.objects.filter(item=item)
            if since:
                tx = tx.filter(happened_at__gt=since)
            in_sum = tx.filter(ttype='IN').aggregate(s=Sum('qty'))['s'] or 0
            out_sum = tx.filter(ttype='OUT').aggregate(s=Sum('qty'))['s'] or 0
            current = base_stock + float(in_sum) - float(out_sum)
            total_stock += current
            if item.min_stock is not None and current < float(item.min_stock):
                low_stock.append({'name': item.name, 'current': current, 'min': float(item.min_stock)})
        recent_tx = Transaction.objects.select_related('item').all()[:20]
        ctx.update({
            'kpi_total_items': total_items,
            'kpi_total_stock': total_stock,
            'low_stock': low_stock[:20],
            'recent_tx': recent_tx,
        })
        return ctx

# Purchase simple form
@login_required
def purchase_new(request):
    if request.method == 'POST':
        supplier_name = request.POST.get('supplier','').strip()
        note = request.POST.get('note','')
        items = []
        for i in range(1, 21):
            nm = request.POST.get(f'item_{i}','').strip()
            qty = request.POST.get(f'qty_{i}','').strip()
            code = request.POST.get(f'code_{i}','').strip()
            if nm and qty:
                items.append((nm, qty, code))
        if not supplier_name or not items:
            return render(request, 'inventory/purchase_new.html', {'error': 'تامین‌کننده و حداقل یک قلم لازم است.'})
        supplier, _ = Supplier.objects.get_or_create(name=supplier_name)
        order = PurchaseOrder.objects.create(supplier=supplier, note=note, created_by=request.user)
        for nm, qty, code in items:
            item, _ = Item.objects.get_or_create(name=nm)
            PurchaseItem.objects.create(order=order, item=item, qty=qty, code=code or '')
        return redirect('dashboard')
    return render(request, 'inventory/purchase_new.html')

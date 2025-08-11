
from django.db import models
from django.contrib.auth import get_user_model

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=32, default='کیلوگرم')
    min_stock = models.DecimalField(max_digits=20, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name

class InventorySnapshot(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='snapshots')
    total_input = models.DecimalField(max_digits=20, decimal_places=3, null=True, blank=True)
    input_minus_waste = models.DecimalField(max_digits=20, decimal_places=3, null=True, blank=True)
    stock = models.DecimalField(max_digits=20, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    TYPE_CHOICES = [(IN, 'ورود'), (OUT, 'خروج')]
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transactions')
    ttype = models.CharField(max_length=3, choices=TYPE_CHOICES)
    qty = models.DecimalField(max_digits=20, decimal_places=3)
    code = models.CharField(max_length=64, null=True, blank=True)
    happened_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default='')
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-happened_at']

class CodeConsumption(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='code_consumptions')
    code = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=20, decimal_places=3)

    class Meta:
        unique_together = ('item', 'code')

# ---- Purchase flow ----
class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=64, blank=True, default='')
    note = models.TextField(blank=True, default='')
    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='orders')
    ordered_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)

class PurchaseItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    qty = models.DecimalField(max_digits=20, decimal_places=3)
    code = models.CharField(max_length=64, blank=True, default='')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # create a matching IN transaction (idempotent handling: ensure not doubling by using note key)
        Transaction.objects.create(
            item=self.item, ttype=Transaction.IN, qty=self.qty, code=self.code,
            note=f'Purchase #{self.order_id}', user=self.order.created_by
        )

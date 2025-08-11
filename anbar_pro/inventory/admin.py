
from django.contrib import admin
from .models import Item, InventorySnapshot, Transaction, CodeConsumption, Supplier, PurchaseOrder, PurchaseItem

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','unit','min_stock')
    search_fields = ('name',)

@admin.register(InventorySnapshot)
class InvSnapAdmin(admin.ModelAdmin):
    list_display = ('item','stock','total_input','input_minus_waste','created_at')
    search_fields = ('item__name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('item','ttype','qty','code','happened_at','user')
    list_filter = ('ttype', 'code')
    search_fields = ('item__name','code','note')

@admin.register(CodeConsumption)
class CodeConsumptionAdmin(admin.ModelAdmin):
    list_display = ('item','code','amount')
    search_fields = ('item__name','code')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id','supplier','ordered_at','created_by')
    inlines = [PurchaseItemInline]

from rest_framework import serializers
from .models import Item, Transaction, InventorySnapshot, CodeConsumption

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','name','unit']

class TransactionSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    class Meta:
        model = Transaction
        fields = ['id','item','item_name','ttype','qty','code','happened_at','note']

class InventorySnapshotSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    class Meta:
        model = InventorySnapshot
        fields = ['id','item','item_name','total_input','input_minus_waste','stock','created_at']

class CodeConsumptionSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    class Meta:
        model = CodeConsumption
        fields = ['id','item','item_name','code','amount']

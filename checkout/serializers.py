from rest_framework import serializers
from .models import Item, PricingRule

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'sku', 'unit_price']


class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRule
        fields = "__all__"
        
class ScanItemSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=10)

    def validate_sku(self, value):
        """
        Ensure that the SKU exists in the Item database.
        """
        if not Item.objects.filter(sku=value).exists():
            raise serializers.ValidationError("Item with this SKU does not exist.")
        return value

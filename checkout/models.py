from django.db import models

class Item(models.Model):
    sku = models.CharField(max_length=10, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sku} - ${self.unit_price}"
    

class PricingRule(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    special_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.sku} - {self.quantity} for ${self.special_price}"
from decimal import Decimal

class Item:
    """
    The Item class represents items.

    Attributes:
        sku (str): A string by sku.
        unit_price (Decimal): A Decimal to keep unit_price.
    """
    def __init__(self, sku: str, unit_price: float):
        self.sku = sku
        self.unit_price = unit_price

class PricingRule:
    """
    Handles Pricing rule feature and its type.
    """
    def calculate_price(self, quantity: int, unit_price: Decimal) -> Decimal:
        raise NotImplementedError("Subclasses should implement this method")

class StandardPricing(PricingRule):
    """
    Handles Standard Pricing feature and extends pricing rule.
    """
    def calculate_price(self, quantity: int, unit_price: Decimal) -> Decimal:
        return unit_price * quantity

class BulkPricing(PricingRule):
    """
    Handles Bulk Pricing feature and extends pricing rule.
    """
    def __init__(self, bulk_quantity: int, bulk_price: Decimal):
        self.bulk_quantity = bulk_quantity
        self.bulk_price = bulk_price

    def calculate_price(self, quantity: int, unit_price: Decimal) -> Decimal:
        bulk_count = quantity // self.bulk_quantity
        remainder = quantity % self.bulk_quantity
        return bulk_count * self.bulk_price + remainder * unit_price

class CheckOut:
    """
    The CheckOut class represents a checkout system where items can be scanned,
    and their total price is calculated based on flexible pricing rules.

    Attributes:
        pricing_rules (dict): A dictionary of pricing rules, keyed by SKU.
        cart (dict): A dictionary to keep track of scanned items.
    """
    def __init__(self, pricing_rules):
        """
        Initializes the checkout system with pricing rules.

        Args:
            pricing_rules (dict): Pricing rules where the key is SKU and the value
                                  is a dict with 'quantity' and 'special_price'.
        """
        self.pricing_rules = pricing_rules
        self.cart = {}

    def scan(self, item):
        """
        Adds an item to the cart. Increments the count if the item is already scanned.

        Args:
            item (Item): The item to be added to the cart.
        """
        if item.sku in self.cart:
            self.cart[item.sku]['count'] += 1
        else:
            self.cart[item.sku] = {'item': item, 'count': 1}

    def total(self):
        """
        Calculates the total price of all items in the cart, applying any special pricing rules.

        Returns:
            float: The total price of the items in the cart.
        """
        total_price = 0
        for sku, details in self.cart.items():
            item = details['item']
            count = details['count']
            total_price += self._calculate_item_total(item, count)
        return total_price

    def _calculate_item_total(self, item, count):
        """
        Calculates the total price for a specific item, applying any special pricing if available.

        Args:
            item (Item): The item to calculate the price for.
            count (int): The quantity of the item in the cart.

        Returns:
            float: The calculated total price for the given item and count.
        """
        pricing_rule = self.pricing_rules.get(item.sku)
        if pricing_rule and count >= pricing_rule['quantity']:
            num_special_price_groups = count // pricing_rule['quantity']
            remainder = count % pricing_rule['quantity']
            return (num_special_price_groups * pricing_rule['special_price'] +
                    remainder * item.unit_price)
        else:
            return count * item.unit_price

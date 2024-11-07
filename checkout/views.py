# Third-party imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
# local imports
from .services.checkout_service import CheckOut
from .models import Item, PricingRule
from .serializers import ScanItemSerializer, PricingRuleSerializer, ItemSerializer

class ItemViewSet(APIView):
    """
    A ViewSet for managing the Item model.
    """
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PricingRuleViewSet(APIView):
    """
    A ViewSet for managing the Pricing Rule model.
    """
    def post(self, request):
        serializer = PricingRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckoutViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing the checkout process, including scanning items and calculating totals.
    """
    
    def __init__(self, **kwargs):
        """
        Initializes the view set and sets up the checkout instance with current pricing rules.
        """
        super().__init__(**kwargs)
        # Set up pricing rules for CheckOut
        pricing_rules = {
            rule.item.sku: {
                'quantity': rule.quantity,
                'special_price': rule.special_price
            }
            for rule in PricingRule.objects.all()
        }
        self.checkout = CheckOut(pricing_rules)

    @action(detail=False, methods=['post'])
    def scan(self, request):
        """
        Endpoint to scan an item and add it to the checkout cart.

        Expected Payload:
        {
            "sku": "A"
        }

        Responses:
        - 200 OK: {"message": "Item A scanned"}
        - 400 Bad Request: {"error": "Item with this SKU does not exist."}
        - 404 Not Found: {"error": "Item not found"}
        """
        serializer = ScanItemSerializer(data=request.data)
        if serializer.is_valid():
            sku = serializer.validated_data['sku']
            item = Item.objects.get(sku=sku)  # We already know this exists from validation
            self.checkout.scan(item)
            return Response({"message": f"Item {sku} scanned"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def total(self, request):
        """
        Endpoint to calculate the total price of all scanned items.

        Responses:
        - 200 OK: {"total": 130.00}
        """
        total_price = self.checkout.total()
        return Response({"total": total_price}, status=status.HTTP_200_OK)

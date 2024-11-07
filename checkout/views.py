from django.shortcuts import get_object_or_404
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
    ViewSet for managing the checkout process with Redis session management.
    """

    def initialize_checkout(self, request):
        """
        Initializes the checkout instance and retrieves or sets the cart in the session.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            CheckOut: A checkout instance with pricing rules loaded.
        """
        pricing_rules = {
            rule.item.sku: {
                'quantity': rule.quantity,
                'special_price': rule.special_price
            }
            for rule in PricingRule.objects.filter(status=True)
        }
        checkout = CheckOut(pricing_rules)

        # Retrieve cart from session or initialize empty cart
        cart = request.session.get('cart', {})
        for sku, details in cart.items():
            item = get_object_or_404(Item, sku=sku)
            for _ in range(details['count']):
                checkout.scan(item)
        return checkout

    def update_session_cart(self, request, checkout):
        """
        Updates the session cart data with the current state of the checkout.

        Args:
            request (Request): The HTTP request object.
            checkout (CheckOut): The checkout instance to save.
        """
        cart_data = {sku: {'count': details['count']} for sku, details in checkout.cart.items()}
        request.session['cart'] = cart_data
        request.session.modified = True

    @action(detail=False, methods=['post'])
    def scan(self, request):
        """
        API endpoint to scan an item and add it to the checkout session.

        Payload:
            {"sku": "A"}

        Response:
            Success: {"message": "Item A scanned"}
            Error: {"error": "Item not found"} or {"error": "Invalid SKU provided"}
        """
        serializer = ScanItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sku = serializer.validated_data['sku']
            item = Item.objects.get(sku=sku)
            checkout = self.initialize_checkout(request)
            checkout.scan(item)
            self.update_session_cart(request, checkout)
            return Response({"message": f"Item {sku} scanned"}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def total(self, request):
        """
        API endpoint to retrieve the total price of all items in the session.

        Response:
            Success: {"total": 130.0}
            Error: {"error": "Error calculating total"}
        """
        try:
            checkout = self.initialize_checkout(request)
            total_price = checkout.total()
            return Response({"total": total_price}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error calculating total: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """
        Clears the checkout session data.
        
        Response:
            200 OK: {"message": "Checkout session cleared"}
        """
        request.session.pop('cart', None)
        return Response({"message": "Checkout session cleared"}, status=status.HTTP_200_OK)
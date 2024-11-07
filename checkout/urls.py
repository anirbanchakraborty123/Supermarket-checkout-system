from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckoutViewSet, ItemViewSet, PricingRuleViewSet

# Router for the Checkout API endpoints
router = DefaultRouter()
router.register(r'checkout', CheckoutViewSet, basename='checkout')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('items/', ItemViewSet.as_view(), name='item-list'),
    path('pricing_rules/', PricingRuleViewSet.as_view(), name='pricing-rule-list'),
]

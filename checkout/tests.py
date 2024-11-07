import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item, PricingRule

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_items(db):
    item_a = Item.objects.create(sku="A", unit_price=50)
    item_b = Item.objects.create(sku="B", unit_price=30)
    PricingRule.objects.create(item=item_a, quantity=3, special_price=130)
    PricingRule.objects.create(item=item_b, quantity=2, special_price=45)
    return {"A": item_a, "B": item_b}

def test_scan_item_success(api_client, setup_items):
    """ Test to scan items to simulate a cart. 
    """
    url = reverse('checkout-scan')
    response = api_client.post(url, {"sku": "A"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Item A scanned"}

def test_scan_item_invalid_sku(api_client):
    """ Test to scan items with invalid SKU to simulate a cart 
        and to check if it can handle invalid SKU. 
    """
    url = reverse('checkout-scan')
    response = api_client.post(url, {"sku": "Z"})  # SKU 'Z' does not exist
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "sku" in response.json()

def test_total_price(api_client, setup_items):
    """ Test to scan items to simulate a cart with special prices and get the
        total price after applying special prices. 
    """
    api_client.post(reverse('checkout-scan'), {"sku": "A"})
    api_client.post(reverse('checkout-scan'), {"sku": "A"})
    api_client.post(reverse('checkout-scan'), {"sku": "A"})

    # Get total
    response = api_client.get(reverse('checkout-total'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"total": 130.00}

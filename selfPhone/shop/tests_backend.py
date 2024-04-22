from django.test import TestCase, Client
from django.urls import reverse
from .models import *
import json


class ShopBackendTestCase(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.client = Client()
        self.user = Costumer.objects.create(
            customer=User.objects.create_user(
                username='testuser', password='12345'),
            first_name='Test',
            last_name='User',
            email='test@example.com'
        )
        self.address = Address.objects.create(
            customer=self.user,
            postcode='12345',
            city='City',
            street='Street',
            house_number='1'
        )
        self.product = Product.objects.create(
            name='Test Product',
            smartphone=Smartphone.objects.create(
                manufacturer='Apple',
                model='iPhone 13',
                color='Schwarz',
                memory_size='8',
                storage_size='128',
                akku=3000,
                basic_price=999.99
            )
        )

    def test_add_to_cart(self):
        # Test adding an item to the cart
        response = self.client.post(reverse('shopBackend'), json.dumps({
            'action': 'add_to_cart',
            'product_id': self.product.id,
            'quantity': 1
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart_quantity', response.json())

    def test_update_cart(self):
        # Test updating an item in the cart
        cart_item = CartItem.objects.create(product=self.product, quantity=1)
        response = self.client.post(reverse('shopBackend'), json.dumps({
            'action': 'update_cart',
            'cart_item_id': cart_item.id,
            'quantity': 2
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_remove_from_cart(self):
        # Test removing an item from the cart
        cart_item = CartItem.objects.create(product=self.product, quantity=1)
        response = self.client.post(reverse('shopBackend'), json.dumps({
            'action': 'remove_from_cart',
            'cart_item_id': cart_item.id
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        # Test creating an order
        response = self.client.post(reverse('shopBackend'), json.dumps({
            'action': 'create_order',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('order_id', response.json())

    def test_invalid_action(self):
        # Test handling of an unknown action
        response = self.client.post(reverse('shopBackend'), json.dumps({
            'action': 'unknown_action',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

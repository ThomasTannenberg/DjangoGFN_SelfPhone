from django.test import TestCase, Client
from django.urls import reverse
from .models import *
import json


class ShopBackendTestCase(TestCase):
    def setUp(self):
        """Set up test data for the shopBackend tests."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.customer = Costumer.objects.create(
            customer=self.user, first_name='Test', last_name='User', email='test@example.com'
        )
        self.address = Address.objects.create(
            customer=self.customer, postcode='12345', city='Test City', street='123 Test St', house_number='1'
        )
        self.smartphone = Smartphone.objects.create(
            manufacturer=Manufacturer.APPLE, model='iPhone 13', color=Color.SCHWARZ,
            memory_size=Memory_size.acht, storage_size=Storage_size.einhundertachtundzwanzig,
            akku=3000, basic_price=799.99
        )
        self.product = Product.objects.create(
            smartphone=self.smartphone, name='iPhone 13 Schwarz')
        # Make sure to define the URL name in urls.py
        self.url = reverse('shopBackend')

    def test_add_to_cart(self):
        """Test adding a product to the cart via POST request."""
        self.client.login(username='testuser', password='testpassword')
        data = {
            'action': 'add_to_cart',
            'product_id': self.product.id,
            'quantity': 1
        }
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Produkt erfolgreich zum Warenkorb hinzugefügt',
                      response.json()['message'])
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 1)

    def test_update_cart(self):
        """Test updating an item in the cart."""
        cart_item = CartItem.objects.create(product=self.product, quantity=1)
        data = {
            'action': 'update_cart',
            'cart_item_id': cart_item.id,
            'quantity': 2
        }
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Warenkorb erfolgreich aktualisiert',
                      response.json()['message'])
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_from_cart(self):
        """Test removing an item from the cart."""
        cart_item = CartItem.objects.create(product=self.product, quantity=1)
        data = {
            'action': 'remove_from_cart',
            'cart_item_id': cart_item.id
        }
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Artikel erfolgreich aus dem Warenkorb entfernt',
                      response.json()['message'])
        self.assertEqual(CartItem.objects.count(), 0)

    def test_create_order(self):
        """Test creating an order with items."""
        cart_item = CartItem.objects.create(product=self.product, quantity=1)
        data = {
            'action': 'create_order'
        }
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bestellung erfolgreich erstellt',
                      response.json()['message'])

    def test_invalid_action(self):
        """Test handling of invalid actions."""
        data = {
            'action': 'invalid_action'
        }
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unbekannte Aktion', response.json()['error'])

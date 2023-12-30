from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from shop.models import Category, Product


class ShopAPITestCase(APITestCase):
    @staticmethod
    def format_datetime(value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestCategory(ShopAPITestCase):
    url = reverse_lazy('category-list')  # completion done by the router

    def test_list(self):
        # Create 2 categories : one active, the other inactive
        category = Category.objects.create(name="Fruits", active=True)
        Category.objects.create(name="Légumes", active=False)

        # Make GET call using Test client
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': category.pk,  # Primary Key
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            },
        ]
        self.assertEqual(excepted, response.json())

    def test_create(self):
        # Check no category exists (in the test client)
        self.assertFalse(Category.objects.exists())

        # Check one cannot create a category from the public API
        response = self.client.post(self.url, data={'name': 'Nouvelle Catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Category.objects.exists())  # Double check


class TestProduct(ShopAPITestCase):
    url_list = reverse_lazy('product-list')

    def test_list(self):
        # Create 1 category and 2 products in this category : one active, the other inactive
        category = Category.objects.create(name="Fruits", active=True)
        product = Product.objects.create(name="Pomme", active=True, category=category)
        Product.objects.create(name="Papaye", active=False, category=category)

        # Make GET call using Test client
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': product.pk,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'name': product.name,
                'category': product.category.id,  # Foreign Key
            },
        ]
        self.assertEqual(excepted, response.json())

    def test_create(self):
        # Check no product exists (in the test client)
        self.assertFalse(Product.objects.exists())

        # Check one cannot create a product from the public API
        category = Category.objects.create(name="Fruits", active=True)
        response = self.client.post(self.url_list, data={'name': 'Nouveau Produit', 'category': category})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Product.objects.exists())  # Double check

    # TODO: Create a test for active products in inactive Category
    # TODO: assess if possible to create the category as a class attribute
    # TODO: Create a test for details on a non-existing product

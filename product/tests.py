from django.test import TestCase
from .models import Product


class AnimalTestCase(TestCase):
    def setUp(self):
        Product.objects.create(title='mahdi',description="hi",price="200",slug='mahdi',category='Electronic',is_public=True,discount="1")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        mahdi = Product.objects.get(name="mahdi")

        self.assertEqual(mahdi.speak(), 'The lion says "roar"')


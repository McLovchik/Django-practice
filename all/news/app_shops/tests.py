import random
import string

from django.test import TestCase
from django.urls import reverse
from .models import Shop
from http import HTTPStatus
from django.contrib.auth.models import User


NUMBER_OF_ITEMS = 10
LETTERS = string.ascii_lowercase


class ShopsListPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Pasha',
            password='az267015'
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        for item_index in range(NUMBER_OF_ITEMS):
            rand_string = ''.join(random.choice(LETTERS) for _ in range(20))
            Shop.objects.create(
                name=f'{rand_string}'
            )

    def test_shops_list_page(self):
        url = reverse('shops-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shops/shops_list.html')
        self.assertTrue(len(response.context['shops_list']) == NUMBER_OF_ITEMS)

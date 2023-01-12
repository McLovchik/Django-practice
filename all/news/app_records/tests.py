import random
import string

from django.test import TestCase
from django.urls import reverse
from .models import Record
from django.contrib.auth.models import User
from http import HTTPStatus


NUMBER_OF_ITEMS = 10
LETTERS = string.ascii_lowercase


class RecordsListPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for item_index in range(NUMBER_OF_ITEMS):
            rand_string = ''.join(random.choice(LETTERS) for _ in range(20))
            Record.objects.create(
                text=f'{rand_string}'
            )

    def test_records_list_page(self):
        url = reverse('records-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'records/records_list.html')
        self.assertTrue(len(response.context['records_list']) == NUMBER_OF_ITEMS)


class RecordCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Pasha',
            password='az267015'
        )
        self.client.force_login(self.user)
        self.path = reverse('create-record')
        self.record = {
            'text': 'blablablabalabaal'
        }

    def test_create_record_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'records/create_record.html')

    def test_create_record_post(self):
        response = self.client.post(self.path, self.record)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(Record.objects.filter(text=self.record['text']).exists())


class RecordDetailPageTest(TestCase):
    def setUp(self):
        self.record = Record.objects.create(text='blablablabaala')
        self.path = reverse('record-detail', kwargs={'pk': self.record.id})

    def test_record_detail_page(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'records/record_detail.html')
        self.assertEqual(response.context_data['record'].text, self.record.text)
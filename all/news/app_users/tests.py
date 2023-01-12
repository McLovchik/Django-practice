from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class RegisterPageTest(TestCase):
    def setUp(self) -> None:
        self.path = reverse('register')
        usual_users_group = Group.objects.create(name='Обычные пользователи')
        self.user = {
            'username': 'Masha', 'first_name': 'Masha', 'last_name': 'Pavlova',
            'password1': 'sdfPfdsf23', 'password2': 'sdfPfdsf23',
        }

    def test_register_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_post(self):
        username = self.user['username']
        response = self.client.post(self.path, self.user)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(username=username).exists())


class EditUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Masha',
            first_name='Masha',
            last_name='Pavlova',
            password='sdfPfdsf23',
        )
        self.client.force_login(self.user)
        self.path = reverse('profile-edit', kwargs={'user_id': self.user.id})

    def test_edit_user_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_edit.html')


class LoginPageTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='Pasha',
            password='az267015'
        )
        self.client.force_login(self.user)

    def test_login_page(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

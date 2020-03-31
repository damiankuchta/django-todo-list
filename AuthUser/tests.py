from django.test import TestCase, Client
from django.urls import resolve, reverse
from .views import create_account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your tests here.
class CreateUserTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.url = reverse('create-account')
        self.response = self.c.get(self.url)
        self.view = resolve('/create_account/')

    def test_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_func(self):
        self.assertEquals(self.view.func, create_account)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

    def test_form_contains_fields(self):
        form = self.response.context.get('form')
        requred_fields = ['username', 'email', 'password1', 'password2']
        actual_fields = list(form.fields)
        self.assertEquals(requred_fields, actual_fields)

    def test_form_does_not_contains_fields(self):
        form = self.response.context.get('form')
        requred_fields = ['username', 'email', 'password1', 'test']
        actual_fields = list(form.fields)
        self.assertNotEquals(requred_fields, actual_fields)

    def test_create_list_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class SuccsefullUserCration(TestCase):
    def setUp(self):
        data = {'username': 'username',
                'email': 'test@gmail.com',
                'password1': 'test_password',
                'password2': 'test_password'}
        self.url = reverse('create-account')
        self.response = self.client.post(self.url, data)
        self.view = resolve('/create_account/')

    def test_redirected(self):
        url = reverse('display-lists')
        self.assertRedirects(self.response, url)

    def test_is_user_created(self):
        self.assertTrue(User.objects.exists())

    def test_is_user_loggedin(self):
        response = self.client.get(self.url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class FailedUserCreation(TestCase):
    def setUp(self):
        self.url = reverse('create-account')
        self.response = self.client.post(self.url, {})
        self.view = resolve('/create_account/')

    def test_redirected(self):
        url = reverse('display-lists')
        self.assertEqual(self.response.status_code, 200)

    def test_is_user_created(self):
        self.assertFalse(User.objects.exists())

    def test_is_user_loggedin(self):
        response = self.client.get(self.url)
        user = response.context.get('user')
        self.assertFalse(user.is_authenticated)

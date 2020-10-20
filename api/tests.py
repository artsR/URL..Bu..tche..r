from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.contrib.auth.models import User
from django.urls import reverse

from urlbutcher.models import Url



class APISlugTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.credentials_auth_user = {'username': 'test', 'password': 'Test123'}
        self.auth_user = User.objects.create(**self.credentials_auth_user)

        self.valid_url = 'http://www.example.pl'

    def test_slug_list_as_anonymous(self):
        """List of slugs can be accessed only by authenticated users.
        Anonymous users should obtain 403 as response.
        """
        response = self.client.get(reverse('api:slug_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_slug_list_as_authenticated(self):
        """List of slugs should respond with 200 for authenticated users."""
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(reverse('api:slug_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

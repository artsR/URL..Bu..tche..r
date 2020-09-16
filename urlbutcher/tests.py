import random
import string
from datetime import timedelta

from django.test import TestCase, SimpleTestCase
from django.utils import timezone

# Create your tests here.
class HomePagesTest(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

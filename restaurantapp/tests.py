from django.test import TestCase
from django.urls import reverse

class RestaurantTestCase(TestCase):
    def setUp(self):
        pass


class LoginRequiredTestCase(TestCase):
    '''anonymous cannot see this page'''

    def test_anonymous_cannot_see_page(self):
        response = self.client.get(reverse('orders'))
        self.assertRedirects(response,"/user/login/?login=/order")

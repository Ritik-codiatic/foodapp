from django.test import TestCase
from django.urls import reverse
from restaurantapp.models import Restaurant
from userapp.user import UserFactory
import datetime
from restaurantapp.restaurant import RestaurantFactory
from faker import Factory

faker = Factory.create()

class TestItem(TestCase):
    def setUp(self) -> None:
        self.client.force_login(user=UserFactory())
        self.response = self.client.post(reverse('add_restaurant'),{
            'name': faker.name(),
            'address': faker.address(),
            'opening_time': datetime.time(),
            'closing_time': datetime.datetime.now(),
            'contact_number': faker.random_number(10),
            'restaurant_type': 'pure veg',
            'location': faker.random_number(10)
        })
    def test_restaurant_choices(self):
        self.assertEqual(self.response.context['form'].errors['restaurant_type'][0],'Select a valid choice. pure veg is not one of the available choices.')

    def test_valid_time(self):
        self.assertEqual(self.response.context['form'].errors['closing_time'][0],'Enter a valid time.')

from django.test import TestCase
from django.urls import reverse
from restaurantapp.models import Restaurant
from userapp.models import CustomUser
import datetime

class TestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            first_name="abhishek",
            last_name="pawar",
            email="abhishek@gmail.com",
            mobile_number='7987907979',
            address="indore",
            gender="Male",
            user_type="Restaurant Owner",
            )
        restaurant = Restaurant.objects.create(name="Test Restaurant",
            owner=user,
            opening_time = datetime.datetime.now(),
            closing_time = datetime.datetime.now(),
            contact_number = '9092090902',
            restaurant_type = 'veg')

    def test_restaurant_created_successfully(self):
        restuarant = Restaurant.objects.get(name="Test Restaurant")
        self.assertEqual(restuarant.contact_number,'9092090902')
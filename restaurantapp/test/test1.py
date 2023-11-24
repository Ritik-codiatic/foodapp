from django.test import TestCase
from django.urls import reverse
from restaurantapp.models import Restaurant
from userapp.models import CustomUser
import datetime
from userapp.user import UserFactory
from restaurantapp.restaurant import RestaurantFactory
from restaurantapp.models import Restaurant
class RestaurantTestCase(TestCase):
    def setUp(self):
        self.restaurant = RestaurantFactory()
        self.restaurant.owner = UserFactory()
        # user = CustomUser.objects.create(
        #     first_name="abhishek",
        #     last_name="pawar",
        #     email="abhishek@gmail.com",
        #     mobile_number='7987907979',
        #     address="indore",
        #     gender="Male",
        #     user_type="Restaurant Owner",)
        # restaurant = Restaurant.objects.create(name="Test Restaurant",
        #     owner=user,
        #     opening_time = datetime.datetime.now(),
        #     closing_time = datetime.datetime.now(),
        #     contact_number = '9092090902',
        #     restaurant_type = 'veg')

    def test_restaurant_created_successfully(self):
        self.assertIsInstance(self.restaurant,Restaurant)
    
    def test_restaurant_updated_successfully(self):
        self.restuarant.name = "Test2"
        self.restuarant.save()
        self.assertEqual(self.restuarant.name,'Test2')

    def test_restaurant_deleted_successfully(self):
        self.client.force_login(user=self.restaurant.owner)
        response = self.client.delete("/editrestaurant/"+str(self.restaurant.id))
        self.assertEqual(response.status_code,200)
        
    

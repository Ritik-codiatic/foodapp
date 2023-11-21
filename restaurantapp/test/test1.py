from django.test import TestCase
from django.urls import reverse
from restaurantapp.models import Restaurant
from userapp.models import CustomUser
import datetime
class RestaurantTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            first_name="abhishek",
            last_name="pawar",
            email="abhishek@gmail.com",
            mobile_number='7987907979',
            address="indore",
            gender="Male",
            user_type="Restaurant Owner",)
        restaurant = Restaurant.objects.create(name="Test Restaurant",
            owner=user,
            opening_time = datetime.datetime.now(),
            closing_time = datetime.datetime.now(),
            contact_number = '9092090902',
            restaurant_type = 'veg')

    def test_restaurant_created_successfully(self):
        restuarant = Restaurant.objects.get(name="Test Restaurant")
        self.assertEqual(restuarant.contact_number,'9092090902')
    
    def test_restaurant_updated_successfully(self):
        restuarant = Restaurant.objects.get(name="Test Restaurant")
        restuarant.name = "Test2"
        restuarant.save()
        self.assertEqual(restuarant.name,'Test2')

    def test_restaurant_deleted_successfully(self):
        user=CustomUser.objects.get(first_name="abhishek")
        self.client.force_login(user=user)
        restaurant=Restaurant.objects.get(name="Test Restaurant")
        response = self.client.delete("/editrestaurant/"+str(restaurant.id))
        self.assertEqual(response.status_code,200)
        
import factory
from .models import Restaurant
from faker import Factory
from userapp.user import UserFactory
import datetime
faker = Factory.create()


class RestaurantFactory(factory.django.DjangoModelFactory):
   
    class Meta:
        model = Restaurant
        django_get_or_create = ('name','owner','address','opening_time','closing_time','restaurant_type') 
    name = faker.name()
    opening_time = datetime.datetime.now()
    closing_time = datetime.datetime.now()
    restaurant_type = 'veg'
    owner = factory.SubFactory(UserFactory)
    address = faker.address()
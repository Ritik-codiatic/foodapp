import factory
from .models import CustomUser
from faker import Factory

faker = Factory.create()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ('first_name','last_name','email','mobile_number','user_type','address','gender','password') 
    first_name = faker.name()
    last_name = faker.name()
    email = faker.email()
    mobile_number = faker.random_number(10)
    user_type = 'customer'
    address = faker.text(50)
    gender = 'Male'
    password = faker.password()

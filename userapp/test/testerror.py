from django.test import TestCase
from userapp.models import CustomUser
from userapp.forms import UserForm
from django.urls import reverse
from userapp.user import UserFactory
import factory
from faker import Factory

faker = Factory.create()

class TestError(TestCase):
    '''test cases to check errors'''
    
    def setUp(self) -> None:
        self.response = self.client.post(reverse('signup'),
            {'email':'ritikmakwmngmal.com',
            'mobile_number':faker.random_number(10),
            'address':faker.address(),
            'user_type':'owner',
            'gender':'Male',
            'password1':faker.password(),})

    def test_password_required(self):
        self.assertEqual(self.response.context['form'].errors['password2'][0],'This field is required.')

    def test_email_not_valid(self):
        self.assertEqual(self.response.context['form'].errors['email'][0],'Enter a valid email address.')
    
    def test_password_not_matched(self):
        response = self.client.post(reverse('signup'),
            {'email':faker.email(),
            'mobile_number':faker.random_number(10),
            'address':faker.address(),
            'user_type':'owner',
            'gender':'Male',
            'password1':faker.password(),
            'password2':faker.password()})
        self.assertEqual(response.context['form'].errors['password2'][0],"The two password fields didn’t match.")
        
    def test_email_exists(self):
        user = UserFactory()
        response = self.client.post(reverse('signup'),
            {'email':user.email,
            'mobile_number':faker.random_number(10),
            'address':faker.address(),
            'user_type':'owner',
            'gender':'Male',
            'password1':faker.password(),
            'password2':faker.password()})
        self.assertEqual(response.context['form'].errors['email'][0],'A user is already registered with this email address')

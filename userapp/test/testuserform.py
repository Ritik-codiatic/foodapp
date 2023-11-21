from django.test import TestCase
from userapp.models import CustomUser
from userapp.forms import UserForm
from django.urls import reverse
from userapp.user import UserFactory
import factory

class UserFormTestCase(TestCase):
    '''user form is valid'''

    def test_user_form(self):
        form_data = {'first_name':'abhishek','last_name':'pawar','user_type':'customer','address':'indore'
                     ,'password1':'Indore@123','password2':'Indore@123','mobile_number':'6876687686','email':'abhishek@gmail.com','gender':'Male',}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_not_valid(self):
        form_data = {'first_name':'abhishek','last_name':'pawar','user_type':'customer','address':'indore'
                     ,'password1':'Indore@123','password2':'@123','mobile_number':'6876687686','email':'abhishek@gmail.com','gender':'Male',}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
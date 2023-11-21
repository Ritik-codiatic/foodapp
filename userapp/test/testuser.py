from django.test import TestCase
from userapp.models import CustomUser
from userapp.forms import UserForm
from django.urls import reverse
from userapp.user import UserFactory
import factory
class UserTestCase(TestCase):
    def setUp(self):
            UserFactory(
                first_name="abhishek",
                last_name="pawar",
                email="abhishek@gmail.com",
                mobile_number='7987907979',
                user_type="Customer",
                address="indore",
                gender="Male")
            
    
    def test_user_is_created(self):
        '''user is created successfully '''

        user = CustomUser.objects.get(first_name="abhishek")
        self.assertEqual(user.last_name,'pawar')
    
    def test_user_is_updated(self):
        '''user is updated '''
        user = CustomUser.objects.get(email="abhishek@gmail.com")
        user.first_name = "abhi"
        user.save()
        self.assertEqual(user.first_name,"abhi")

    def multiple_user_created(self):
        '''multiple user is created'''
        user = UserFactory.create_batch(5,
            first_name='abhishek',
            mobile_number=factory.Sequence(lambda n:'{0}'.format(n)),
            email=factory.Sequence(lambda i:'{0}@gmail.com'.format(i)))
        
        self.assertEqual(len(user),5)
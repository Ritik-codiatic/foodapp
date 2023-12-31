from django.test import TestCase
from .models import CustomUser
from .forms import UserForm
from django.urls import reverse
from .user import UserFactory
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
    

class UserFormTestCase(TestCase):
    '''user form is valid'''

    def test_user_form(self):
        form_data = {'first_name':'abhishek','last_name':'pawar','user_type':'Customer','address':'indore'
                     ,'password1':'Indore@123','password2':'Indore@123','mobile_number':'6876687686','email':'abhishek@gmail.com','gender':'Male',}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewsTestCase(TestCase):
    '''test login page loads properly'''

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,"user/home.html")
    
    def test_login_user(self):
        CustomUser.objects.create(email="ritik@gmail.com",password="Ritik@gmail.com")
        user = CustomUser.objects.get(email="ritik@gmail.com")
        login = self.client.post(reverse('login'),self.client.force_login(user=user))
        #user = self.client.post(reverse('login'),{"email":"ritik@gmail.com","password":"Ritik@123"})
        self.assertEqual(login.status_code,200)

class LoginRequiredTestCase(TestCase):
    '''anonymous cannot see this page'''

    def test_anonymous_cannot_see_page(self):
        response = self.client.get(reverse('orders'))
        self.assertRedirects(response,"/user/login/?login=/order")

    def authenticated_user_can_see_page(self):
        user = CustomUser.objects.create(
            first_name="abhishek",
            last_name="pawar",
            email="abhishek@gmail.com",
            mobile_number='7987907979',
            user_type="Customer",
            address="indore",
            gender="Male")
        self.client.force_login(user=user)
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
    

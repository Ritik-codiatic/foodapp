from django.test import TestCase
from .models import CustomUser
from .forms import UserForm
from django.urls import reverse
class UserTestCase(TestCase):
    def setUp(self):
        for i in range(10):
            CustomUser.objects.create(
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
        user = self.client.post(reverse('login'),{"email":"ritik@gmail.com","password":"Ritik@123"})
        self.assertEqual(user.status_code,200)

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
    

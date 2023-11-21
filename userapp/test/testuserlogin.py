from django.test import TestCase
from userapp.models import CustomUser
from userapp.forms import UserForm
from django.urls import reverse
from userapp.user import UserFactory
import factory

class ViewsTestCase(TestCase):
    '''test login page loads properly'''
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,"user/home.html")
    
    def test_login_user(self):
        login = self.client.post(reverse('login'),self.client.force_login(user=self.user))
        #user = self.client.post(reverse('login'),{"email":"ritik@gmail.com","password":"Ritik@123"})
        #login.context_data['form'].is_valid()
        self.assertTrue(login.context['user'].is_authenticated)
    
    def test_user_logout(self):
        '''test user is logged out'''
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code,302)
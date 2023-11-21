from django.test import TestCase
from userapp.models import CustomUser
from userapp.forms import UserForm
from django.urls import reverse
from userapp.user import UserFactory
import factory

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
            user_type="customer",
            address="indore",
            gender="Male")
        self.client.force_login(user=user)
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
    
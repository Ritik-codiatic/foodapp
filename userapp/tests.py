from django.test import TestCase
from .models import CustomUser
class UserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            first_name="abhishek",
            last_name="pawar",
            email="abhishek@gmail.com",
            mobile_number='7987907979',
            user_type="Customer",
            address="indore",
            gender="Male")
    
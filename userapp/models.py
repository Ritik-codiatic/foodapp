# local imp
from .custommanager import UserManager
# django imp
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


#Create your models here.

class CustomUser(AbstractUser):

    USER_TYPES = (("customer","Customer"),
             ("owner","Restaurent Owner")
            )
    GENDER_CHOICES = (("Male","Male"),("Female","Female"))

    user_type = models.CharField(max_length=20,choices=USER_TYPES)
    mobile_number = models.CharField(null=True, max_length=10, unique=True, error_messages={
            'unique': _(
                "A user is already registered with this Mobile number"),
        },)
    address = models.TextField(max_length=100)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES)
    profile_pic = models.ImageField(upload_to='pics',blank=True,null=True)
    city_name = models.ForeignKey('City',on_delete=models.CASCADE,null=True)
    username = None
    email = models.EmailField(_('email address'), unique=True, error_messages={
            'unique': _(
                "A user is already registered with this email address"),
        },)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self) -> str:
       return self.email


class City(models.Model):
    name = models.CharField(max_length=20)
    state = models.ForeignKey('State',on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name
    
class State(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name

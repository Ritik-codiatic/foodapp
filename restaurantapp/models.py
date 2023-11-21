# django imp
from django.db import models
from userapp.models import CustomUser
from django.db.models import Avg,F, Func,FloatField
# libs imp
from location_field.models.plain import PlainLocationField
from datetime import datetime
class Round(Func):
    function = 'ROUND'
    arity = 2
    # Only works as the arity is 2
    arg_joiner = '::numeric, '

    def as_sqlite(self, compiler, connection, **extra_context):
        return super().as_sqlite(compiler, connection, arg_joiner=", ", **extra_context)

class Restaurant(models.Model):
    RESTAURANT_TYPES = (('veg','veg'),
                        ('non veg','non veg'),
                        ('both','both'))
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.TextField()
    opening_time = models.TimeField(auto_now=False)
    closing_time = models.TimeField(auto_now=False)
    contact_number = models.CharField(max_length=10)
    restaurant_type = models.CharField(max_length=20,choices=RESTAURANT_TYPES)
    location = PlainLocationField(based_fields=['city'], zoom=7,null = True)
    created_at = models.DateTimeField(auto_now_add=True ,null=True)
    updated_at = models.DateTimeField(auto_now=True , null=True)

    def average_rating(self) -> float:
        return RestaurantRating.objects.filter(restaurant=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def restaurant_menu_catogory(self):
        return Menu.objects.filter(restaurant=self)

    def __str__(self) -> str:
        return self.name

class MenuCategory(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.name

class MenuItem(models.Model):
    FOOD_TYPES = (
            ('veg','veg'),
            ('non veg','non veg')
        )

    menu_category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    food_type = models.CharField(max_length=20,choices=FOOD_TYPES)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    '''model for item pricing for a particular restaurant '''
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='pics/menuitems',null=True)
    description = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('item', 'restaurant',)


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pics/restaurant_images' )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Common(models.Model):  # COMM0N 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: 
        abstract = True
class Cart(Common):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    order_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    
class CartItem(Common):
    cart_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class OrderDetail(Common):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart,verbose_name='Cart',on_delete=models.PROTECT)
    amount = models.FloatField(verbose_name='Amount')
    stripe_payment_intent = models.CharField( max_length=200,null=True)
    has_paid = models.BooleanField(default=False,verbose_name='Payment Status')


class RestaurantRating(Common):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    order = models.ForeignKey(OrderDetail,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=100,null=True)

# def get_menu_category():
#     res = RestaurantMenu.objects.first()
#     manu_category = MenuCategory.objects.create(res.id, "default menu category")
#     return manu_category.id


# class Notificaton(models.Model):
#     user = models.ManyToManyField(CustomUser)
#     headline = models.CharField(max_length=20)
#     text = models.TextField(max_length=100)
       
#     def __str__(self) -> str:
#         return self.headline
    
# class RestaurantFollower(models.Model):
#     followers = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     following = models.ForeignKey(Restaurant,on_delete=models.CASCADE)



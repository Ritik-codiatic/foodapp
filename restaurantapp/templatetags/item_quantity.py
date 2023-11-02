from django import template
from restaurantapp.models import Menu, CartItem, Cart, RestaurantRating

register = template.Library()

@register.simple_tag()
def item_quantity(item_id, user_id, *args, **kwargs):
        try:
            cart_item = CartItem.objects.get(cart_item__id = item_id, cart__user__id = user_id,cart__is_paid = False)
            return cart_item.quantity
        except:
              return 0
    
@register.simple_tag()
def item_rating(user_id, restaurant_id, order_id, *args, **kwargs):
    try:
        rating = RestaurantRating.objects.get(user__id = user_id, restaurant__id = restaurant_id, order__id = order_id)
        return rating.rating
    except:
        return 0
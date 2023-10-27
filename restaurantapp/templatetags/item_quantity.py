from django import template
from restaurantapp.models import Menu, CartItem, Cart

register = template.Library()

@register.simple_tag()
def item_quantity(item_id, user_id, *args, **kwargs):
        try:
            cart_item = CartItem.objects.get(cart_item__id = item_id, cart__user__id = user_id)
            return cart_item.quantity
        except:
              return 1
        
    
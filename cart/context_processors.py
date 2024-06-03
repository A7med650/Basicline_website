from .models import Cart, CartItem
from .views import __cart_id


def counter(request):
    cart_count = 0
    cart_items = None
    total = 0
    grand_total = 0
    tax = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=__cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart_items = CartItem.objects.filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
                if cart_item.product.sale_price != None and cart_item.product.sale_price > 0:
                    total += (cart_item.quantity*cart_item.product.sale_price)
                else:
                    total += (cart_item.quantity*cart_item.product.price)
            tax = (10 * total)/100
            grand_total = total + tax
        except Cart.DoesNotExist:
            cart_count = 0
        context = {
            'cart_count': cart_count,
            'cart_items': cart_items,
            'grand_total': grand_total,
            'total': total,
        }
        return context

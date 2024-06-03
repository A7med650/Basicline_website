from django.shortcuts import render, redirect
from cart.models import CartItem
from .models import Order, OrderProduct
from .forms import OrderForm
import uuid
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='register_and_login')
def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    total = 0
    tax = 0
    quantity = 0

    for cart_item in cart_items:
        if cart_item.product.sale_price != None and cart_item.product.sale_price > 0:
            total += (cart_item.quantity*cart_item.product.sale_price)
        else:
            total += (cart_item.quantity*cart_item.product.price)
        quantity += cart_item.quantity
    tax = (10*total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = round(grand_total, 2)
            data.tax = round(tax, 2)
            data.save()
            order_number = str(uuid.uuid4()) + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            order_product(request, order)
            context = {
                # 'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return redirect('checkout')
    else:
        return redirect('checkout')


def order_product(request, order):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        if item.product.sale_price != None and item.product.sale_price > 0:
            order_product.product_price = item.product.sale_price
        else:
            order_product.product_price = item.product.price
        order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variation.set(product_variation)
        order_product.save()


@login_required(login_url='register_and_login')
def view_order_products(request, order_number):
    order_products = OrderProduct.objects.filter(
        order__order_number=order_number).select_related('product')
    context = {
        'order_products': order_products,
    }
    return render(request, 'order-detail.html', context)

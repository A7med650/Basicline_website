from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.


def __cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request):
    cart_items = None
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user).select_related('product')
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_items = CartItem.objects.filter(
                cart=cart).select_related('product')
        for cart_item in cart_items:
            if cart_item.product.sale_price != None and cart_item.product.sale_price > 0:
                total += (cart_item.quantity*cart_item.product.sale_price)
            else:
                total += (cart_item.quantity*cart_item.product.price)
            quantity += cart_item.quantity
        tax = (10 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, slug):
    cart_items = None
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=request.user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=request.user)

            ex_var_list = []
            ex_var_list1 = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all().order_by('id')
                ex_var_list.append(list(existing_variation))
                existing_variation = item.variations.all().order_by('-id')
                ex_var_list1.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += int(request.POST.get('quantity'))
                item.save()
            elif product_variation in ex_var_list1:
                index = ex_var_list1.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += int(request.POST.get('quantity'))
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=int(request.POST.get('quantity')), user=request.user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=int(request.POST.get('quantity')), user=request.user)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=__cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=__cart_id(request))
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, cart=cart)

            ex_var_list = []
            ex_var_list1 = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all().order_by('id')
                ex_var_list.append(list(existing_variation))
                existing_variation = item.variations.all().order_by('-id')
                ex_var_list1.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += int(request.POST.get('quantity'))
                item.save()
            elif product_variation in ex_var_list1:
                index = ex_var_list1.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += int(request.POST.get('quantity'))
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=int(request.POST.get('quantity')), cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=int(request.POST.get('quantity')), cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

    context = {
        'product_name': product.product_name,
        'is_cart_item_exists': is_cart_item_exists,
        'first_image_url': product.first_image_url,
        'category_slug': product.category.slug,
        'product_slug': product.slug,
        'product_sale_price': product.sale_price,
        'product_price': product.price,
    }
    from .context_processors import counter
    cart_counter = counter(request)
    context['cart_count'] = cart_counter['cart_count']
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user).select_related('product')
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_items = CartItem.objects.filter(
                cart=cart).select_related('product')
        for cart_item in cart_items:
            if cart_item.product.sale_price != None and cart_item.product.sale_price > 0:
                total += (cart_item.quantity*cart_item.product.sale_price)
            else:
                total += (cart_item.quantity*cart_item.product.price)
            quantity += cart_item.quantity
        tax = (10 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context['total'] = total
    context['grand_total'] = grand_total
    return JsonResponse(context)


def remove_cart_item(request, product_id, cart_item_id):
    cart_items = None
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            user=request.user, product=product, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=__cart_id(request))
        cart_item = CartItem.objects.get(
            cart=cart, product=product, id=cart_item_id)
    save_cart_item_id = cart_item.id
    cart_item.delete()
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user).select_related('product')
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_items = CartItem.objects.filter(
                cart=cart).select_related('product')
        for cart_item in cart_items:
            if cart_item.product.sale_price != None and cart_item.product.sale_price > 0:
                total += (cart_item.quantity*cart_item.product.sale_price)
            else:
                total += (cart_item.quantity*cart_item.product.price)
            quantity += cart_item.quantity
        tax = (10 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'cart_item_id': save_cart_item_id,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }
    from .context_processors import counter
    cart_counter = counter(request)
    context['cart_count'] = cart_counter['cart_count']
    return JsonResponse(context)


def increment_cart_item(request, product_id, cart_item_id):
    cart_items = None
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                user=request.user, product=product, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_item = CartItem.objects.get(
                cart=cart, product=product, id=cart_item_id)
        # if cart_item.quantity > 1:
        cart_item.quantity += 1
        cart_item.save()
        # else:
        #     cart_item.delete()
    except:
        pass
    context = {
        'product': product.product_name,
        'cart_item_id': cart_item.id,
        'cart_item_quantity': cart_item.quantity,
        'cart_item_sale_price': cart_item.product.sale_price,
        'cart_item_price': cart_item.product.price,
    }
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user).select_related('product')
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_items = CartItem.objects.filter(
                cart=cart).select_related('product')
        for cart_item in cart_items:
            if cart_item.product.sale_price != None and cart_item.product.sale_price > 0:
                total += (cart_item.quantity*cart_item.product.sale_price)
            else:
                total += (cart_item.quantity*cart_item.product.price)
            quantity += cart_item.quantity
        tax = (10 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context['total'] = total
    context['tax'] = tax
    context['grand_total'] = grand_total
    context['quantity'] = quantity
    from .context_processors import counter
    cart_counter = counter(request)
    context['cart_count'] = cart_counter['cart_count']
    return JsonResponse(context)


def decrement_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    check_delete = None
    cart_item_id_delete = None
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                user=request.user, product=product, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_item = CartItem.objects.get(
                cart=cart, product=product, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item_id_delete = cart_item.id
            check_delete = True
            cart_item.delete()
    except:
        pass
    context = {
        'product': product.product_name,
        'cart_item_id': cart_item.id,
        'cart_item_quantity': cart_item.quantity,
        'check_delete': check_delete,
        'cart_item_id_delete': cart_item_id_delete,
        'cart_item_sale_price': cart_item.product.sale_price,
        'cart_item_price': cart_item.product.price,
    }
    cart_items = None
    total = 0
    tax = 0
    quantity = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user).select_related('product')
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_items = CartItem.objects.filter(
                cart=cart).select_related('product')
        for cart_item in cart_items:
            if cart_item.product.sale_price != None and cart_item.product.sale_price > 0:
                total += (cart_item.quantity*cart_item.product.sale_price)
            else:
                total += (cart_item.quantity*cart_item.product.price)
            quantity += cart_item.quantity
        tax = (10 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context['total'] = total
    context['tax'] = tax
    context['grand_total'] = grand_total
    context['quantity'] = quantity
    from .context_processors import counter
    cart_counter = counter(request)
    context['cart_count'] = cart_counter['cart_count']
    return JsonResponse(context)


@login_required(login_url='register_and_login')
def checkout(request):
    total = 0
    quantity = 0
    cart_items = None
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user).select_related('product')
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_items = CartItem.objects.filter(
                cart=cart).select_related('product')
        for cart_item in cart_items:
            if cart_item.product.sale_price != None and cart_item.product.sale_price > 0:
                total += (cart_item.quantity*cart_item.product.sale_price)
            else:
                total += (cart_item.quantity*cart_item.product.price)
            quantity += cart_item.quantity
        tax = (10*total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    if cart_items.count() == 0:
        return redirect("store")
    return render(request, 'checkout.html', context)

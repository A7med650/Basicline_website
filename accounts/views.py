from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from cart.views import __cart_id

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from .forms import UserForm
from orders.models import OrderProduct, Order

# Create your views here.


def register_and_login(request):
    context = {}
    if request.method == "POST":
        if request.POST.get('login') == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            if "@" in email:
                get_username = User.objects.filter(email=email).first()
                try:
                    email = get_username.username
                except:
                    messages.error(request, 'This email does not exist.')
                    return redirect('register_and_login')
            user = auth.authenticate(username=email, password=password)
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=__cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(
                        cart=cart).exists()
                    if is_cart_item_exists:
                        cartitem = CartItem.objects.filter(cart=cart)

                        # Getting the product variations by cart_id
                        product_variation = []
                        for item in cartitem:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        # Get the cart items from user to access his product variations
                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                        for product in product_variation:
                            if product in ex_var_list:
                                index = ex_var_list.index(product)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('register_and_login')
        elif request.POST.get('register') == "Register":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            get_username = User.objects.filter(username=username).count()
            get_email = User.objects.filter(email=email).count()
            if get_username > 0:
                messages.error(request, 'Username already taken.')
                return redirect('register_and_login')
            if get_email > 0:
                messages.error(request, 'Email already taken.')
                return redirect('register_and_login')
            if len(password) < 7:
                messages.error(request, 'Password is short.')
                return redirect('register_and_login')
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            email_subject = 'Please activate your account'
            message = render_to_string('account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject, message, to=[to_email])
            send_email.send()

    return render(request, 'login.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations! Your account is activated.')
        return redirect('register_and_login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register_and_login')


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        content = request.POST.get('message')
        message = name + "\n" + email + "\n\n" + content
        print("message => ", message)

        e = EmailMessage(
            "Contact-Us",
            message,
            "am8540689@gmail.com",
            ["tefa2436@gmail.com"],
        )
        e.send()
        print("test")
        return render(request, 'contact.html')
    return render(request, 'contact.html')


@login_required(login_url='register_and_login')
def logout(request):
    auth.logout(request)
    return redirect('register_and_login')


@login_required(login_url='register_and_login')
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'account.html', context)


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            email_subject = 'Reset Your Password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject, message, to=[to_email])
            send_email.send()
            messages.success(
                request, 'Password reset email has been sent to your email address.')
            return redirect('forgotpassword')
        else:
            messages.error(request, "Account does not exist!")
            return redirect('forgotpassword')
    return render(request, 'Forget.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('register_and_login')


def resetpassword(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if len(password) < 7:
            messages.error(request, 'Password is short.')
            return redirect('resetpassword')
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('register_and_login')
        else:
            messages.error(request, 'Password do not math!')
            return redirect('resetpassword')
    else:
        return render(request, 'reset_password.html')


@login_required(login_url='register_and_login')
def edit_profile(request):
    if request.method == "POST":
        current_user = request.user
        user = User.objects.get(username=current_user)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Your profile has been updated.')
    return redirect('dashboard')


@login_required(login_url='register_and_login')
def change_password(request):
    if request.method == "POST":
        current_user = request.user
        user = User.objects.get(username=current_user)
        current_password = request.POST.get("password_current")
        new_password = request.POST.get("password_new")
        confirm_password = request.POST.get("password_confirm")
        if len(new_password) < 7:
            messages.error(request, 'Password is short.')
            return redirect("dashboard")
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('register_and_login')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect("dashboard")
        else:
            messages.error(request, 'Password do not math!')
            return redirect("dashboard")
    else:
        return redirect("dashboard")

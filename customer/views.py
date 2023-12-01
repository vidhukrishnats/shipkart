from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product
from django.contrib.auth import login, logout, authenticate, get_user_model
from .models import CustomUser
from django.db.models import Q
from .forms import  RegistrationForm, UserUpdateForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generateToken
from django.core.mail import EmailMessage
from django.conf import settings
from carts.models import Cart, CartItem
from carts.views import _cartId
import requests

def categories(request):
    return {'categories': Category.objects.all}

def allProducts(request):
    products = Product.objects.all()
    sort_option = request.GET.get('sort')
    if sort_option == 'low_to_high':
        products = products.order_by('price')
    elif sort_option == 'high_to_low':
        products =  products.order_by('-price')
    context = {'products':products}
    return render(request, 'home.html', context)

def loginPage(request):
    page = 'login'
    email = ''
    password = ''
    user = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    try:
                        cart = Cart.objects.get(cart_id=_cartId(request))
                        is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                        if is_cart_item_exists:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                    except:
                        pass
                    login(request, user)
                    url = request.META.get('HTTP_REFERER')
                    try:
                        query = requests.utils.urlparse(url).query
                        params = dict(x.split('=')for x in query.split('&'))
                        if 'next' in params:
                            nextPage = params['next']
                            return redirect(nextPage)
                    except:
                        return redirect ('allproducts')
            else:
                raise user.DoesNotExist
        except CustomUser.DoesNotExist:
            messages.error(request, "Email or Password is incorrect!")
    context = {'page':page}
    return render(request, 'login_register.html', context)

def customLogout(request):
    logout(request)
    request.session.flush()
    return redirect('allproducts')

def sendEmail(user, request):
    current_site = get_current_site(request)
    email_subject = "Activate your account."
    email_body = render_to_string('activate.html',{
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generateToken.make_token(user)
    })
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM, to=[user.email])
    email.send()

def registerUser(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            sendEmail(user, request)
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = RegistrationForm()
    return render(request=request,template_name="login_register.html",context={"form": form})

def activateUser(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except Exception as e:
        user=None
    if user and generateToken.check_token(user, token):
        user.is_email_verified = True
        user.is_staff = True
        user.is_active = True
        user.save()
        user = authenticate(request, email=user.email, password=user.password)
        if user is not None:
            login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Verification successful, you can now login!')
        return redirect('login')
    return render(request, 'activation_failed.html', {'user':user})

def productDetail(request, slug):
    product = Product.objects.get(slug=slug)
    context = {'product':product}
    return render(request, 'product.html', context)

def categoryList(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    context = {'category':category, 'products': products}
    return render(request, 'category.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created').filter(Q(description__icontains=keyword) | Q(title__icontains=keyword))
    context = {'products':products}
    return render(request, 'home.html', context)

def profile(request, username):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save(commit=False)
            form.instance.email = user.email
            form.save()
            username = form.instance.email
            messages.success(request, f'{form.instance.email}, Your profile has been updated!')
            return redirect("profile", username)
    user = get_user_model().objects.filter(email=request.user.email).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request,"profile.html",{"form": form})
    return redirect("allproducts")

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST ['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact = email)
            current_site = get_current_site(request)
            email_subject = "Reset your password."
            email_body = render_to_string('reset_password_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generateToken.make_token(user)
            })
            email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM, to=[user.email])
            email.send()
            messages.success(request, 'Password reset email has been sent successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'forgotPassword.html')

def resetPasswordValidate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generateToken.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password!')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Reset password successfull! Login.")
            return redirect('login')
        else:
            messages.error(request, 'Password do not match! Try again.')
            return redirect('reset_password')
    else:
        return render(request, 'reset_password.html')
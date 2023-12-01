from django.shortcuts import get_object_or_404, render, redirect
from customer.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required

def _cartId(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def addCart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=request.user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, user=request.user)
            cart_item.quantity += 1
        else:
            cart_item = CartItem.objects.create(product=product,quantity=1,user=request.user)
        cart_item.save()
    else:
        try:
            cart = Cart.objects.get(cart_id=_cartId(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cartId(request))
        cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product,quantity=1,cart=cart)
        cart_item.save()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_item=None, cart_items=[], tax=0, grand_total=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cartId(request))
            cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except Exception as e:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_item':cart_item,
        'cart_items':cart_items,
        'tax': tax,
        'grand_total':grand_total
    }
    return render(request, 'cart.html', context)

def removeCart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cartId(request))
            cart_items = CartItem.objects.filter(product=product, cart=cart)
        if cart_items.exists():
            cart_item = cart_items.first()
        if cart_item.quantity>1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def removeFullCartItem(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cartId(request))
        cart_items = CartItem.objects.filter(product=product, cart=cart)
    cart_items.delete()
    return redirect('cart')

@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_item=None, cart_items=[], tax=0, grand_total=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cartId(request))
            cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
    except Exception as e:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_item': cart_item,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'checkout.html', context)

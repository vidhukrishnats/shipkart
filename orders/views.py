from django.shortcuts import render, redirect
from customer.models import *
from carts.models import *
from .models import Order
from .forms import OrderForm
import datetime

def payments(request):
    return render(request, 'payments.html')

def placeOrder(request, total=0, quantity=0):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('allproducts')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address1 = form.cleaned_data['address1']
            data.address2 = form.cleaned_data['address2']
            data.pincode = form.cleaned_data['pincode']
            data.landmark = form.cleaned_data['landmark']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            context = {'order':data,'cart_items':cart_items,'total':total,'tax':tax,'grand_total':grand_total,}
            return render(request,'payments.html', context)
    else:
        return redirect('checkout')
    return render(request, 'place_order.html')

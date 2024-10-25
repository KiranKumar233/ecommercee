from django.shortcuts import render,redirect
from store.models import Wishlist, product,Cart,Order, OrderItem, profile
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse


from django.contrib import messages
import random

from django.contrib.auth.decorators import login_required

@login_required(login_url='loginpage')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_prices * item.product_qty
    userprofile = profile.objects.filter(user = request.user).first()

    context = {'cartitems':cartitems, 'total_price':total_price, 'userprofile':userprofile}
    return render(request,"checkout.html",context)




@login_required(login_url='loginpage')
def placeorder(request):
    
    if request.method == "POST":
        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name :
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()
        if not profile.objects.filter(user=request.user):
            userprofile = profile()
            userprofile.user = request.user

            userprofile.phone = request.POST.get('phone')
            userprofile.adress= request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()


        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.adress= request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = sum(item.product.selling_prices * item.product_qty for item in cart)
        neworder.total_price = cart_total_price

        # Generate a unique tracking number
        trackno = 'ORD' + str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'ORD' + str(random.randint(1111111,9999999))
        neworder.tracking_no = trackno

        neworder.save()

        for item in cart:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_prices,
                quantity=item.product_qty
            )

            # To Decrease The Product Quantity From Available Stock
            orderproduct = product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        # To Clear user's cart
        Cart.objects.filter(user=request.user).delete()

        
        
        payMode = request.POST.get('payment_mode')
        if(payMode == 'Paid by Razorpay'):
            return JsonResponse({ 'status' : "Your order has been placed successfully" })
        else:
            messages.success(request, "Your order has been placed successfully")

    return redirect('/')


@login_required(login_url='loginpage')

def razorpaycheck(request):
    cart = Cart.objects.filter(user = request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.product.selling_prices  * item.product_qty
        
    return JsonResponse({
        'total_price' : total_price
    })
    
def orders(request):
    return HttpResponse("my order page")
from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from store.models import Wishlist, product


from django.contrib import messages

from django.contrib.auth.decorators import login_required


@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request,'wishlist.html', context)

def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get("product_id"))
            product_check = product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user = request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product Already In Wishlist"})
                else:
                    Wishlist.objects.create(user = request.user, product_id = prod_id)
                    return JsonResponse({'status':"Product Added To Wishlist"})


            else:
                return JsonResponse({'status':"No Such Product Found"})

        else:
            return JsonResponse({'status' : "Login To Continue"})

    return redirect('/')

from django.core.exceptions import ObjectDoesNotExist

def deletewishlistitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            try:
                wishlist_items = Wishlist.objects.filter(user=request.user, product_id=prod_id)
                if wishlist_items.exists():
                    wishlist_items.delete()
                    return JsonResponse({'status': "Product Removed From Wishlist"})
                else:
                    return JsonResponse({'status': "Product Not Found In Wishlist"})
                
            except ObjectDoesNotExist:
                return JsonResponse({'status': "Product Not Found In Wishlist"})
        else:
            return JsonResponse({'status': "Login To Continue"})
    return redirect('/')


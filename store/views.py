from django.shortcuts import render,redirect
from django.contrib import messages
from django.http.response import JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import get_object_or_404
from .forms import ContactForm, ReviewForm, ReplyForm
from .models import Item, ContactPage, FeedbackPage,Review, category,product 
# OTP verification
import random
from django.core.mail import send_mail
from ecommercee import settings
from .models import OTP
import datetime
from django.utils import timezone



def home(request):
    trending_products = product.objects.filter(trending=1)
    context = {'trending_products':trending_products}
    return render(request, 'index.html', context)

def collections(request):
    rows = category.objects.filter(status = 0)
    return render(request, 'collections.html',{'category':rows})

def collectionsview(request,slug):
    if(category.objects.filter(slug = slug, status = 0)):
        rows = product.objects.filter(category__slug = slug)
        category_name = category.objects.filter(slug = slug).first()
        context = {'products':rows, 'category_name':category_name}
        return render(request, 'products/index.html', context)
    else:
        messages.warning(request,'No Such Category Found')
        return redirect('collections')

def productview(request, cate_slug, prod_slug):
    if (category.objects.filter(slug = cate_slug, status = 0)):

            if (product.objects.filter(slug = prod_slug, status = 0)):
                products = product.objects.filter(slug = prod_slug, status = 0).first
                context = {'products':products}
            else:
                messages.error(request, 'No Such Product Found')
                return redirect('collections')
    else:
        messages.error(request, 'No Such Category Found')
        return redirect('collections')
    return render(request, 'products/view.html', context)

def register(request):
    return render(request, 'register.html')

def productlistAjax(request):
    list_products = product.objects.filter(status = 0).values_list('name', flat = True)
    productlist = list(list_products)
    return JsonResponse(productlist, safe=False)

def searchproduct(request):
    if request.method == "POST":
        searched_term = request.POST.get('productsearch')
        # Add validation for search term length
        if len(searched_term) > 50:  # Adjust the length limit as needed
            messages.info(request, "Search term is too long")
            return redirect(request.META.get('HTTP_REFERER'))
        if searched_term.strip() == "":
            # If search term is empty, redirect back to the previous page
            return redirect(request.META.get('HTTP_REFERER'))
        # Use '__icontains' to perform a case-insensitive search on the 'meta_keywords' field
        found_products = product.objects.filter(meta_keywords__icontains=searched_term)
        if found_products.exists():
            # Render an HTML template to display search results
            return render(request, 'search_results.html', {'searched_term': searched_term, 'found_products': found_products})
        else:
            # If no products are found, return a message or redirect to a different view
            return render(request, 'no_results.html', {'searched_term': searched_term})
    # Handle GET requests or other cases
    return redirect(request.META.get('HTTP_REFERER'))

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect or render success page
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})

def add_review(request, item_id):
    item = Item.objects.get(pk=item_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.save()
            return redirect('item_detail', item_id=item_id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'item': item})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    reviews = item.review_set.all()
    return render(request, 'item_detail.html', {'item': item, 'reviews': reviews})

def about(request):
    return render(request,'aboutus.html')

def faq_page(request):
    return render(request,'faq.html')

def contact(request):
    if request.method == 'GET':
        return render(request, 'contact_form.html')
    else:
        ContactPage(
            First_Name = request.POST.get('fname'),
            Last_nName = request.POST.get('lname'),
            Email = request.POST.get('email'),
            Mobile = request.POST.get('mobile'),
            Topic = request.POST.get('topic'),
            Message = request.POST.get('message'),
        ).save()
        return render(request, 'contact_form.html')
    
def feedback(request):
    if request.method == 'GET':
        return render(request, 'feedback.html')
    else:
        FeedbackPage(
            Name = request.POST.get('name'),
            Email = request.POST.get('email'),
            Feedback = request.POST.get('message')
        ).save()
        return render (request, 'feedback_success.html')
    


def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'review_list.html', {'reviews': reviews})

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})

def reply_to_review(request, review_id):
    review = Review.objects.get(pk=review_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.save()
            return redirect('review_list')
    else:
        form = ReplyForm()
    return render(request, 'reply_to_review.html', {'form': form, 'review':review})

def product_detail_view(request, product_id):
    # Fetch reviews for the product with the given ID
    reviews = Review.objects.filter(product_id=product_id)

    return render(request, 'product_detail.html', {'reviews': reviews})

# OTP verification
def generate_otp():
    otp = str(random.randint(100000, 999999))
    return otp

def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f"Your OTP for verification is: {otp}\n Don't Share this with anyone"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def register_verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        try:
            otp_obj = OTP.objects.get(otp_code=otp_entered)
            # Check if OTP is expired
            if timezone.now() > otp_obj.expiration_time:
                # OTP has expired
                return render(request, 'verification_fail.html', {'message': 'OTP has expired. Please try again.'})
            else:
                # OTP is valid
                otp_obj.delete()  # Delete OTP entry after successful verification
                return render(request, 'register_success.html')
        except OTP.DoesNotExist:
            # OTP verification failed
            return render(request, 'verification_fail.html', {'message': 'Invalid OTP. Please try again.'})
    return render(request, 'verify_otp.html')
def register_send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = generate_otp()  # Generate OTP code
        expiration_time = timezone.now() + datetime.timedelta(minutes=5)  # Calculate expiration time
        otp_obj, created = OTP.objects.get_or_create(email=email)
        otp_obj.otp_code = otp
        otp_obj.expiration_time = expiration_time  # Assign the expiration time
        otp_obj.save()
        send_otp_email(email, otp)
        return redirect('register_verify_otp')
    return render(request, 'send_otp.html')

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Process the form submission
            # For example, you can send the reset email here
            return render(request, 'reset_password.html', {'form': form, 'validlink': True})
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form, 'validlink': False})


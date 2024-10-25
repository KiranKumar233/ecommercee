from django.db import models
from django.contrib.auth.models import User
import datetime as dt
import os

class OTP(models.Model):
    email = models.EmailField(unique=True, max_length=100)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(blank=True, null=True)
    
def get_file_path(request, filename):
        original_filename = filename
        nowtime = dt.datetime.now().strftime('%Y%m%d%H:%M:%S')
        filename = '%s%s' % (nowtime, original_filename)

        return os.path.join('uploads/', filename)

class category(models.Model):
    slug = models.CharField(max_length = 150, null = False, blank = False)
    name = models.CharField(max_length = 150, null = False, blank = False)
    image = models.ImageField(upload_to = get_file_path, null = True, blank = True)
    description =  models.TextField(max_length = 500, null = False, blank = False)
    status = models.BooleanField(default = False, help_text = '0 = default, 1=Hidden')
    trending = models.BooleanField(default = False, help_text = '0 = default, 1=Trending')
    meta_title = models.CharField(max_length = 150, null = False, blank = False)
    meta_keywords = models.CharField(max_length = 150, null = False, blank = False)
    meta_description =  models.TextField(max_length = 500, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class product(models.Model):
    category = models.ForeignKey(category, on_delete = models.CASCADE)
    slug = models.CharField(max_length = 150, null = False, blank = False)
    name = models.CharField(max_length = 150, null = False, blank = False)
    product_image = models.ImageField(upload_to = get_file_path, null = True, blank = True)
    small_description =  models.CharField(max_length = 100, null = False, blank = False)
    quantity = models.IntegerField(null = False, blank = False)
    description =  models.TextField(max_length = 500, null = False, blank = False)
    original_price = models.FloatField(null = False, blank = False)
    selling_prices = models.FloatField(null = False, blank = False)
    offer = models.CharField(max_length = 150,null = False, blank = False, default='5% off')
    status = models.BooleanField(default = False, help_text = '0 = default, 1=Hidden')
    trending = models.BooleanField(default = False, help_text = '0 = default, 1=Trending')
    tag = models.CharField(max_length = 150, null = False, blank = False)
    meta_title = models.CharField(max_length = 150, null = False, blank = False)
    meta_keywords = models.CharField(max_length = 150, null = False, blank = False)
    meta_description =  models.TextField(max_length = 500, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(product, on_delete = models.CASCADE)
    product_qty = models.IntegerField(null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(product, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    fname = models.CharField(max_length = 150, null = False)
    lname = models.CharField(max_length = 150, null = False)
    email = models.EmailField(max_length = 150, null = False)
    phone = models.CharField(max_length=100, null = False)
    adress = models.TextField(null = False)
    city = models.CharField(max_length = 150, null = False)
    state = models.CharField(max_length = 150, null = False)
    country = models.CharField(max_length = 150, null = False)
    pincode = models.IntegerField(null = False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_mode = models.CharField(max_length = 150, default='default_value')
    payment_id = models.CharField(max_length = 250, null=True)
    orderstatuses = (
       ('Pending','Pending'),
       ('Out For Shipping', 'Out For Shipping'),
       ('Completed', 'Completed'),
       ('Cancel', 'Canceled')
    )
    status = models.CharField(max_length = 150, choices=orderstatuses, default='Pending')
    message = models.TextField(null = True)
    tracking_no = models.CharField(max_length = 150, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True,)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(product, on_delete = models.CASCADE)
    price =models. FloatField(null = False)
    quantity = models.IntegerField(null = False)

    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)

class profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length = 100, null = False)
    Address = models.TextField(null = False)
    city = models.CharField(max_length = 100, null = False)
    state = models.CharField(max_length = 100, null = False)
    country= models.CharField(max_length = 100, null = False)
    pincode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return  self.user.username

class ContactPage(models.Model):
    First_Name = models.CharField(max_length = 50, null = False)
    Last_nName = models.CharField(max_length = 50, null = False)
    Email = models.EmailField(max_length = 100, null = False)
    Mobile = models.BigIntegerField()
    Topic = models.CharField(max_length = 100, null = False)
    Message = models.TextField(max_length = 300, null = False)
    Time = models.DateTimeField(auto_now = True)

class FeedbackPage(models.Model):
    Name = models.CharField(max_length = 100, null = False)
    Email = models.EmailField(max_length = 100, null = False)
    Feedback = models.TextField(max_length = 300, null = False)
    Time = models.DateTimeField(auto_now = True)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(product, related_name = 'reviews', on_delete = models.CASCADE)
    rating  = models.IntegerField(default=3)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class Reply(models.Model):
    review = models.ForeignKey(Review, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
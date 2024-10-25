"""
URL configuration for ecommercee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from store.views import contact_us
from django.conf.urls.static import static
from store .controller import authview, cart, wishlist,checkout, order
from django.contrib.auth import views as auth_views
from ecommercee import settings
from store import views, forms
from django.contrib import admin
app_name = 'store'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name = 'home'),
    path('collections',views.collections, name = 'collections'),
    path('collections/<str:slug>',views.collectionsview, name = 'collectionsview'),
    path('collections/<str:cate_slug>/<str:prod_slug>/', views.productview, name='productview'),
    path('product-list', views.productlistAjax),
    path('searchproduct', views.searchproduct, name="searchproduct"),
    path('register/',authview.register, name = 'register'),
    path('register_send_otp/', views.register_send_otp, name='register_send_otp'),
    path('register_verify_otp/', views.register_verify_otp, name='register_verify_otp'),
    path('login/',authview.loginpage, name = 'loginpage'),
    path('logout/',authview.logoutpage, name = 'logout'),
    path('add-to-cart', cart.addtocart, name = 'addtocart'),
    path('cart', cart.viewcart, name = "cart"),
    path('contact/', contact_us, name='contact_us'),
# Footer
    path('aboutus',views.about,name='aboutus'),
    path('contactus',views.contact,name='contactus'),
    path('faq',views.faq_page,name='faq'),
    path('feedback/',views.feedback,name='feedback'),
# Cart  
    path('update-cart',cart.updatecart, name = "updatecart"),
    path('delete_cart_item', cart.deleteitem, name = 'delete_cart_item'),
    path('wishlist', wishlist.index, name = "wishlist" ),
    path('add-to-wishlist',wishlist.addtowishlist,name="addtowishlis"),
    path('delete_wishlist_item', wishlist.deletewishlistitem, name = "deletewishlistitem"),
    path('checkout',checkout.index, name = "checkout"),
    path('place-order',checkout.placeorder, name = "placeorder"),
    path('proceed-to-pay', checkout.razorpaycheck),
    path('my-orders', order.index, name = 'myorders'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('view-order/<str:t_no>', order.vieworder, name= "orderview"),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('item/<int:item_id>/add_review/', views.add_review, name='add_review'),
# Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class= forms.CustomPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('login/', authview.loginpage, name = 'loginpage'),
    path('', views.review_list, name='review_list'),
    path('add/', views.add_review, name='add_review'),
    path('reply/<int:review_id>/', views.reply_to_review, name='reply_to_review'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
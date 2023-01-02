from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name="home"),
    # path('product-detail', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('checkout/', views.checkout, name='checkout'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('cancelorder/<int:id>', views.cancelorder, name = "cancelorder"),
    path('cancellationdone/<int:id>', views.cancellationdone, name = "cancellationdone"),
    path('submitrating/<int:pk>/', views.SubmitRating.as_view(), name = "submit-rating"),
    path('search', views.search, name="search"),

    # URLS FOR PRODUCT PAGES
 
    # ELECTRONICS START FROM HERE --

    # URL For mobiles
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    #URL For Laptops
    path('laptops/', views.laptops, name = 'laptops'),
    path('laptops/<slug:data>', views.laptops, name = 'laptopsdata'),

    #URL For Other Electronics
    path('electronics/', views.electronics, name = 'electronics'),
    path('electronics/<slug:data>', views.electronics, name = "electronicsdata"),

    # URL for Hearing and Music
    path('hearingandmusic/', views.hearingandmusic,  name = 'hearingandmusic'),
    path('hearingandmusic/<slug:data>', views.hearingandmusic,  name = 'hearingandmusicdata'),

    # URL for watches
    path('watches/', views.watches, name = "watches"),
    path('watches/<slug:data>', views.watches, name = "watchesdata"),


    # FOOD ITEMS FROM HERE --

    # URL for Groceries
    path('groceries/', views.groceries, name = "groceries" ),
    path('groceries/<slug:data>', views.groceries, name='groceriesdata'),

    # URL for Frozen and Chilled Food
    path('almonds/', views.almonds, name=  "almonds"),
    path('almonds/<slug:data>', views.almonds, name = "almonds"),
    
    # URL for bakery items
    path('bakeries/', views.bakeries, name  = "bakeries"),
    path('bakeries/<slug:data>', views.bakeries, name  = "bakeriesdata"),

    # URL for Restaurant Food
    path('restaurantfood/', views.restaurantfood, name = "restaurantfood"),
    path('restaurantfood/<slug:data>', views.restaurantfood, name = "restaurantfooddata"),

   
    # URL for Kashmiri Special
    path('kashmirispices/', views.kashmirispices, name  = "kashmirispices"),
    path('kashmirispices/<slug:data>', views.kashmirispices, name = "kashmirispicesdata"),



    # Fashion Items From Here

    # URL for Top Wear
    path('topwear/', views.topwear, name =  "topwear"),
    path('topwear/<slug:data>', views.topwear, name = "topweardata"),

    # URL for Bottom Wear
    path('bottomwear/', views.bottomwear, name =  "bottomwear"),
    path('bottomwear/<slug:data>', views.bottomwear, name = "bottomweardata"),

    # URL FOR KNITTED WEAR
    path('knittedwear/', views.knittedwear, name =  "knittedwear"),
    path('knittedwear/<slug:data>', views.knittedwear, name = "knittedweardata"),

    # URL for footwear
    path('footwear/', views.footwear, name =  "footwear"),
    path('footwear/<slug:data>', views.footwear, name = "footweardata"),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name="password_reset_complete"),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('about/', views.about, name = "about"),
    path('bulk/', views.bulk, name = "bulk"),
    path('privacypolicy/', views.privacypolicy, name = "privacypolicy")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

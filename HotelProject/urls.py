from django.contrib import admin
from django.urls import path,include
from account.views import SignUpView,CustomerSignUpView,HotelSignUpView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('accounts/signup/hotel/', HotelSignUpView.as_view(), name='hotel_signup'),
]
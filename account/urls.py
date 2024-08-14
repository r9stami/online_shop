from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login',views.LoginView.as_view(),name='login'),
    path('sign/up',views.SignUpView.as_view(),name='signup'),
    path('verify',views.VerifyOtpView.as_view(),name='verify'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('address/create',views.AddressCreateView.as_view(),name='address_create'),
    path('contact/us',views.ContactView.as_view(),name='contact_create'),
    path('user/profile',views.UserProfileView.as_view(),name='user_profile'),


]
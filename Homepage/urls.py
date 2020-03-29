from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.homepage , name='Homepage'),

    path('login/', views.login , name="Login" ),
    path('signup/', views.signup , name="Signup" ),
    path('Account/',include('Account.urls')),
    path('Logout/', views.logout, name="logout"),
    path('VerifyOTP', views.verifyOTP, name="VerifyOTP"),
]

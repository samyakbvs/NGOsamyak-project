from django.urls import path , include
from . import views

urlpatterns = [

    path('', views.Home , name="H" ),
    path('login/', views.login , name="Login" ),
    path('signup/', views.signup , name="Signup" ),
    path('Account/',include('Account.urls')),
    path('Logout/', views.logout, name="Logout"),
    path('VerifyOTP', views.verifyOTP, name="VerifyOTP"),
]

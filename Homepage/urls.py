from django.urls import path , include
from . import views

urlpatterns = [
    # path('', views.error , name="error" ),
    path('', views.Home , name="authHome" ),
    path('about/', views.About , name="authAbout" ),
    path('login/', views.login , name="Login" ),
    path('signup/', views.signup , name="Signup" ),
    path('Account/',include('Account.urls')),
    path('Logout/', views.logout, name="Logout"),
    path('VerifyOTP', views.verifyOTP, name="VerifyOTP"),
]

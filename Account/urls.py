from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage , name='Homepage'),
    path('Contact/', views.Contact , name='Contact'),
    path('About/', views.About, name='About'),
    path('Info/',views.Info,name='Info'),
    path('History/',views.History,name='History'),
    path('Database/',views.Database,name='Database'),
    path('Site/<int:site_id>/', views.Detail , name="detail"),
    path('Form/<int:detailSite_id>/', views.SiteForm , name="SiteForm"),
    path('ThankYou/<str:Donation_Type>/<str:CollectionId>/', views.ThankYou, name='ThankYou'),
    path('ChangeDetails/', views.changeDetails, name='ChangeDetails'),
    path('MonetaryForm/<int:detailSite_id>/', views.SiteMonetaryForm, name='SiteMonetaryForm'),
]

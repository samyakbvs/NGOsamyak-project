from django.urls import path
from . import views

urlpatterns = [
    path('Info/',views.Info,name='Info'),
    path('History/',views.History,name='History'),
    path('Database/',views.Database,name='database'),
    path('Site/<int:site_id>/', views.Detail , name="detail"),
    path('Form/<int:detailSite_id>/', views.SiteForm , name="SiteForm"),
    path('ThankYou/<str:Donation_Type>/<str:HistoryId>/<str:CollectionId>/', views.ThankYou, name='ThankYou'),
    path('ChangeDetails/<str:user_username>', views.changeDetails, name='ChangeDetails'),
    path('MonetaryForm/<int:detailSite_id>/', views.SiteMonetaryForm, name='SiteMonetaryForm'),
]

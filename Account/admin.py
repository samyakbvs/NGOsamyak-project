from django.contrib import admin
from .models import Site,Collection,MonetaryCollection,ThingsDonated,Donation
# Register your models here.

admin.site.register(Site)
admin.site.register(ThingsDonated)
admin.site.register(Collection)
admin.site.register(MonetaryCollection)
admin.site.register(Donation)

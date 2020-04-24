from django.contrib import admin
from .models import Site,Collection,MonetaryCollection,ThingsDonated
# Register your models here.

admin.site.register(Site)
admin.site.register(ThingsDonated)
admin.site.register(Collection)
admin.site.register(MonetaryCollection)

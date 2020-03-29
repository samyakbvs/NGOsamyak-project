from django.contrib import admin
from .models import Site,CreateHistory,Collection,MonetaryCollection
# Register your models here.

admin.site.register(Site)
admin.site.register(CreateHistory)
admin.site.register(Collection)
admin.site.register(MonetaryCollection)

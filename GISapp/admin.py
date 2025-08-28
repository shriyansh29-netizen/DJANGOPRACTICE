from django.contrib import admin
from .models import Feeder, DT, LocationEntry, FeederDTSelection

admin.site.register(Feeder)
admin.site.register(DT)
admin.site.register(LocationEntry)
admin.site.register(FeederDTSelection)


# Register your models here.

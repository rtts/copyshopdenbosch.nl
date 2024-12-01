from django.contrib import admin
from .models import *

@admin.register(BWPrice)
class BWPriceAdmin(admin.ModelAdmin):
    pass

@admin.register(FCPrice)
class FCPriceAdmin(admin.ModelAdmin):
    pass

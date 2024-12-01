from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe
from .models import *

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['get_order_nr', 'created', 'customer', 'total', 'status', 'assignee', 'get_checkout_url']
    list_filter = ['status', 'assignee', 'created']
    fields = ['total', 'status', 'assignee', 'customer', 'phone', 'email', 'address', 'notes']
    readonly_fields = ['total', 'status']

    def get_checkout_url(self, order):
        url = reverse('checkout', args=[order.token])
        return mark_safe(f'<a style="font-size:1.25em" href="{url}">Link</a>')
    get_checkout_url.short_description = 'link voor klant'

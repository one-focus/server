# erank_app/admin.py

from django.contrib import admin
from .models import ShopListing


@admin.register(ShopListing)
class ShopListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price']
    search_fields = ['title']
    list_filter = ['currency_code', 'currency_symbol']
    ordering = ['-last_updated']

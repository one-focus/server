# erank_app/serializers.py

from rest_framework import serializers
from .models import ShopListing


class ShopListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopListing
        fields = [
            'id',
            'last_updated',
            'title',
            'tags',
            'listing_image',
            'total_views',
            'favorites',
            'listing_age',
            'daily_view',
            'price',
            'currency_code',
            'currency_symbol',
            'orig_price',
            'est_sales_value',
            'est_sales_label',
            'est_revenue_value',
            'est_revenue_label',
            'est_conversion_rate_value',
            'est_conversion_rate_label',
        ]

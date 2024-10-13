# erank_app/models.py

from django.db import models


class ShopListing(models.Model):
    id = models.IntegerField(primary_key=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    tags = models.JSONField(default=list)
    listing_image = models.URLField(max_length=500, blank=True)
    total_views = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    listing_age = models.IntegerField(default=0)  # Assuming days
    daily_view = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    currency_code = models.CharField(max_length=10, blank=True)
    currency_symbol = models.CharField(max_length=5, blank=True)
    orig_price = models.FloatField(default=0.0)
    est_sales_value = models.IntegerField(default=0)
    est_sales_label = models.CharField(max_length=50, blank=True)
    est_revenue_value = models.FloatField(default=0.0)
    est_revenue_label = models.CharField(max_length=50, blank=True)
    est_conversion_rate_value = models.FloatField(default=0.0)
    est_conversion_rate_label = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

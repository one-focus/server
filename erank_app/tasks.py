import logging
import os

import requests
import browser_cookie3
import json
from django.conf import settings
from django.utils import timezone  # Import timezone utilities
from datetime import datetime
from .models import ShopListing

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the desired log level

# Check if the logger already has handlers to prevent duplicate logs
if not logger.handlers:
    # Define log file path
    log_directory = os.path.join(settings.BASE_DIR, 'logs')
    os.makedirs(log_directory, exist_ok=True)  # Create the log directory if it doesn't exist
    log_file = os.path.join(log_directory, 'erank.log')

    # Create a file handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)

    # Define a log format
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s:%(lineno)d %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)


def clean_int(value):
    """
    Cleans a string by removing commas and converts it to an integer.
    Returns None if conversion fails.
    """
    try:
        return int(value.replace(',', ''))
    except (ValueError, AttributeError):
        return None


def clean_float(value):
    """
    Cleans a string by removing commas and converts it to a float.
    Returns None if conversion fails.
    """
    try:
        return float(value.replace(',', ''))
    except (ValueError, AttributeError):
        return None


def fetch_erank_data(shop_name, offset=0):
    chrome_profile_path = os.path.expanduser(
        '/Users/alexandrkardash/Library/Application Support/Google/Chrome/Profile 5'
    )

    try:
        # Retrieve cookies from the specified Chrome profile
        cookies = browser_cookie3.chrome(
            cookie_file=os.path.join(chrome_profile_path, 'Cookies'),
            domain_name='erank.com'
        )
    except Exception as e:
        logger.error(f"Failed to retrieve cookies from Profile 5: {e}")
        raise RuntimeError(f"Failed to retrieve cookies from profile Profile 5: {str(e)}")

    cookie_dict = {cookie.name: cookie.value for cookie in cookies}

    # Define headers as per the cURL command
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'https://erank.com',
        'Priority': 'u=1, i',
        'Referer': f'https://erank.com/shop-info/{shop_name}',
        'Sec-CH-UA': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    # Define the payload as per the cURL command
    payload = {
        "url": f"http://api.erank.vpc/shop/listings/{shop_name}",
        "method": "GET",
        "data": {
            "shop_name": shop_name,
            "currency": "USD",
            "limit": 100,
            "offset": offset,
            "show_popular_tags": 0
        }
    }

    # Log request details for debugging
    logger.debug(f"POST URL: https://erank.com/api/shop/listings/{shop_name}")
    logger.debug(f"Headers: {headers}")
    logger.debug(f"Cookies: {cookie_dict}")
    logger.debug(f"Payload: {payload}")

    try:
        # Make the POST request to the eRank API using the json parameter
        response = requests.post(
            f'https://erank.com/api/shop/listings/{shop_name}',
            headers=headers,
            cookies=cookie_dict,
            json=payload  # Use json= instead of data=
        )
        logger.debug(f"Response Status: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")
    except requests.RequestException as e:
        logger.error(f"HTTP request failed: {e}")
        raise

    if response.status_code == 200:
        data = response.json()
        listings = data.get('data', {}).get('recent_listings', [])

        for item in listings:
            # Parse and convert fields as necessary
            try:
                naive_last_updated = datetime.strptime(item['last_updated'], '%Y-%m-%d %H:%M:%S')
                last_updated = timezone.make_aware(naive_last_updated, timezone.get_current_timezone())
            except ValueError:
                last_updated = None  # Handle or log the error as needed

            tags = item.get('tags', [])

            orig_currency_price = item.get('orig_currency_price', {})
            currency_code = orig_currency_price.get('currency_code', '')
            currency_symbol = orig_currency_price.get('symbol', '')
            orig_price = clean_float(orig_currency_price.get('price', 0))

            est_sales = item.get('est_sales', {})
            est_sales_value = clean_int(est_sales.get('value', 0))
            est_sales_label = est_sales.get('label', '')

            est_revenue = item.get('est_revenue', {})
            est_revenue_value = clean_float(est_revenue.get('value', 0))
            est_revenue_label = est_revenue.get('label', '')

            est_conversion_rate = item.get('est_conversion_rate', {})
            est_conversion_rate_value = clean_float(est_conversion_rate.get('value', 0.0))
            est_conversion_rate_label = est_conversion_rate.get('label', '')

            total_views = clean_int(item.get('total_views', 0))
            favorites = clean_int(item.get('favorites', 0))
            listing_age = clean_int(item.get('listing_age', 0))
            daily_view = clean_float(item.get('daily_view', 0.0))
            price = clean_float(item.get('price', 0.0))

            try:
                ShopListing.objects.update_or_create(
                    id=item['listing_id'],
                    defaults={
                        'last_updated': last_updated,
                        'title': item.get('title', ''),
                        'tags': tags,
                        'listing_image': item.get('listing_image', ''),
                        'total_views': total_views if total_views is not None else 0,
                        'favorites': favorites if favorites is not None else 0,
                        'listing_age': listing_age if listing_age is not None else 0,
                        'daily_view': daily_view if daily_view is not None else 0.0,
                        'price': price if price is not None else 0.0,
                        'currency_code': currency_code,
                        'currency_symbol': currency_symbol,
                        'orig_price': orig_price if orig_price is not None else 0.0,
                        'est_sales_value': est_sales_value if est_sales_value is not None else 0,
                        'est_sales_label': est_sales_label,
                        'est_revenue_value': est_revenue_value if est_revenue_value is not None else 0.0,
                        'est_revenue_label': est_revenue_label,
                        'est_conversion_rate_value': est_conversion_rate_value if est_conversion_rate_value is not None else 0.0,
                        'est_conversion_rate_label': est_conversion_rate_label,
                    }
                )
            except Exception as e:
                logger.error(f"Failed to update/create ShopListing for listing_id {item.get('listing_id')}: {str(e)}")
    else:
        logger.error(f"Failed to fetch data from eRank: {response.status_code} {response.text}")
        raise Exception(f"Failed to fetch data from eRank: {response.status_code} {response.text}")

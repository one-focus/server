# ai_app/views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from g4f.client import Client
import browser_cookie3
from asgiref.sync import sync_to_async


# Optional: Function to get cookies from browser
def get_browser_cookies(domain):
    try:
        cj = browser_cookie3.load(domain_name=domain)
        cookies_dict = {cookie.name: cookie.value for cookie in cj}
        return cookies_dict
    except Exception as e:
        print(f"Error loading cookies: {e}")
        return {}


# AI processing function (async)
async def process_text_with_ai(model, text, cookies=None):
    try:
        client = Client()
        response = await sync_to_async(client.chat.completions.create)(
            model=model,
            messages=[{"role": "user", "content": text}],
            cookies=cookies,  # Optionally include cookies
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)


@csrf_exempt
async def ai_endpoint(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        text = data.get('text', '')
        model = data.get('model', 'gpt-3.5-turbo')  # Default to gpt-3.5-turbo
        use_browser_cookies = data.get('use_browser_cookies', False)

        # Get cookies if use_browser_cookies is set to True
        cookies = None
        if use_browser_cookies:
            cookies = get_browser_cookies(".openai.com")  # Adjust domain as needed

        # Process the text with selected AI model
        ai_response = await process_text_with_ai(model, text, cookies)

        return JsonResponse({'response': ai_response})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

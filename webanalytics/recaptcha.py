import requests
from django.conf import settings

def verify_recaptcha(token):
    """ Verifies reCAPTCHA token with Google """
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token
    }
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get('success', False)
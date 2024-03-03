# utils.py

import requests
from django.conf import settings

def send_sms_via_textbelt(to, message):
    response = requests.post('https://textbelt.com/text', {
        'phone': to,
        'message': message,
        'key': settings.TEXTBELT_API_KEY,
    })
    return response.json()

def format_number_for_sms(number):
    return '+1' + number.translate(str.maketrans('', '', '()- '))
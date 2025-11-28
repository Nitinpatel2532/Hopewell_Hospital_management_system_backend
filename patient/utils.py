import random
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import Emailotp
import requests

def generate_otp():
    return str(random.randint(100000, 999999))

def create_otp(user):
    otp_code = generate_otp()
    expiry = timezone.now() + timedelta(minutes=5)
    Emailotp.objects.create(user=user, otp=otp_code, valid_untill=expiry)
    return otp_code

def send_otp_email(user, otp_code):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {"name": "Hopewell Hospital", "email": settings.DEFAULT_FROM_EMAIL},
        "to": [{"email": user.Email, "name": user.First_name}],
        "subject": "Hopewell Hospital OTP Verification",
        "htmlContent": f"""
            <p>Hello {user.First_name},</p>
            <p>Your OTP is <strong>{otp_code}</strong>.</p>
            <p>It will expire in 5 minutes.</p>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Optional: Debugging print (remove later)
    print("Brevo Response:", response.status_code, response.text)

    return response.status_code == 201

import random
from django.utils import timezone
from datetime import timedelta

from .models import Emailotp
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(random.randint(100000,999999))

def create_otp(user):
    otp_code=generate_otp()
    expiry=timezone.now()+timedelta(minutes=5)
    otp_obj=Emailotp.objects.create(user=user, otp=otp_code, valid_untill=expiry)
    return otp_code

def send_otp_email(user, otp_code):
    subject = "COMPANY NAME"
    message = f'Your OTP is {otp_code}'
    email_from = settings.EMAIL_HOST_USER   # ✅ correct
    recipient_list = [user.Email]

    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False  # Important for debugging
    )


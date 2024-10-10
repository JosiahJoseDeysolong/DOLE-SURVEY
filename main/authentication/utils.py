import pyotp
from datetime import timedelta
from django.utils import timezone
from emails.utils import send_custom_email
from django.contrib.auth.models import User

def send_otp(request):
    otp_secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(otp_secret_key, interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = otp_secret_key
    valid_date = timezone.now() + timedelta(seconds=60)
    request.session['otp_valid_date'] = valid_date.isoformat()
    request.session['otp'] = otp
    username = request.session.get('username')

    try:
        user = User.objects.get(username=username)
        user_email = user.email
        subject = "Your One-Time Password (OTP)"
        message = f"{user.username}, Your one-time password is {otp}. It will expire in 60 seconds."
        send_custom_email(subject, message, user_email)
    except User.DoesNotExist:
        print("User does not exist or email not found.")

    print(f"Your one-time password is {otp}")

def has_role(user, allowed_roles):
    if hasattr(user, 'profile') and user.profile.role in allowed_roles:
        return True
    return False

def is_superuser(user):
    return user.is_superuser
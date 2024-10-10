from django.core.mail import send_mail

def send_custom_email(subject, message, to_email):
    send_mail(
        subject,
        message,
        'apollowebsiteojt@gmail.com',
        [to_email],
        fail_silently=False,
    )

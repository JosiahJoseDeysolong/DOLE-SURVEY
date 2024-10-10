from django.shortcuts import render
from .utils import send_custom_email

def email_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        to_email = request.POST.get('to_email')
        
        send_custom_email(subject, message, to_email)
        
        return render(request, 'index.html')
    return render(request, 'email_form.html')

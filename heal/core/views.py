from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage 
from django.conf import settings
from .models import Service

def services(request):
    services = Service.objects.all()  # Fetch all services from the database
    return render(request, 'services.html', {'services': services})



# Create your views here.
def home(request):
    user = request.user if request.user.is_authenticated else None
    return render(request, 'landing.html', {'user': user})

def send_mail_to_admin(user_name, user_email, mobile_number, subject, enquiry, user_message):
    # Update the message body to include the enquiry field
    message_body = (
        f"Form filled by {user_name}--- with the email {user_email}.\n\n"
        f"Mobile number -- {mobile_number}\n\n"
        f"Selected Enquiry: {enquiry}\n\n"
        f"The Message provided is:\n{user_message}"
    )

    # Create and send the email
    message = EmailMessage(
        subject=f"New form filled by {user_name}--- with subject {subject}",
        body=message_body,
        from_email=settings.EMAIL_HOST_USER,
        to=['himanshusinghwork365@gmail.com']
    )
    message.send()


def contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        subject = request.POST.get('subject')
        enquiry =request.POST.get('enquiry')
        user_message = request.POST.get('message')
        
        
        send_mail_to_admin(user_name, user_email, mobile_number, subject, enquiry, user_message)
        return redirect('home')
    else:
        return render(request, 'landing.html')


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import EmailMessage 
from django.conf import settings
from .models import Service
from django.shortcuts import render, get_object_or_404
from .models import Booking
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Verified
from .utils import *
import uuid
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
        return render(request, 'contact.html')



# Register view
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if username is already taken
        if User.objects.filter(username=uname).exists():
    # Check if the username is associated with an unverified user
            existing_user_by_username = User.objects.filter(username=uname).first()
            if existing_user_by_username:
                verified_obj = Verified.objects.filter(user=existing_user_by_username).first()
                if verified_obj and not verified_obj.is_verified:
            # Delete unverified user
                    existing_user_by_username.delete()
                else:
                    messages.error(request, "Username already exists!")
                    return redirect('register')

# Check if the email is registered and verified
        existing_user_by_email = User.objects.filter(email=email).first()
        if existing_user_by_email:
            verified_obj = Verified.objects.filter(user=existing_user_by_email).first()
            if verified_obj and verified_obj.is_verified:
                messages.error(request, "Email already exists!")
                return redirect('register')
            else:
        # Delete unverified user
                existing_user_by_email.delete()
        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Your password and confirm password are not the same!")
            return redirect('register')

        # Validate password strength
        try:
            validate_password(pass1)  # Raises ValidationError for weak passwords
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect('register')

        # Save the User object but keep it inactive
        my_user = User(
            username=uname,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=False  # User is inactive by default
        )
        my_user.set_password(pass1)
        my_user.save()

        # Create Verified object
        v_obj = Verified.objects.create(
            user=my_user,
            email_token=str(uuid.uuid4())
        )

        # Send email token
        send_email_token(email, v_obj.email_token)

        return render(request, 'verify_email.html')

    else:
        return render(request, 'signup.html')

        

def verify(request, token):
    try:
        obj = Verified.objects.get(email_token=token)
        obj.is_verified = True
        obj.save()

        # Activate the user
        obj.user.is_active = True
        obj.user.save()

        messages.success(request, "Your account has been created successfully!")
        return redirect('login')
    except Verified.DoesNotExist:
        messages.error(request, "Invalid or expired token.")
        return redirect('register')

        

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Check if user exists
        if user is None:
            messages.error(request, "Invalid UserName or Password.")
        else:
            # User exists, check password
            if user.check_password(password):
                # Password is correct, log in user
                auth.login(request, user)
                return redirect('home')
            else:
                # Incorrect password
                messages.error(request, "Invalid UserName or Password.")


    return render(request, 'login.html')

# Logout view
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile(request):
    bookings = request.user.bookings.all()  # Get all bookings linked to the logged-in user
    user = request.user if request.user.is_authenticated else None
    con = {
        'bookings': bookings,
        'user': user,
    }
    return render(request, 'profile.html', con)




from django.shortcuts import render, get_object_or_404
from .models import Service
@login_required(login_url='login')
def booksession(request, service_id):
    # Retrieve the specific service using service_id or return 404 if not found
    service = get_object_or_404(Service, id=service_id)
    
    # Get user details (ensure user is authenticated)
    user = request.user if request.user.is_authenticated else None

    # Pass the user and service details to the template
    context = {
        'service': service,
        'user': user,
    }
    return render(request, 'booking.html', context)





@login_required(login_url='login')
def book_session(request, service_id):
    service = get_object_or_404(Service, id=service_id)




    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        terms_accepted = request.POST.get('terms') == 'on'  # Checkbox value

        # Validate data (optional but recommended)
        if not all([first_name, last_name, email, phone, gender, dob, age]):
            messages.error(request, "All fields are required.")
            return redirect('book_session')

        if not terms_accepted:
            messages.error(request, "You must accept the terms and conditions.")
            return redirect('book_session')

        # Save the booking
        Booking.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender,
            date_of_birth=dob,
            age=int(age),
            terms_accepted=terms_accepted,
            # Service details
            service_title=service.title,
            service_price=service.price,
            service_duration=service.duration,
            service_mode=service.mode_of_service,
            service_location=service.location,
            service_instructor=service.instructor,
            service_date_from=service.from_date,
            service_date_to=service.to_date,
            service_time_from=service.time_from,
            service_time_to=service.time_to,
        )

        messages.success(request, "Booking successfully created!")
        return redirect('home')  # Redirect to booking history

    return render(request, 'book_session.html')


def is_admin(user):
    return user.is_superuser
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    query = request.GET.get('query')
    users = User.objects.filter(
        Q(username__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
    ) if query else None

    # Check if no users are found
    no_users_found = False
    if query and not users:
        no_users_found = True
        messages.info(request, "No users found matching your search criteria.")

    context = {
        'users': users,
        'no_users_found': no_users_found,
        'services': Service.objects.all()
    }
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    bookings = Booking.objects.filter(user=user)

    context = {
        'user': user,
        'bookings': bookings,
    }
    return render(request, 'user_detail.html', context)



# @login_required(login_url='login')
# @user_passes_test(is_admin)

# def manage_services(request):
#     message = None
#     if request.method == "POST":
#         action = request.POST.get("action")
#         try:
#             if action == "add":
#                 # Add a new service
#                 service = Service(
#                     title=request.POST.get("title"),
#                     description=request.POST.get("description"),
#                     duration=request.POST.get("duration"),
#                     mode_of_service=request.POST.get("mode_of_service"),
#                     from_date=request.POST.get("from_date"),
#                     to_date=request.POST.get("to_date"),
#                     time_from=request.POST.get("time_from"),
#                     time_to=request.POST.get("time_to"),
#                     location=request.POST.get("location"),
#                     instructor=request.POST.get("instructor"),
#                     price=request.POST.get("price"),
#                 )
#                 if 'image' in request.FILES:
#                     service.image = request.FILES['image']
#                 service.save()
#                 message = "Service added successfully!"

#             elif action == "edit":
#                 # Edit an existing service
#                 service_id = request.POST.get("service_id")
#                 service = get_object_or_404(Service, id=service_id)
#                 service.title = request.POST.get("title")
#                 service.description = request.POST.get("description")
#                 service.duration = request.POST.get("duration")
#                 service.mode_of_service = request.POST.get("mode_of_service")
#                 service.from_date = request.POST.get("from_date")
#                 service.to_date = request.POST.get("to_date")
#                 service.time_from = request.POST.get("time_from")
#                 service.time_to = request.POST.get("time_to")
#                 service.location = request.POST.get("location")
#                 service.instructor = request.POST.get("instructor")
#                 service.price = request.POST.get("price")
#                 if 'image' in request.FILES:
#                     service.image = request.FILES['image']
#                 service.save()
#                 message = "Service updated successfully!"

#             elif action == "delete":
#                 # Delete a service
#                 service_id = request.POST.get("service_id")
#                 service = get_object_or_404(Service, id=service_id)
#                 service.delete()
#                 message = "Service deleted successfully!"

#             else:
#                 message = "Invalid action."

#         except Exception as e:
#             message = f"An error occurred: {str(e)}"

#     services = Service.objects.all()
#     return render(request, 'manage_services.html', {'services': services, 'message': message})




@login_required(login_url='login')
@user_passes_test(is_admin)
def manage_services(request):
    """View to display all services"""
    services = Service.objects.all()
    return render(request, 'manage_services.html', {'services': services})

@login_required(login_url='login')
@user_passes_test(is_admin)
def add_service(request):
    """View to add a new service"""
    if request.method == "POST":
        try:
            service = Service(
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                duration=request.POST.get("duration"),
                mode_of_service=request.POST.get("mode_of_service"),
                from_date=request.POST.get("from_date"),
                to_date=request.POST.get("to_date"),
                time_from=request.POST.get("time_from"),
                time_to=request.POST.get("time_to"),
                location=request.POST.get("location"),
                instructor=request.POST.get("instructor"),
                price=request.POST.get("price"),
            )
            if 'image' in request.FILES:
                service.image = request.FILES['image']
            service.save()
            messages.success(request, "Service added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return redirect('manage_services')

# @login_required(login_url='login')
# @user_passes_test(is_admin)
# def edit_service(request, service_id):
#     """View to edit an existing service"""
#     service = get_object_or_404(Service, id=service_id)
#     if request.method == "POST":
#         try:
#             service.title = request.POST.get("title")
#             service.description = request.POST.get("description")
#             service.duration = request.POST.get("duration")
#             service.mode_of_service = request.POST.get("mode_of_service")
#             service.from_date = request.POST.get("from_date")
#             service.to_date = request.POST.get("to_date")
#             service.time_from = request.POST.get("time_from")
#             service.time_to = request.POST.get("time_to")
#             service.location = request.POST.get("location")
#             service.instructor = request.POST.get("instructor")
#             service.price = request.POST.get("price")
#             if 'image' in request.FILES:
#                 service.image = request.FILES['image']
#             service.save()
#             messages.success(request, "Service updated successfully!")
#         except Exception as e:
#             messages.error(request, f"An error occurred: {str(e)}")
#     return redirect('manage_services')

@login_required(login_url='login')
@user_passes_test(is_admin)
def delete_service(request, service_id):
    """View to delete a service"""
    service = get_object_or_404(Service, id=service_id)
    try:
        service.delete()
        messages.success(request, "Service deleted successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('manage_services')

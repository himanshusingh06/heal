from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model
from datetime import time, date


class Verified(models.Model):
    user =models.OneToOneField(User ,on_delete=models.CASCADE)
    email_token =models.CharField(max_length=200)
    is_verified =models.BooleanField(default=False)

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=100, default="60 mins")  # Default duration
    mode_of_service = models.CharField(max_length=100, default="Online")  # Default mode
    image = models.ImageField(upload_to='services/', null=True, blank=True)  # Allow blank for existing records
    from_date = models.DateField(default=date.today)  # Default to current date
    to_date = models.DateField(default=date.today)  # Default to current date
    time_from = models.TimeField(default=time(9, 0))  # Default start time (e.g., 09:00 AM)
    time_to = models.TimeField(default=time(17, 0))  # Default end time (e.g., 05:00 PM)
    location = models.CharField(max_length=255, default="Online")  # Default location
    instructor = models.CharField(max_length=255, default="Not Assigned")  # Default instructor
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')  # Link booking to user
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    terms_accepted = models.BooleanField(default=False)

     # Service details
     # Service details with default values
    service_title = models.CharField(max_length=100, default='Default Service Title')
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_duration = models.CharField(max_length=50, default='1 hour')
    service_mode = models.CharField(max_length=50, default='Online')
    service_location = models.CharField(max_length=200, default='Default Location')
    service_instructor = models.CharField(max_length=100, default='Default Instructor')
    service_date_from = models.DateField(default='2024-01-01')
    service_date_to = models.DateField(default='2024-01-02')
    service_time_from = models.TimeField(default='09:00:00')
    service_time_to = models.TimeField(default='10:00:00')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service_title} - {self.created_at}"


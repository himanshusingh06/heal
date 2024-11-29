from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    mode_of_service = models.CharField(max_length=100)
    image = models.ImageField(upload_to='services/')
    date = models.DateField()  # To specify service date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

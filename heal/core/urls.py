from django.contrib import admin
from django.urls import path
from core import views
urlpatterns = [
    path('', views.home, name='home'),
    path('contact',views.contact,name='contact'),
    # path('about/',views.AboutPage,name='about'),
   
]
from django.contrib import admin
from django.urls import path
from core import views
urlpatterns = [
    path('', views.home, name='home'),
    path('contact',views.contact,name='contact'),
    path('services',views.services,name='services'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('services/booknow/<int:service_id>/', views.booksession, name='booksession'),
    path('book-session/<int:service_id>', views.book_session, name='book_session'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('manage-services/', views.manage_services, name='manage_services'),
    path('manage-services/add/', views.add_service, name='add_service'),
    # path('manage-services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('manage-services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('verify/<str:token>', views.verify, name='verify'),

]
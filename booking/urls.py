from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.view_slots,name='view_slots'),
    path('book/<int:slot_id>/',views.book_slot,name='book_slot'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:slot_id>/', views.cancel_booking, name='cancel_booking'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
]
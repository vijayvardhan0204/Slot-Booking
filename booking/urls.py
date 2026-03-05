from django.urls import path
from . import views

urlpatterns = [
    path('',views.view_slots,name='view_slots'),
    path('book/<int:slot_id>/',views.book_slot,name='book_slot'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:slot_id>/', views.cancel_booking, name='cancel_booking'),
]
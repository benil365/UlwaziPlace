# hotel/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room/<int:room_id>/book/', views.book_room, name='book_room'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('dashboard/', views.dashboard, name='dashboard'),
     path('signup/', views.signup, name='signup'),
     path('room_list',views.room_list, name='room_list'),
]

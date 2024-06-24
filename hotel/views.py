from django.shortcuts import render
# hotel/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Booking, Payment
from .forms import BookingForm
import stripe
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})

def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'room_detail.html', {'room': room})

def room_list(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'room_list.html', {'room': room})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def book_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm(initial={'room': room})
    return render(request, 'booking_form.html', {'form': form})

@login_required
def payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        token = request.POST['stripeToken']
        charge = stripe.Charge.create(
            amount=int(booking.room.price * 100),
            currency='usd',
            description=f'Booking for {booking.room.name}',
            source=token,
        )
        Payment.objects.create(
            user=request.user,
            amount=booking.room.price
        )
        booking.checked_in = True
        booking.save()
        return redirect('dashboard')
    return render(request, 'payment_form.html', {'booking': booking, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'bookings': bookings})

# Create your views here.

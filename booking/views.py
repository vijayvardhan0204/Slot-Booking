'''This imports two useful Django functions:

render() → used to send data to an HTML template and display a webpage

redirect() → used to redirect the user to another page (not used in this function yet)'''

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from .forms import RegisterForm
from .models import Slot

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect("/")
            except IntegrityError:
                form.add_error("email", "An account with this email already exists.")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('/login/')

@login_required
def view_slots(request):
    slots = Slot.objects.all().order_by("date", "time")
    return render(request,"slots.html",{"slots":slots})

@login_required
def book_slot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)

    if slot.is_booked:
        return render(request, "error.html", {"message": "Slot already booked!"})

    if request.method == "POST":
        name = request.user.get_full_name() or request.user.username

        slot.is_booked = True
        slot.booked_by = name
        slot.save()
        
        return redirect("/")
    
    return render(request, "book.html", {"slot": slot})



@login_required
def my_bookings(request):
    display_name = request.user.get_full_name() or request.user.username
    bookings = Slot.objects.filter(Q(booked_by=request.user.username) | Q(booked_by=display_name))
    return render(request, "my_bookings.html", {"bookings": bookings})


@login_required
def cancel_booking(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)
    display_name = request.user.get_full_name() or request.user.username

    # Only the user who booked can cancel
    if slot.booked_by in [request.user.username, display_name]:
        slot.is_booked = False
        slot.booked_by = None
        slot.save()

    return redirect('my_bookings')

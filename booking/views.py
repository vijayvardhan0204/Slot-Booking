'''This imports two useful Django functions:

render() → used to send data to an HTML template and display a webpage

redirect() → used to redirect the user to another page (not used in this function yet)'''

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import Slot

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    else:
        form = UserCreationForm()

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
        name = request.user.username

        slot.is_booked = True
        slot.booked_by = name
        slot.save()
        
        return redirect("/")
    
    return render(request, "book.html", {"slot": slot})



@login_required
def my_bookings(request):
    bookings = Slot.objects.filter(booked_by=request.user.username)
    return render(request, "my_bookings.html", {"bookings": bookings})


@login_required
def cancel_booking(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)

    # Only the user who booked can cancel
    if slot.booked_by == request.user.username:
        slot.is_booked = False
        slot.booked_by = None
        slot.save()

    return redirect('my_bookings')
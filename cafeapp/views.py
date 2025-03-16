from django.shortcuts import render, redirect
from cafeapp.models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')

def starter(request):
    return render(request, 'starter-page.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')

def booking(request):
    if request.method == "POST":
        mybooking =Booking(
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            date = request.POST['date'],
            number = request.POST['people'],
            message = request.POST['message']
        )

        mybooking.save()
        return redirect('/booking')

    else:
        return render(request,'booking.html')

def chefs(request):
    return render(request, 'chefs.html')

def contact(request):
    if request.method == "POST":
        mycontact =Contact(
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            message = request.POST['message']
        )

        mycontact.save()
        return redirect('/contact')

    else:
        return render(request,'contact.html')

def events(request):
    return render(request, 'events.html')

def gallery(request):
    return render(request, 'gallery.html')


def specials(request):
    return render(request, 'specials.html')

def testimonials(request):
    return render(request, 'testimonials.html')

def whyus(request):
    return render(request, 'whyus.html')
import json
from pyexpat.errors import messages

import requests
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


from cafeapp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from cafeapp.models import *
from requests.auth import HTTPBasicAuth





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
        return redirect('/show')

    else:
        return render(request,'booking.html')


def editbookinginfo(request,id):
    editbooking = get_object_or_404(Booking,id=id)
    if request.method == 'POST':
        editbooking.name = request.POST.get('name')
        editbooking.email = request.POST.get('email')
        editbooking.phone = request.POST.get('phone')
        editbooking.date = request.POST.get('date')
        editbooking.number = request.POST.get('people')
        editbooking.message = request.POST.get('message')
        editbooking.save()
        return redirect('/show')

    else:
        return render(request,'edit-booking.html',{'editbooking':editbooking})

def deletebooking(request,id):
  deletedbooking = Booking.objects.get(id=id)
  deletedbooking.delete()
  return redirect ('/show')

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

def show(request):
    all = Booking.objects.all()
    return render(request,'show.html',{'all':all})

def events(request):
    return render(request, 'events.html')

def gallery(request):
    return render(request, 'gallery.html')


def specials(request):
    return render(request, 'specials.html')

def login(request):
    return render(request, 'login.html')

def registration(request):
    return render(request, 'registration.html')



def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        confirm_password = request.POST['confirm_password']


        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('/login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('/home')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')




#Mpesa API
def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Apen Softwares",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        # Parse response
        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")  # 0 is success, 1 is failure

        # Save transaction to database
        transaction = Transaction(
            phone_number=phone,
            amount=amount,
            transaction_id=transaction_id,
            status="Success" if result_code == "0" else "Failed"
        )
        transaction.save()

        return HttpResponse(
            f"Transaction ID: {transaction_id}, Status: {'Success' if result_code == '0' else 'Failed'}")


def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})
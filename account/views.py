from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .decorators import customer_required,hotel_required
from .forms import  CustomerSignUpForm,HotelSignUpForm

from django.views.generic import TemplateView
from .models import User,HotelNameList,Room,Reservation,BookingInfo

from django.db.models import Q

#import django_filters

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customers:Customer_Home')


class HotelSignUpView(CreateView):
    model = User
    form_class = HotelSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'hotel'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('hotels:Hotel_Home')


def home(request):
    if request.user.is_authenticated:
        if request.user.is_hotel:
            return redirect('hotels:Hotel_Home')
        else:
            return redirect('customers:Customer_Home')
    return render(request, 'temp/home.html')

### Customer Functions

@login_required
@customer_required
def Customer_Home(request):
    username = request.user.username
    if request.method == 'POST':
        city = request.POST['city']
        check_in= request.POST['check_in']
        check_out = request.POST['check_out']
        people = request.POST['people']

        rooms = Room.objects.filter(Q(city = city) & Q(number_of_people__gte = people))

        avi_room = []    # list of rooms that is avilable as per users filter

        for room in rooms:

            case_1 = Reservation.objects.filter(room=room, check_in__lte=check_in, check_out__gte=check_in).exists()

            case_2 = Reservation.objects.filter(room=room, check_in__lte=check_out, check_out__gte=check_out).exists()
            
            case_3 = Reservation.objects.filter(room=room, check_in__gte=check_in, check_out__lte=check_out).exists()


            if case_1 or case_2 or case_3:
                print("NO room avilable this days")
            else:
                avi_room.append(room)
        
        totalrooms = len(avi_room)

        if totalrooms==0:
            return render(request, 'temp/customer/home1.html',{"username":username,"message":"No Rooms avilable as per your filter search Sorry !!","totalrooms":totalrooms})
        else:
            return render(request, 'temp/customer/home1.html',{"username":username,"rooms":avi_room,"totalrooms":totalrooms,"message":"Rooms Avilable as per filter search result !!"})

    else:
        rooms=Room.objects.all()
        totalrooms = rooms.count()
        sta = request.user.is_customer
        return render(request, 'temp/customer/home1.html',{"username":username,"rooms":rooms,"totalrooms":totalrooms,"role":sta})


@login_required
@customer_required
def BookRoom(request,i_id):
    pk=i_id
    room = Room.objects.get(pk = pk)   #get the room
    hotel_id = room.hotel_id
    hotel = HotelNameList.objects.get(hotel_id = hotel_id)
    hotel_name = hotel.hotel_name
    if request.method == 'POST':
        #invalid_dates = False
        fullname = request.POST['fullname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        check_in= request.POST['check_in']
        check_out = request.POST['check_out']

        case_1 = Reservation.objects.filter(room=room, check_in__lte=check_in, check_out__gte=check_in).exists()

        case_2 = Reservation.objects.filter(room=room, check_in__lte=check_out, check_out__gte=check_out).exists()
            
        case_3 = Reservation.objects.filter(room=room, check_in__gte=check_in, check_out__lte=check_out).exists()


        # if either of these is true, abort and render the error
        if case_1 or case_2 or case_3:
                return render(request, "temp/customer/bookroom.html", {"errors": "This room is not available on your selected dates","room":room,"hotel_name":hotel_name})                  
             
        # dates are valid
        reservation = Reservation(
        check_in = check_in, 
        check_out = check_out,
        room = room,
        guest = request.user
        )

        reservation.save()

        Booking = BookingInfo(
            fullname = fullname,
            email = email,
            mobile = mobile,
            customer = request.user,
            room = room
        )

        Booking.save()


        #redirect to success page (need to define this as a separate view)
        return render(request, "temp/customer/bookroom.html", {"sucess":"room sucessfully registered Thank You","room":room,"hotel_name":hotel_name})

    else:
        return render(request, 'temp/customer/bookroom.html',{"room":room,"hotel_name":hotel_name})



### Hotel Functions 


@login_required
@hotel_required
def Hotel_Home(request):
    added=False
    HotelName=""
    if request.method == 'POST':
        x = request.POST['content']
        new_item = HotelNameList(hotel_name = x,added = True,hotel_id=request.user)
        added = True
        new_item.save()
        HotelName=str(x)

    else:
        if HotelNameList.objects.filter(hotel_id=request.user).exists():
            added=True
            obj = HotelNameList.objects.get(hotel_id=request.user)
            HotelName = obj.hotel_name
        else:
            added = False

    username = request.user.username
    return render(request, 'temp/hotel/home2.html',{"username":username,"hotelname":HotelName,"added":added})


@login_required
@hotel_required
def AddRoom(request):
    obj = HotelNameList.objects.get(hotel_id=request.user)
    HotelName = obj.hotel_name
    if request.method == 'POST':
        name = request.POST['roomname']
        price = request.POST['roomprice']
        people = request.POST['people']
        desc = request.POST['desc']
        city = request.POST['city']
        
        new_room = Room(name=name,price=price,number_of_people=people,desc=desc,hotel_id=request.user)
        new_room.save()
        message = "Room Added Succesfully"
    else:
        message = "ADD ROOM NOW"
    return render(request, 'temp/hotel/addroom.html',{"message":message,"hotelname":HotelName})


@login_required
@hotel_required
def ViewRoom(request):
    obj = HotelNameList.objects.get(hotel_id=request.user)
    HotelName = obj.hotel_name
    rooms = Room.objects.filter(hotel_id=request.user)
    total=rooms.count()
    return render(request, 'temp/hotel/viewroom.html',{"room":rooms,"totalrooms":total,"hotelname":HotelName})


def EditRoom(request,i_id):
    pk=i_id
    room = Room.objects.get(pk = pk)
    name = room.name
    price = room.price
    city = room.city
    people = room.number_of_people
    desc = room.desc

    if request.method == 'POST':
        name = request.POST['roomname']
        price = request.POST['roomprice']
        people = request.POST['people']
        desc = request.POST['desc']
        city = request.POST['city']
        room.name = name
        room.price = price
        room.city = city
        room.number_of_people = people
        room.desc = desc

        room.save()

        return redirect('hotels:viewroom')

    else:
        return render(request,'temp/hotel/editroom.html',{"name":name,"price":price,"city":city,"people":people,"desc":desc})



@login_required
@hotel_required
def BookingInfo(request):
    user = request.user
    all_reservations = Reservation.objects.all()
    li = []
    for i in all_reservations:
        roomm = i.room
        if roomm.hotel_id == user:
            li.append(i)
    message = " ROOMS BOOKED TILL NOW"
    n=len(li)
    if n == 0:
        message = "NO ROOM BOOKED YET"
    return render(request,'temp/hotel/bookinginfo.html',{"message":message,"rooms":li,"booked":n})
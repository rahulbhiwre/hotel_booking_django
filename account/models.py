from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from pytz import timezone
from django.utils import timezone
#import django_filters

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_hotel = models.BooleanField(default=False)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=20,default="")

    def __str__(self):
        return self.user.username

class HotelNameList(models.Model):
    hotel_name = models.CharField(max_length=20,default="")
    added = models.BooleanField(default=False)
    hotel_id = models.ForeignKey(User,on_delete=models.CASCADE)

class Room(models.Model):
   name = models.CharField(max_length = 200)
   desc = models.TextField()
   price = models.IntegerField()
   is_reserved = models.BooleanField(default=False)
   number_of_people = models.PositiveIntegerField()
   hotel_id = models.ForeignKey(User,on_delete=models.CASCADE)
   city = models.CharField(max_length = 30,default="")
   #reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL)


   def __str__(self):
       return self.name

   class Meta:
       verbose_name = 'Room'
       verbose_name_plural = 'Rooms'


class Reservation(models.Model):
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    guest = models.ForeignKey(User, on_delete= models.CASCADE)

    class Meta:
       verbose_name = 'Reservation'
       verbose_name_plural = 'Reservations'



class BookingInfo(models.Model):
    fullname = models.CharField(max_length = 200)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length = 13)
    customer = models.ForeignKey(User, on_delete= models.CASCADE,default="")
    room = models.ForeignKey(Room, on_delete = models.CASCADE,default="")
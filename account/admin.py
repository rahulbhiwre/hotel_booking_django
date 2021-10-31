from django.contrib import admin

from .models import Customer

admin.site.register(Customer)

from .models import User

admin.site.register(User)

from .models import HotelNameList

admin.site.register(HotelNameList)

from .models import Room

admin.site.register(Room)

from .models import Reservation

admin.site.register(Reservation)


from .models import BookingInfo

admin.site.register(BookingInfo)
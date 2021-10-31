from django.urls import include, path
from .views import Hotel_Home,Customer_Home,home,AddRoom,ViewRoom,BookRoom,EditRoom,BookingInfo

urlpatterns = [
    path('', home, name='home'),
    path('customers/', include(([
    path('', Customer_Home, name='Customer_Home'),
    path('bookroom/<i_id>', BookRoom, name='bookroom'),
    ], 'classroom'), namespace='customers')), 


    path('hotels/', include(([
        path('', Hotel_Home, name='Hotel_Home'),
        path('addroom/', AddRoom, name='addroom'),
        path('viewroom/', ViewRoom, name='viewroom'),
        path('editroom/<i_id>', EditRoom, name='editroom'),
        path('bookinginfo/', BookingInfo, name='bookinginfo'),
    ], 'classroom'), namespace='hotels')),

]
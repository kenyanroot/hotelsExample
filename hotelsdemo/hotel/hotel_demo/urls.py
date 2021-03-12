from django.urls import path,include
from .views import search,hoteldetails,roomdetails,book,booking_form

urlpatterns = [


    path('', search, name='search'),
    path('hoteldetails/<str:hotelid>', hoteldetails, name='hoteldetails'),
    path('roomdetails/<str:offer_id>', roomdetails, name='roomdetails'),
    path('book/<str:offerid>', book, name='book'),
    path('bookingform/<str:offerid>', booking_form, name='bookingform'),

]
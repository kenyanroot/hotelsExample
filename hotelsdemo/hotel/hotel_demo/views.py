from amadeus import ResponseError
from django.http import HttpResponse
from django.shortcuts import render
from amadeus import Client, ResponseError


amadeus = Client(
            client_id='clientID',
            client_secret='ClientSecret',
            hostname='production'
        )


def search(request):

    if request.method == "POST":
        citycode = request.POST.get('citycode', )
        checkindate = request.POST.get('checkindate', )
        checkoutdate = request.POST.get('checkoutdate', )



        # print(adults,children,rooms)
        destination = citycode.split()

        destination = destination[-1]


        data=' '
        try:
            # Get list of Hotels by city code
            hotels_by_city = amadeus.shopping.hotel_offers.get(cityCode=destination, checkInDate=checkindate,
                                                               checkOutDate=checkoutdate)
            data = hotels_by_city.data


        except ResponseError as error:
            print(error.description())



        context={
            'data':data,
        }
        print(context)


        return render(request,'results.html',context)

    else:

        return render(request, 'search.html')




def hoteldetails(request, hotelid):

    data= ' '
    try:
        # Get list of offers for a specific hotel
        hotel_offers = amadeus.shopping.hotel_offers_by_hotel.get(hotelId=hotelid)
        # print('this are hotel offers',hotel_offers.data)

        data = hotel_offers.data


    except ResponseError as error:
        raise error

    context = {
        'data': data,
    }

    return render(request, 'hoteldetails.html', context)



def roomdetails(request, offer_id):

    data=' '
    try:
        # Confirm the availability of a specific offer
        offer_availability = amadeus.shopping.hotel_offer(offer_id).get()
        # print('this is offer availlability',offer_availability.data)
        k = offer_availability.data

        data = k
        print(data)

    except ResponseError as error:

        raise error

    context = {
        'data': data,
    }
    return render(request, 'roomdetails.html', context)


def booking_form(request,offerid):
    if request.method == 'POST':
        data=request.POST.get('data', )
        data=eval(data)

        context={
            'offerid':offerid,
            'data':data,
        }
        return render(request,'booking_form.html',context)

    else:
        return HttpResponse('you seem lost!')



def book(request, offerid):

    if request.method == 'POST':
        data=request.POST.get('data', )
        title = request.POST.get('title', )
        firstname = request.POST.get('FirstName', )
        lastname = request.POST.get('LastName', )
        phone = request.POST.get('phone', )
        email = request.POST.get('email', )
        cardVendorCode = request.POST.get('card_vendor_code', )
        Card_number = request.POST.get('card_number', )
        Expiry = request.POST.get('expiry', )
        # print(offerid, title, firstname, lastname, email, phoneno,cardVendorCode,Card_number,Expiry)
        offer = offerid


        try:


            guests = [{'id': 1,'name': {'title': title, 'firstName': firstname, 'lastName': lastname},'contact': {'phone': phone, 'email': email}}]
            payments = {'id': 1,'method': 'creditCard',
                        'card': {'vendorCode': cardVendorCode, 'cardNumber': Card_number, 'expiryDate': Expiry}} #'2021-08'

            hotel_booking = amadeus.booking.hotel_bookings.post(offer, guests, payments)

            data=hotel_booking.data

        except ResponseError as error:
            print('this is ', error)
            return HttpResponse('booking failed')

        return HttpResponse('booking successfull')

    else:
        context={
            'offerid':offerid,
        }


        return render(request,'booking_form.html',context)

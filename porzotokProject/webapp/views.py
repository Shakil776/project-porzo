from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from porzotokProject.settings import BASE_URL_LOCAL, BASE_URL_LIVE
from django.shortcuts import get_object_or_404
from porzotokApp import models
import requests
import json
import uuid
from porzotokApp.password import PassWord 
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from sys import platform
url_base_path = ""
if platform == 'linux':
    url_base_path = BASE_URL_LIVE
else:
    url_base_path = BASE_URL_LOCAL


# Create your views here.


''' 
    * START
    * FRONTEND
    * Porzotok frontend view start from here 
'''

# home 
class HomeView(View):
    def get(self, request):
        context = {}
        context['twenty_deals'] = []
        context['24_room'] = []
        context['hotels'] = models.HotelDetails.objects.filter(is_active=True)
        context['recommendedHotels'] = models.HotelDetails.objects.filter(is_recommended=True, is_active=True)
        context['spots'] = models.TouristSpot.objects.filter()
        twenty_deals = models.Room.objects.filter(is_deals=True)
        for each in twenty_deals:
            if each.hotel_id not in context['24_room']:
                context['twenty_deals'].append(each)
                context['24_room'].append(each.hotel_id)

        context['citys'] = list(dict.fromkeys([each.city_id.city_name for each in context['hotels']]))[:7]
        context['citys_by_hotel'] = []
        context['touristspots'] = models.TouristSpot.objects.filter(city_id__is_popular=True)[:6]
        for i_ in context['hotels']:
            try:
                min_val = min([each.price_id.offer_price for each in models.Room.objects.filter(hotel_id = i_)])
            except:
                min_val = 0
            list_image = []
            for img_ in models.Image.objects.filter(image_galary_details_id=i_.image_galary_details_id.image_galary_details_id):
                list_image.append(img_.Image.url)
            each_hotel = {
                'hotel_id': i_.hotel_id,
                'hotel_name': i_.hotel_name,
                'slug': i_.slug_name,
                'image': list_image,
                'price': min_val,
                'city': i_.city_id.city_name,
                'state': i_.city_id.state_id.state_name,
                'country': i_.city_id.state_id.country_id.country_name,
            }
            context['citys_by_hotel'].append(each_hotel)
        return render(request, 'frontEnd/html/home/home.html', context)

    def post(self, request):
        pass

# checkout
class CheckOutView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/checkout/checkout.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/checkout/checkout.html', context)

# confirm booking page
class ConfirmBookingView(View):
    def get(self, request):
        context = {}
        return HttpResponseRedirect('/')

    def post(self, request):
        context = {}
        if 'csrfmiddlewaretoken' in request.POST and 'user_id' in request.POST and 'payment_id' in request.POST and 'cart_id_cookie'in request.POST:
            user_id = request.POST['user_id']
            payment_id = request.POST['payment_id']
            cart_id_cookie = request.POST['cart_id_cookie']
            this_cart_id = models.Cart.objects.get(cart_id=cart_id_cookie)
            booking = False
            date_cal = models.RoomCartDetails.objects.filter(cart_id=this_cart_id)
            booking_total_amount = 0
            for eachRoom in date_cal:
                booking_total_amount += eachRoom.static_offer_price
                if eachRoom.check_in_date is not None and eachRoom.check_out_date is not None:
                    booking = True

            if booking:
                if this_cart_id.is_active:
                    booking_data = models.Booking(
                            user_id = models.User.objects.get(user_id=user_id),
                            cart_id = this_cart_id,
                            payment_method_id = models.Payment.objects.get(payment_method_id=payment_id),
                            booking_status = 1,
                            total_amount = booking_total_amount,
                        )
                    booking_data.save()

                    if booking_data:
                        #Price copy from main price table
                        query_ = models.RoomCartDetails.objects.filter(cart_id__cart_id=cart_id_cookie)
                        hotels_reviews = []
                        for each_room in query_:
                            if each_room.room_id.hotel_id not in hotels_reviews:
                                add_review_p = models.BookingReviewBool(
                                    user_id = each_room.cart_id.user_id,
                                    hotel_id = each_room.room_id.hotel_id,
                                    is_active = True
                                ).save()
                                hotels_reviews.append(each_room.room_id.hotel_id)
                            each_room.static_regular_price = each_room.room_id.price_id.price
                            each_room.static_offer_price = each_room.room_id.price_id.offer_price
                            each_room.room_status = '3'
                            each_room.save()

                        # booking table copy into confirm booking
                        booking_datail = models.Booking.objects.get(cart_id__cart_id=cart_id_cookie)
                        price = models.RoomCartDetails.objects.filter(cart_id__cart_id = booking_data.cart_id.cart_id)
                        total_price = 0
                        for p in price:
                            total_day = (p.check_out_date - p.check_in_date).days
                            days_amount = total_day * p.static_offer_price
                            total_price += days_amount
                        confirm_booking = models.ConfirmBooking(
                                booking_id = booking_datail.booking_id,
                                user_id = models.User.objects.get(user_id=booking_datail.user_id.user_id),
                                cart_id = models.Cart.objects.get(cart_id=booking_datail.cart_id.cart_id),
                                booking_status = booking_datail.booking_status,
                                total_amount = total_price,
                                total_payable_amount = 0.0,
                                vat_amount = 0.0,
                                vat_percent = 0.0,
                                payment_method = booking_datail.payment_method_id.payment_method_name,
                                payment_account_number = '',
                                transaction_code = '',
                                offer_type = '',
                                offer_amount = 0.0,
                                offer_max_amount = 0.0,
                                coupon_code = '',
                                coupon_amount = 0.0,
                                coupon_max_amount = 0.0,
                                hotel_discount_amount = 0.0,
                                hotel_discount_max_amount = 0.0,
                                gift_card_number = '',
                                gift_card_amount = 0.0,
                            )
                        confirm_booking.save()
                
                        # deactive user cart and delete user current session
                        this_cart_id.is_active = False
                        this_cart_id.save()
                        del request.session['session_id']
                        context['booking_details'] = confirm_booking
                        context['room_booking_details'] = models.RoomCartDetails.objects.filter(cart_id=confirm_booking.cart_id)

                else:
                    context['booking_details'] = {}
            else:
                context['booking_details'] = {}
            
        return render(request, 'frontEnd/html/checkout/confirm_booking.html', context)

# single hotel 
class SingleHotelView(View):

    def get(self, request, hotel_slug):
        context = {}
        if 'session_id' not in request.session:
            request.session['session_id'] = str(uuid.uuid4())
            request.session['isActive'] = 0
            context['pro_cart_id'] = 0
        else:
            try:
                context['pro_cart_id'] = models.Cart.objects.get(session_id=request.session['session_id']).cart_id
                request.session['isActive'] = 1
            except:
                context['pro_cart_id'] = 0
                #request.session['isActive'] = 0 # add it for create session in search page

        context['isActive'] = request.session['isActive']
        context['single_hotel_data'] = requests.get(f'{url_base_path}/single-hotel-details/{hotel_slug}/').json()

        return render(request, 'frontEnd/html/hotels/single_hotel.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/hotels/single_hotel.html', context)

#Destination Single View
class SingleCityView(View):
    def get(self, request, city_slug):
        context = {}
        context['city_s'] = models.City.objects.filter(city_slug_name=city_slug)
        
        if len(context['city_s']) != 0:
            context['touristspots'] = models.TouristSpot.objects.filter(city_id__city_name= context['city_s'][0].city_name)
            context['hotels'] = models.HotelDetails.objects.filter(city_id__city_name= context['city_s'][0].city_name)
            context['spot_by_city'] = []
            context['city_by_hotels'] = []
            for i_ in context['touristspots']:
                list_image = []
                for img_ in models.Image.objects.filter(image_galary_details_id=i_.image_galary_details_id.image_galary_details_id):
                    list_image.append(img_.Image.url)
                try:
                    tourist_image = list_image[0]
                except:
                    tourist_image = ""

                each_tspot = {
                    'tourist_spot_name': i_.tourist_spot_name,
                    'slug': i_.slug_name,
                    'image': tourist_image,
                    'description': i_.description,
                    'city': i_.city_id.city_name,
                    'tag_line': i_.city_id.tag_line,
                    'city_slug': i_.city_id.city_slug_name,
                    'state': i_.city_id.state_id.state_name,
                    'country': i_.city_id.state_id.country_id.country_name,
                }
                context['spot_by_city'].append(each_tspot)

            for i_ in context['hotels']:
                list_image = []
                for img_ in models.Image.objects.filter(image_galary_details_id=i_.image_galary_details_id.image_galary_details_id):
                    list_image.append(img_.Image.url)
                    
                try:
                    tourist_image = list_image[0]
                except:
                    tourist_image = ""

                each_hotel = {
                    'hotel_name': i_.hotel_name,
                    'slug': i_.slug_name,
                    'image': tourist_image,
                    'city': i_.city_id.city_name,
                    'city_slug': i_.city_id.city_slug_name,
                    'state': i_.city_id.state_id.state_name,
                    'country': i_.city_id.state_id.country_id.country_name,
                }
                context['city_by_hotels'].append(each_hotel)
            
        return render(request, 'frontEnd/html/others/destination.html', context)

# spot single view
class SpotSingleView(View):
    
    def get(self, request, spots_slug):
        context = {}
        context['tourist_spots'] = models.TouristSpot.objects.filter(slug_name=spots_slug)
        if len(context['tourist_spots']) != 0:
            context['hotel_s'] = models.HotelDetails.objects.filter(spot= context['tourist_spots'][0])
            context['spots_by_hotels'] = []
            for i_ in context['hotel_s']:
                list_image = []
                for img_ in models.Image.objects.filter(image_galary_details_id=i_.image_galary_details_id.image_galary_details_id):
                    list_image.append(img_.Image.url)
                e_each_hotel = {
                    'hotel_name': i_.hotel_name,
                    'slug': i_.slug_name,
                    'image': list_image[0],
                    'city': i_.city_id.city_name,
                    'spots_slug':spots_slug,
                    'state': i_.city_id.state_id.state_name,
                    'country': i_.city_id.state_id.country_id.country_name,
                }
                context['spots_by_hotels'].append(e_each_hotel)

        return render(request, 'frontEnd/html/others/spotsingleview.html', context)

# SearchView
class SearchView(View):
    def get(self, request):
        context = {}
        if 'search_session_id' not in request.session:
            request.session['search_session_id'] = str(uuid.uuid4())
        return render(request, 'frontEnd/html/search/search.html', context)

# Cartview/ show cart details
class CartSView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/cart/show_cart_details.html', context)

# user registraton from front end
class UserRegistrationView(View):

    def post(self, request):
        context = {}
        if 'email' in request.POST and 'name' in request.POST and 'mobile' in request.POST and 'password' in request.POST and 'nid_number' in request.POST and 'date_of_birth' in request.POST and 'gender' in request.POST and 'city' in request.POST and 'address' in request.POST:
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            nid_number = request.POST['nid_number']
            date_of_birth = request.POST['date_of_birth']
            gender = request.POST['gender']
            address = request.POST['address']
            city = request.POST['city']
            password = request.POST['password']
            
            register = models.User(
                    user_name = name,
                    user_email = email,
                    user_phone = mobile,
                    gender = gender,
                    city_id = models.City.objects.get(city_id=int(city)),
                    user_password = PassWord(password),
                    user_national_id_card = nid_number,
                    date_of_birth = date_of_birth,
                    user_short_address = address,
                )
            register.save()


            request.session['user_id'] = register.user_id
            request.session['user_name'] = register.user_name
            request.session['type'] = 'customer'
            request.session['time'] = str(register.created_at)
            request.session['isLogin'] = True
            context['user_id'] = register.user_id
            context['user_name'] = register.user_name
            context['type'] = 'customer'
            context['time'] = str(register.created_at)
            context['isLogin'] = True

        elif 'name' in request.POST and 'email' in request.POST and 'mobile' in request.POST and 'password' in request.POST:
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password = request.POST['password']
            if name == "" or email == "" or mobile == "" or password == "":
                context['isLogin'] = False
            else:
                try:
                    register = models.User(
                            user_name = name,
                            user_email = email,
                            user_phone = mobile,
                            user_password = PassWord(password)
                        )
                    register.save()


                    request.session['user_id'] = register.user_id
                    request.session['user_name'] = register.user_name
                    request.session['type'] = 'customer'
                    request.session['time'] = str(register.created_at)
                    request.session['isLogin'] = True
                    context['user_id'] = register.user_id
                    context['user_name'] = register.user_name
                    context['type'] = 'customer'
                    context['time'] = str(register.created_at)
                    context['isLogin'] = True
                except:
                    context['isLogin'] = False

        return JsonResponse({"data": context})

# user login from front end
class UserLoginView(View):
    
    def post(self, request):
        context = {}
        if 'mobile' in request.POST and 'password' in request.POST:
            mobile = request.POST['mobile']
            password = request.POST['password']

            try:
                user = models.User.objects.get(user_phone=mobile, user_password=PassWord(password))
                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.user_name
                request.session['type'] = 'customer'
                request.session['time'] = str(user.created_at)
                request.session['isLogin'] = True
                context['user_id'] = user.user_id
                context['user_name'] = user.user_name
                context['type'] = 'customer'
                context['time'] = str(user.created_at)
                context['isLogin'] = True
            except:
                context['isLogin'] = False
        return JsonResponse({"data": context})

# user logout from front end
class UserLogOutView(View):

    def post(self, request):
        context = {}

        if 'user_id' in request.session and 'user_name' in request.session\
         and 'type' in request.session and 'time' in request.session and 'isLogin' in request.session:

            try:
                del request.session['user_id']
                del request.session['user_name']
                del request.session['type']
                del request.session['time']
                del request.session['isLogin']
                context['success'] = True
            except:
                context['success'] = False
        return JsonResponse({"data": context})
    

class TwentyFourHoursDealsView(View):
    def get(self, request):
        context = {}
        if 'session_id' not in request.session:
            request.session['session_id'] = str(uuid.uuid4())
            request.session['isActive'] = 0
            context['pro_cart_id'] = 0
        else:
            try:
                context['pro_cart_id'] = models.Cart.objects.get(session_id=request.session['session_id']).cart_id
                request.session['isActive'] = 1
            except:
                context['pro_cart_id'] = 0

        context['isActive'] = request.session['isActive']

        return render(request, 'frontEnd/html/deals/twenty_four_hours_deals.html', context)
    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/deals/twenty_four_hours_deals.html', context)      

# login from mobile device view
class UserLoginFromMobileDeviceView(View):
    def get(self, request):
        context = {}
        if 'user_id' in request.session and 'user_name' in request.session:
            return HttpResponseRedirect("/")
        else:
            return render(request, 'frontEnd/html/login/mobile_login.html', context)

# register from mobile device view
class UserRegistrationFromMobileDeviceView(View):
    def get(self, request):
        context = {}
        if 'user_id' in request.session and 'user_name' in request.session:
            return HttpResponseRedirect("/")
        else:
            return render(request, 'frontEnd/html/login/mobile_register.html', context)

# about us
class AboutUsView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/about_us.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/about_us.html', context)   

# contact us
class ContactUsView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/contact_us.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/contact_us.html', context)   

# faq
class FaqView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/faq.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/faq.html', context)

# blog
class BlogView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/blog.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/blog.html', context)

# press
class PressView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/press.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/press.html', context)

# Terms Of Use
class TermsOfUseView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/terms_of_use.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/terms_of_use.html', context)

# Give us feedback
class GiveFeedbackView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/give_us_feedback.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/give_us_feedback.html', context)

# Help center
class HelpCenterView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/help_center.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/help_center.html', context)

# Privacy policy
class PrivacyPolicyView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/privacy_policy.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/privacy_policy.html', context)

# event
class EventFrontEndView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/event.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/event.html', context)

# services
class ServicesFrontEndView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/services.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/others/services.html', context)

# hotel
class HotelsFrontEndView(View):
    def get(self, request):
        context = {}
        context['cities'] = models.City.objects.filter()
        context['facilites'] = models.Facilites.objects.filter()
        context['hotels'] = models.HotelDetails.objects.filter(is_active=True)
        return render(request, 'frontEnd/html/hotels/v-hotels.html', context)

    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/hotels/hotels.html', context)


# user profile view
class UserProfileView(View):
    def get(self, request):
        context = {}
        if 'user_id' in request.session and 'user_name' in request.session:
            return render(request, 'frontEnd/html/user/profile.html', context)
        else:
            return HttpResponseRedirect("/")
    def post(self, request):
        context = {}
        return render(request, 'frontEnd/html/user/profile.html', context)
''' 
    * END
    * FRONTEND
    * Porzotok frontend view end
'''




''' 
    * START
    * Porzotok admin panel view start from here 
'''

# Porzotok Dashboard
class DashboardView(View):

    def get(self, request):
        context = {}
        return render(request, 'backEnd/dashboard/dashboard.html', context)
    def post(self, request):
        return HttpResponse("Under Development")

# admin login view
class AdminLoginView(View):

    def get(self, request):
        context = {}
        return render(request, 'backEnd/admin_login.html', context)

# hotel user type 
class UserTypeView(View):
    def get(self, request):
        context = {}
        return render(request, 'backEnd/hotel-user/user_type.html', context)

# List Of Hotel
class HotelView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/hotel/hotels.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/hotel/hotels.html', context)

# Rooms
class RoomView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/room/rooms.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/room/rooms.html', context)

# Offer types
class OfferTypeView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/offers/offer_types.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/offers/offer_types.html', context)

# Offer max amount
class OfferMaxAmountView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/offers/offer_max_amount.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/offers/offer_max_amount.html', context)

# Offer
class OfferView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/offers/offer.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/offers/offer.html', context)

# events
class EventView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/events/events.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/events/events.html', context)


# Food Menu
class FoodMenuView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/foodmenu/foodmenu.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/foodmenu/foodmenu.html', context)
#Tourist Spot
class TouristSpotView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/touristspot/touristspot.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/touristspot/touristspot.html', context)

#HotelGallery
class HotelGallery(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/gallery/gallery.html', context)

    def post(self, request):
        context = {}
        return render(request, 'backEnd/gallery/gallery.html', context)

# booking 
class BookingView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/booking/booking.html', context)

    def post(self, request):
        context = {}
        return render(request, 'backEnd/booking/booking.html', context)

#Cupon
class CuponView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/offers/cupon.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/offers/cupon.html', context)

#GiftCard
class GiftCardView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/offers/giftcard.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/offers/giftcard.html', context)


# package 
class PackageView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/package/package.html', context)

    def post(self, request):
        context = {}
        return render(request, 'backEnd/package/package.html', context)


# carts 
class CartView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/cart/cart.html', context)

    def post(self, request):
        context = {}
        return render(request, 'backEnd/cart/cart.html', context)

# Facilites
class FacilitesView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/facilites/facilites.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/facilites/facilites.html', context)

# FacilitesGroup
class FacilitesGroupView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/facilites/facilitesgroup.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/facilites/facilitesgroup.html', context)


# FacilitesGroup 
class HotelFacilitesView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/facilites/hotelfacilites.html', context)

    def post(self, request):
        context = {}
        return render(request, 'backEnd/facilites/hotelfacilites.html', context)        

# Twenty Four Hours Deals Porzotok View
class TwentyFourHoursDealsPorzotokAppView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/24hoursdeals/porzotok_24_hours_deals.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/24hoursdeals/porzotok_24_hours_deals.html', context)    
class TwentyFourHoursDealsHotelView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'backEnd/24hoursdeals/hotel_room_24_hours_deals.html', context)
    def post(self, request):
        context = {}
        return render(request, 'backEnd/24hoursdeals/hotel_room_24_hours_deals.html', context)
''' 
    * END
    * Porzotok admin panel view end
'''
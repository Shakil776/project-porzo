from django.shortcuts import render
from porzotokApp import models
from androidAPI_V1 import serializers
from rest_framework import viewsets, generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from porzotokApp.password import PassWord, saveRecentSearchHistory, CheckAvailable
from HotelAdmin.pagination import PaginationHandlerMixin
import datetime
from django.db.models import Q
import base64
import io
import PIL.Image as Image
from django.core.files.base import ContentFile
import uuid
import re

# Create your views here.

# country 
class CountryAPIView(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer

# state 
class StateAPIView(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer

# city 
class CityAPIView(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer

# hotel detail 
class HotelDetailViewSet(viewsets.ViewSet):
    def list(self, request):
        hotel_details = models.HotelDetails.objects.filter(is_active=True)
        serializer = serializers.HotelDetailsSerializer(hotel_details, many=True, context={"request": request}) 
        return Response({"error": False, "message": "All Hotel Details List", "data": serializer.data})

# Search 
class SearchModelViewSet(viewsets.ViewSet):

    def list(self, request):

        if 'q' in request.GET:
            key = request.GET.get('q')
            results = models.HotelDetails.objects.filter(hotel_name__contains=str(key))[:5]
            serializer = serializers.FrontEndSearchHotelDetailsSerializer(results, many=True, context={"request": request})
            cities = models.City.objects.filter(city_name__contains=str(key))[:5]
            city_serializer = serializers.FrontEndSearchCitySerializer(cities, many=True, context={"request": request})
            return Response({"error": False, "message": "Search results", "data": serializer.data, "cities": city_serializer.data})

# search result details
class SearchResultModelViewSet(viewsets.ViewSet):

    def list(self, request):
        search_result_list = []

        if 'q' in request.GET and 'user_id' in request.GET and 'search_session_id' in request.GET:
            key = request.GET.get('q')
            user_id = request.GET.get('user_id')
            search_session_id = request.GET.get('search_session_id')

            results = models.HotelDetails.objects.filter(Q(hotel_name__contains=str(key)) | Q(city_id__city_name__contains=str(key)) | Q(hotel_info__contains=str(key)) | Q(short_address__contains=str(key)))
            serializer = serializers.SearchResultDetailsSerializer(results, many=True, context={"request": request})
            search_result_list = serializer.data
            # save recent search history
            saveRecentSearchHistory(user_id, search_session_id, key)
            return Response({"error": False, "message": "Search results", "data": serializer.data})

# user recent search keyword
class SearchKeyWordViewSet(viewsets.ViewSet):
    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            results = models.RecentSearch.objects.filter(user_id__user_id=user_id).order_by('-created_at')[:5]
            serializer = serializers.SearchKeyWordSerializer(results, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data})

# Single Hotel Details
class SingleHotelDetailsFrontEndViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):
        queryset = models.HotelDetails.objects.all()
        single_hotel = get_object_or_404(queryset, slug_name=pk)
        serializer = serializers.HotelInfoFrontEndRoomSerializer(single_hotel, context={"request": request})
        return Response({"error": False, "message": "Single Hotel Details", "data": serializer.data})

# CartByUserModelViewSet
class CartByUserModelViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            cart_user = models.Cart.objects.filter(user_id__user_id=user_id, is_active=True).order_by('-cart_id')
            serializer = serializers.CartSerializer(cart_user, many=True, context={"request": request})
            return Response({"error": False, "data":serializer.data})

# cart
class CartModelViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

# CartDetails create
class CartDetailsModelViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            # save room CartDetails
            if 'room_id' in request.data:
                day_count = False
                room_cart_detail = {}
                room_cart_detail["cart_id"] = request.data['cart_id']

                # start check cart id available in database
                try:
                    cart = models.Cart.objects.get(cart_id=int(request.data['cart_id']))
                except:
                    add_cart = models.Cart(
                        user_id=models.User.objects.get(user_id=request.data['user_id']),
                        session_id=request.data['session_id']
                    )
                    add_cart.save()
                    room_cart_detail["cart_id"] = add_cart.cart_id
                # end check cart id available in database

                room_cart_detail["room_id"] = request.data['room_id']
                room_cart = models.Room.objects.filter(room_id=int(request.data['room_id']))
                if len(room_cart) != 0:
                    room_cart = room_cart[0]
                    if 'check_in_time' in request.data and 'check_out_time' in request.data:
                        day_count = True
                        
                        #Check Room Available
                        de = CheckAvailable(request.data['check_in_time'], request.data['check_out_time'], int(request.data['room_id']))
                        if 'match' in de:
                            if de['match']:
                                return Response({"error": True, "message": "This room already booked in this date", 'cart_id': room_cart_detail["cart_id"]})
                        #Check Room Available
                        room_cart_detail["check_in_date"] = request.data['check_in_time']
                        room_cart_detail["check_out_date"] = request.data['check_out_time']
                        re_start_date = str(request.data['check_in_time']).split('-')
                        re_end_date = str(request.data['check_out_time']).split('-')
                        start_date = datetime.date(int(re_start_date[0]), int(re_start_date[1]), int(re_start_date[2]))
                        end_date = datetime.date(int(re_end_date[0]), int(re_end_date[1]), int(re_end_date[2]))

                        total_days = end_date - start_date
                        room_cart_detail["total_day"] = total_days.days
                        room_cart_detail["static_regular_price"] = int(room_cart.price_id.price) * total_days.days
                        room_cart_detail["static_offer_price"] = int(room_cart.price_id.offer_price) * total_days.days
                        
                    room_cart_serializer = serializers.RoomCartDetailsSerializer(data=room_cart_detail, context={"request": request})
                    room_cart_serializer.is_valid(raise_exception=True)
                    room_cart_serializer.save()
                
            # save food menu CartDetails
            if 'food_menu_id' in request.data:
                food_cart_list = []
                food_cart_detail = {}
                food_cart_detail["cart_id"] = request.data['cart_id']
                food_cart_detail["food_id"] = request.data['food_menu_id']
                food_cart_list.append(food_cart_detail)
                food_cart_serializer = serializers.FoodMenuCartDetailsSerializer(data=food_cart_list, many=True, context={"request": request})
                food_cart_serializer.is_valid(raise_exception=True)
                food_cart_serializer.save()

            # save hotel Facilities CartDetails
            if 'hotel_facilites_id' in request.data:
                facilities_cart_list = []
                facilities_cart_detail = {}
                facilities_cart_detail["cart_id"] = request.data['cart_id']
                facilities_cart_detail["hotel_facilites_id"] = request.data['hotel_facilites_id']
                facilities_cart_list.append(facilities_cart_detail)
                facilities_cart_serializer = serializers.FacilitesCartDetailsSerializer(data=facilities_cart_list, many=True, context={"request": request})
                facilities_cart_serializer.is_valid(raise_exception=True)
                facilities_cart_serializer.save()

            # save Package CartDetails
            if 'package_id' in request.data:
                package_cart_list = []
                package_cart_detail = {}
                package_cart_detail["cart_id"] = request.data['cart_id']
                package_cart_detail["package_id"] = request.data['package_id']
                package_cart_list.append(package_cart_detail)
                package_cart_serializer = serializers.PackageCartDetailsSerializer(data=package_cart_list, many=True, context={"request": request})
                package_cart_serializer.is_valid(raise_exception=True)
                package_cart_serializer.save()

            dict_response = {"error": False, "message": "Added Successfully in the cart", "cart_id": room_cart_detail["cart_id"]}
        except Exception as e:
            dict_response = {"error": True, "message": "CartDetails Information Not Save."}
        return Response(dict_response)

    def update(self, request, pk=None):
        try:
            cart_id = request.data['cart_id']
            queryset = models.RoomCartDetails.objects.all()
            room_cart = get_object_or_404(queryset, cart_id__cart_id=cart_id, room_cart_details_id=pk)

            details = {}
            details["check_in_date"] = request.data['check_in_date']
            details["check_out_date"] = request.data['check_out_date']
            #Check Room Available
            de = CheckAvailable(request.data['check_in_date'], request.data['check_out_date'], int(room_cart.room_id.room_id))
            if 'match' in de:
                if de['match']:
                    return Response({"error": True, "message": "This room already booked in this date"})
            #Check Room Available
            re_start_date = str(request.data['check_in_date']).split('-')
            re_end_date = str(request.data['check_out_date']).split('-')
            start_date = datetime.date(int(re_start_date[0]), int(re_start_date[1]), int(re_start_date[2]))
            end_date = datetime.date(int(re_end_date[0]), int(re_end_date[1]), int(re_end_date[2]))
            total_days = end_date - start_date
            details["total_day"] = total_days.days
            details["static_regular_price"] = int(room_cart.room_id.price_id.price) * total_days.days
            details["static_offer_price"] = int(room_cart.room_id.price_id.offer_price) * total_days.days
            serializer = serializers.UpdateRoomCartDetailsSerializer(room_cart, partial=True, data=details, context={"request": request})
            if serializer.is_valid():
                serializer.save()
            dict_response = {"error": False, "message": "Booking Date Updated.", "data": serializer.data}
        except Exception as e:
            dict_response = {"error": True, "message": "Not Updated",  "data": {}}
        return Response(dict_response)

# get user cart details
class UserCartDetailsModelViewSet(viewsets.ViewSet): 

    def list(self, request):

        if 'u_id' in request.GET:
            user_id = request.GET.get('u_id')

            user_carts = models.Cart.objects.filter(user_id__user_id=int(user_id), is_active=True)
            if len(user_carts) != 0:
                user_cart_serializer = serializers.UserFrontEndCartSerializer(user_carts, many=True, context={"request": request})

                for user_cart in user_cart_serializer.data:
                    # room
                    user_cart_room_details = models.RoomCartDetails.objects.filter(cart_id=user_cart['cart_id'])

                    room_serializer = serializers.FrontEndRoomCartDetailsSerializer(user_cart_room_details, many=True, context={"request": request})


                    # food
                    user_cart_food_details = models.FoodMenuCartDetails.objects.filter(cart_id=user_cart['cart_id'])

                    food_menu_serializer = serializers.FrontEndFoodMenuCartDetailsSerializer(user_cart_food_details, many=True, context={"request": request})

                    # facilities
                    user_cart_facilities_details = models.FacilitesCartDetails.objects.filter(cart_id=user_cart['cart_id'])

                    facilities_cart_serializer = serializers.FrontEndFacilitiesCartDetailsSerializer(user_cart_facilities_details, many=True, context={"request": request})

                    # package
                    user_cart_package_details = models.PackageCartDetails.objects.filter(cart_id=user_cart['cart_id'])

                    package_cart_serializer = serializers.FrontEndPackageCartDetailsSerializer(user_cart_package_details, many=True, context={"request": request})
                return Response(
                    {
                        "error": False, 
                        "message": "Cart List", 
                        "data": {
                            'cart_id': user_cart_serializer.data[0]['cart_id'],
                            'cart_room_data': room_serializer.data,
                            'cart_food_data': food_menu_serializer.data,
                            'cart_facilities_data': facilities_cart_serializer.data,
                            'cart_package_data': package_cart_serializer.data
                        }
                    }
                )

            else:
                return Response(
                    {
                        "error": False, 
                        "message": "Cart List", 
                        "data": {
                            'cart_id': 0,
                            'cart_room_data': [],
                            'cart_food_data': [],
                            'cart_facilities_data': [],
                            'cart_package_data': []
                        }
                    }
                )
        elif 'session_id' in request.GET:

            session_id = request.GET.get('session_id')

            user_carts = models.Cart.objects.filter(session_id=str(session_id), is_active=True)

            if len(user_carts) != 0:

                user_cart_serializer = serializers.UserFrontEndCartSerializer(user_carts, many=True, context={"request": request})

        
                for user_cart in user_cart_serializer.data:
                    # room
                    user_cart_room_details = models.RoomCartDetails.objects.filter(cart_id=user_cart['cart_id'])

                    room_serializer = serializers.FrontEndRoomCartDetailsSerializer(user_cart_room_details, many=True, context={"request": request})


                    # food
                    user_cart_food_details = models.FoodMenuCartDetails.objects.filter(cart_id=user_cart['cart_id'])

                    food_menu_serializer = serializers.FrontEndFoodMenuCartDetailsSerializer(user_cart_food_details, many=True, context={"request": request})

                     # facilities
                    user_cart_facilities_details = models.FacilitesCartDetails.objects.filter(cart_id=user_cart['cart_id'])

                    facilities_cart_serializer = serializers.FrontEndFacilitiesCartDetailsSerializer(user_cart_facilities_details, many=True, context={"request": request})

                    # package
                    user_cart_package_details = models.PackageCartDetails.objects.filter(cart_id=user_cart['cart_id'])

                    package_cart_serializer = serializers.FrontEndPackageCartDetailsSerializer(user_cart_package_details, many=True, context={"request": request})

                return Response(
                    {
                        "error": False, 
                        "message": "Cart List", 
                        "data": {
                            'cart_id': user_cart_serializer.data[0]['cart_id'],
                            'cart_room_data': room_serializer.data,
                            'cart_food_data': food_menu_serializer.data,
                            'cart_facilities_data': facilities_cart_serializer.data,
                            'cart_package_data': package_cart_serializer.data
                        }
                    }
                )

            else:
                return Response(
                    {
                        "error": False, 
                        "message": "Cart List", 
                        "data": {
                            'cart_id': 0,
                            'cart_room_data': [],
                            'cart_food_data': [],
                            'cart_facilities_data': [],
                            'cart_package_data': []
                        }
                    }
                )


    def destroy(self, request, pk=None):

        if 'session_id' in request.GET:
            session_id = request.GET.get('session_id')
            user_carts = models.RoomCartDetails.objects.get(cart_id__session_id=str(session_id), room_cart_details_id=pk)
            user_carts.delete()
            return Response({"error": False, "message": "Cart Item deleted successfully!"})
        elif 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            user_carts = models.RoomCartDetails.objects.get(cart_id__user_id__user_id=str(user_id), room_cart_details_id=pk)
            user_carts.delete()
            return Response({"error": False, "message": "Cart Item deleted successfully!"})

        return Response({"error": True, "message": "Cart Item Not Deleted!"})

# user 
class UserViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            user_detail = {}
            user_detail["user_name"] = request.data["name"]
            user_detail["user_email"] = request.data["email"]
            user_detail["user_phone"] = request.data["mobile"]
            user_detail["user_password"] = PassWord(request.data["password"])

            serializer = serializers.UserRegisterAndroidSerializer(data=user_detail, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "User Registration Completed Successfully!", "success": True, "data": serializer.data}
        except Exception as e:
            dict_response = {"error": True, "message": "Registration Failed. Please try again.", "success": False, "data": {}}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.User.objects.all()
        user = get_object_or_404(queryset, user_id=pk)
        serializer = serializers.SingleUserSerializer(user, context={"request": request})
        return Response({"error": False, "message": "Single User Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.User.objects.all()
            user = get_object_or_404(queryset, user_id=pk)
            user_detail = {}
            user_detail["user_name"] = request.data["name"]
            user_detail["user_email"] = request.data["email"]
            user_detail["gender"] = request.data["gender"]
            user_detail["date_of_birth"] = request.data["date_of_birth"]
            user_detail["user_short_address"] = request.data["user_address"]
            user_detail["city_id"] = request.data["city"]
            user_detail["user_national_id_card"] = request.data["nid_card_num"]

            serializer = serializers.UserProfileUpdateAndroidSerializer(user, data=user_detail, context={"request": request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "User Information Updated Successfully!", "data": serializer.data}
        except Exception as e:
            dict_response = {"error": True, "message": "User Information Not Updated."}
        return Response(dict_response)

# user login android api
class UserLoginAndroidViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            mobile = request.data["mobile"]
            password = request.data["password"]
            user = models.User.objects.get(user_phone=mobile, user_password=PassWord(password), is_active=True)
            serializer = serializers.UserLoginAndroidSerializer(user, context={"request": request})
            dict_response = {"error": False, "message": "Successfully Login.", "success": True, "data": serializer.data}
        except Exception as e:
            dict_response = {"error": True, "message": "Invalid cradentials.", "success": False, "data": {}}
        return Response(dict_response)

# change user password
class ChangeUserPasswordViewSet(viewsets.ViewSet):
    
    def update(self, request, pk=None):
        queryset = models.User.objects.all()
        user = get_object_or_404(queryset, user_id=pk)

        if PassWord(request.data['old_password']) == user.user_password:
            user.user_password = PassWord(request.data['new_password'])
            user.save()
            return Response({"error": False, "message": "Password Changed Successfully!"})
        else:
            return Response({"error": True, "message": "Password doesn't match."})

# update user profile photo
class UpdateUserProfilePhotoViewSet(viewsets.ViewSet):
    
    def update(self, request, pk=None):
        json_string = request.data['profile_image']
        random = str(uuid.uuid4())
        random = random.upper()
        random = random.replace("-", "")

        data = ContentFile(base64.b64decode(json_string), name=random + '.' + 'png')

        try:
            queryset = models.User.objects.all()
            user = get_object_or_404(queryset, user_id=pk)
            user_detail = {}
            user_detail["user_image"] = data
            serializer = serializers.UserProfilePhotoUpdateAndroidSerializer(user, data=user_detail, context={"request": request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"error": False, "message": "Profile Photo changed Successfully!", "data": serializer.data})
        except Exception as e:
            return Response({"error": True, "message": "Profile Photo not Changed!", "data": {}})

# get Review
class ReviewViewSet(viewsets.ViewSet):
    def list(self, request):
        if 'hotel_id' in request.GET:
            hotel_id = request.GET.get('hotel_id')
            queryset = models.Review.objects.filter(hotel_id__hotel_id=int(hotel_id))
            serializer = serializers.ReviewSerializer(queryset, many=True, context={"request": request})
        return Response({"error": False, "message": "User Review List.", "data": serializer.data})

# recommended hotels
class RecommendedHotelViewSet(viewsets.ViewSet):
    def list(self, request):
        hotel_details = models.HotelDetails.objects.filter(is_recommended=True, is_active=True)
        serializer = serializers.RecommendedHotelDetailsSerializer(hotel_details, many=True, context={"request": request})
        if len(serializer.data) != 0:
            return Response({"error": False, "message": "All Recommended Hotel Details List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "No Recommended Hotel Found", "data": []})

# Basic Pagination limit/size 
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

# twenty four hour deals room
class TwentyFourHoursDealsAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = serializers.RoomDealsSerializer

    def get(self, request, format=None, *args, **kwargs):
        instance = models.Room.objects.filter(is_deals=True, is_active=True).order_by('room_id')
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# check user active or deactive status
class CheckUserStatusViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            user = models.User.objects.get(user_id=user_id)
            if user.is_active == True:
                return Response({"is_active": True})
            else:
                return Response({"is_active": False})

# single room details  with related room
class SingleRoomDetailsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = models.Room.objects.all()
        room = get_object_or_404(queryset, pk=pk)
        max_price = (room.price_id.price) + 5000
        min_price = (room.price_id.price) - 5000
        serializer = serializers.SingleRoomDetailsSerializer(room)
        related_rooms = models.Room.objects.filter(~Q(room_id=room.room_id), hotel_id__city_id__city_name=room.hotel_id.city_id.city_name, price_id__price__range=(min_price, max_price))
        related_room_serializer = serializers.RelatedRoomDetailsSerializer(related_rooms, many=True)

        return Response({"error": False, "data": serializer.data, "related_rooms": related_room_serializer.data})


# Hotel By City View
class HotelByCityViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.GET.get('city_id'):
            city_id = request.GET.get('city_id')
            hotel_by_city = models.HotelDetails.objects.filter(city_id__city_id=int(city_id))
            serializer = serializers.HotelByCitySerializer(hotel_by_city, many=True, context={"request": request})
            return Response({"error": False, "message": "Hotel By City Data List", "data": serializer.data})
        else:
            return Response({"error": True, "message": "Hotel By City Data List"})

# Booking Details 
class BookingDetailsViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            queryset = models.ConfirmBooking.objects.filter(user_id__user_id=int(user_id)).order_by('-booking_id')
            serializer = serializers.BookingListSerializer(queryset, many=True, context={"request": request})
        return Response({"error": False, "message": "User Booking List.", "data": serializer.data})


    def retrieve(self, request, pk=None):
        queryset = models.ConfirmBooking.objects.all()
        booking_details = get_object_or_404(queryset, booking_id=int(pk))
        serializer = serializers.BookingDetailsSerializer(booking_details, context={"request": request})
        return Response({"error": False, "message": "User Single booking details.", "data":serializer.data})

#Book
class BookViewSet(viewsets.ViewSet):
        
    def create(self, request):
        try:
            cart_check = models.Cart.objects.filter(cart_id=request.data["cart_id"])
            if len(cart_check) != 0 and len(cart_check) == 1:
                #Room Available Check
                # de = CheckAvailable(request.data['check_in_time'], request.data['check_out_time'], int(request.data['room_id']), request.data["cart_id"])
                # if de['match']:
                #     return Response({"error": True, "message": "This room already booked in this date"})
                #Room Available Check
                # Save Booking details
                booking_details_list = []
                booking_detail = {}
                booking_detail["user_id"] = request.data["user_id"]
                booking_detail["cart_id"] = request.data["cart_id"]
                booking_detail["booking_status"] = 1
                booking_detail["payment_method_id"] = request.data["payment_id"]
                booking_details_list.append(booking_detail)
                # save into booking serializer
                serializer = serializers.BookingSerializer(data=booking_details_list, many=True, context={"request":request})
                serializer.is_valid(raise_exception=True)
                
                if serializer.save():
                    #Price copy from main price table
                    query_ = models.RoomCartDetails.objects.filter(cart_id__cart_id=request.data["cart_id"])
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
                    booking_data = models.Booking.objects.get(cart_id__cart_id=request.data["cart_id"])
                    #booking_data = models.Booking.objects.get(cart_id__cart_id=request.data["cart_id"])
                    price = models.RoomCartDetails.objects.filter(cart_id__cart_id = booking_data.cart_id.cart_id)
                    total_price = 0
                    for p in price:
                        total_day = (p.check_out_date - p.check_in_date).days
                        days_amount = total_day * p.static_offer_price
                        total_price += days_amount
                    confirm_booking = models.ConfirmBooking(
                            booking_id = booking_data.booking_id,
                            user_id = models.User.objects.get(user_id=booking_data.user_id.user_id),
                            cart_id = models.Cart.objects.get(cart_id=booking_data.cart_id.cart_id),
                            booking_status = booking_data.booking_status,
                            total_amount = total_price,
                            total_payable_amount = 0.0,
                            vat_amount = 0.0,
                            vat_percent = 0.0,
                            payment_method = booking_data.payment_method_id.payment_method_name,
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
                    #update cart table
                    update_cart = models.Cart.objects.get(cart_id=int(request.data["cart_id"]))
                    update_cart.is_active = False
                    update_cart.save()
                    dict_response = {"error": False, "message": "Booking Information Save Successfully!", 'data': serializer.data, "booking_id": confirm_booking.booking_id}
            else:
                dict_response = {"error": True, "message": "Cart Not Active."}
        except Exception as e:
            dict_response = {"error": True, "message": "Booking Information Not Save.", 'data': {}}
        return Response(dict_response)

# Single hotel all images list with pagination
class HotelImagesAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = serializers.ImageSerializer

    def get(self, request, format=None, *args, **kwargs):
        slug_name = self.request.query_params.get('slug_name')
        hotel = models.HotelDetails.objects.get(slug_name=slug_name, is_active=True)
        instance = models.Image.objects.filter(image_galary_details_id=hotel.image_galary_details_id)
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# Single room all images list with pagination
class RoomImagesAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = serializers.ImageSerializer

    def get(self, request, format=None, *args, **kwargs):
        room_id = self.request.query_params.get('room_id')
        room = models.Room.objects.get(room_id=room_id, is_active=True)
        instance = models.Image.objects.filter(image_galary_details_id=room.image_galary_details_id)
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
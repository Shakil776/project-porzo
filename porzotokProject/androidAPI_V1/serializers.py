from rest_framework import serializers
from porzotokApp import models
from django.db.models import Q


# hotel details serializer
class HotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user'] = HotelUserOwnerSerializer(instance.hotel_user_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['city'] = CitySerializer(instance.city_id).data
        response['reviews'] = ReviewSerializer(models.Review.objects.filter(hotel_id__hotel_id = instance.hotel_id), many=True).data
        return response

# hotel user owner serializer
class HotelUserOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserOwner
        fields = "__all__"
        extra_kwargs = {'hotel_user_password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_type'] = HotelUserTypeSerializer(instance.hotel_user_type_id).data
        return response

#Image serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'


# country serializer
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'

# state serializer
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['country'] = CountrySerializer(instance.country_id).data
        return response

# city serializer
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['state'] = StateSerializer(instance.state_id).data
        return response

# hotel user type serializer
class HotelUserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserType
        fields = "__all__"

# ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = "__all__"
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_details'] = UsersReviewSerializer(instance.user_id).data
        response['replay'] = ReviewReplaySerializer(models.ReviewReplay.objects.filter(review_id = instance.review_id), many=True).data
        return response

# User Review Serializer
class UsersReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_id','user_name', 'user_image']

# ReviewReplaySerializer
class ReviewReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewReplay
        fields = "__all__"
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = ReviewReplayHotelDetailsSerializer(instance.hotel_id).data
        response['photo_details'] = FrontEndHotelLogoSerializer(instance.logo_id).data
        return response

class ReviewReplayHotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id','hotel_name']

class FrontEndHotelLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FrontEndHotelLogo
        fields = "__all__"

# search autocomplete hotels
class FrontEndSearchHotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_name']

# search autocomplete city
class FrontEndSearchCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ['city_id', 'city_name']

# search result details
class SearchResultDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name', 'slug_name', 'city_id', 'hotel_info', 'image_galary_details_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['city'] = CitySerializer(instance.city_id).data
        response['hotel_facilities'] = FrontEndSearchHotelFacilitesSerializer(models.HotelFacilites.objects.filter(hotel_id__hotel_id=instance.hotel_id), many=True).data
        response['room_details'] = HotelDetailsFrontEndSearchRoomPriceSerializer(models.Room.objects.filter(hotel_id=instance.hotel_id), many=True).data
        response['reviews'] = ReviewSerializer(models.Review.objects.filter(hotel_id__hotel_id = instance.hotel_id), many=True).data
        return response

# search forntend HotelFacilitesFrontEndSerializer
class FrontEndSearchHotelFacilitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelFacilites
        fields = ['hotel_facilites_id', 'facilites_id', 'price_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['facilites_id'] = FacilitesSerializer(instance.facilites_id).data
        response['price_id'] = PriceSerializer(instance.price_id).data
        return response

# Facilites Serializer
class FacilitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Facilites
        fields = "__all__"

# Price serializer
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        fields = '__all__'

# Search page front end hotels with room price
class HotelDetailsFrontEndSearchRoomPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('room_id', 'is_deals', 'price_id')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = FrontEndSearchPriceSerializer(instance.price_id).data
        return response

# Front end search page Price
class FrontEndSearchPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        fields = ['price_id', 'price', 'offer_price']

# get search keyword 
class SearchKeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecentSearch
        fields = ['keyword']

# HotelDetailsFrontEndSingleRoomSerializer
class HotelDetailsFrontEndSingleRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('room_id', 'room_name', 'room_no', 'is_deals', 'deal_start_date', 'is_active', 'floor_id', 'price_id', 'room_status', 'room_description', 'image_galary_details_id')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['floor_details'] = FloorSerializer(instance.floor_id).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['facilites_details'] = FacilitesGroupSerializerFront(models.FacilitesGroup.objects.filter(room_id=instance.room_id), many=True).data
        return response

# Single Hotel Info
class HotelInfoFrontEndRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ('hotel_id', 'hotel_name', 'latitude', 'longitude', 'city_id', 'hotel_info', 'image_galary_details_id')
        lookup_field = "slug_name"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['room_details'] = HotelDetailsFrontEndSingleRoomSerializer(models.Room.objects.filter(hotel_id=instance.hotel_id).order_by('-is_deals'), many=True).data
        response['hotel_facilities_details'] = HotelFacilitesFrontEndSerializer(models.HotelFacilites.objects.filter(hotel_id=instance.hotel_id), many=True).data
        response['hotel_foodmenu_details'] = HotelFoodMenuFrontEndSerializer(models.FoodMenu.objects.filter(hotel_id=instance.hotel_id), many=True).data
        response['reviews'] = ReviewSerializer(models.Review.objects.filter(hotel_id__hotel_id = instance.hotel_id), many=True).data
        return response



# Floor serializer
class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floor
        fields = "__all__"

# FacilitesGroupSerializerFront
class FacilitesGroupSerializerFront(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesGroup
        fields = ("facilites_id", "facilites_group_id",)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['facilites_id'] = FacilitesSerializer(instance.facilites_id).data
        return response

# HotelFacilitesFrontEndSerializer
class HotelFacilitesFrontEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelFacilites
        fields = ['hotel_facilites_id', 'facilites_id', 'hotel_id', 'price_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['facilites_details'] = FacilitesSerializer(instance.facilites_id).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

# HotelFoodMenuFrontEndSerializer
class HotelFoodMenuFrontEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenu
        fields = ['food_menu_id', 'food_name', 'hotel_id', 'price_id','food_image']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

# Cart serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'

# RoomCartDetails Serializer
class RoomCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        fields = "__all__"
        extra_kwargs = {'check_in_date':{'required':False},'check_out_date':{'required':False}, 'total_day':{'required':False}}

# FoodMenuCartDetails Serializer
class FoodMenuCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenuCartDetails
        fields = "__all__"

# FacilitesCartDetails Serializer
class FacilitesCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesCartDetails
        fields = "__all__"

# PackageCartDetails Serializer
class PackageCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackageCartDetails
        fields = "__all__"

# FrontEnd Cart serializer
class UserFrontEndCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['cart_id', 'user_id', 'session_id', 'created_at']

# FrontEnd Room Cart Show Details Serializer
class FrontEndRoomCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cart_details'] = UserFrontEndCartSerializer(instance.cart_id ).data
        response['room_details'] = FrontEndRoomSerializer(instance.room_id).data
        response['hotels'] = HotelDetailsFrontEndSingleSerializer(models.HotelDetails.objects.get(hotel_id=instance.room_id.hotel_id.hotel_id)).data
        return response

# FrontEnd Room Serializer
class FrontEndRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'hotel_id', 'room_name', 'room_no', 'price_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

# HotelDetailsFrontEndSingleSerializer
class HotelDetailsFrontEndSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name', 'latitude', 'longitude', 'city_id', 'image_galary_details_id', 'hotel_info', 'hotel_type']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city_id'] = CitySerializer(instance.city_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        return response

# FrontEnd Food Menu Cart Details Serializer
class FrontEndFoodMenuCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenuCartDetails
        fields = ['food_cart_details_id', 'cart_id', 'food_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cart_details'] = UserFrontEndCartSerializer(instance.cart_id ).data
        response['food_details'] = FrontEndFoodMenuSerializer(instance.food_id ).data
        return response

#  FrontEnd FoodMenu Serializer
class FrontEndFoodMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenu
        fields = ['food_menu_id', 'food_name', 'price_id', 'food_image']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

# FrontEnd Facilities Cart Details Serializer
class FrontEndFacilitiesCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesCartDetails
        fields = ['facilities_cart_details_id', 'cart_id', 'hotel_facilites_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cart_details'] = UserFrontEndCartSerializer(instance.cart_id ).data
        response['hotel_facilities_details'] = FrontEndHotelFacilitesSerializer(instance.hotel_facilites_id ).data
        return response

#  FrontEnd Hotel Facilites Serializer
class FrontEndHotelFacilitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelFacilites
        fields = ['hotel_facilites_id', 'facilites_id', 'price_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['facilites_details'] = FacilitesSerializer(instance.facilites_id).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

#  FrontEnd Package Cart Details Serializer
class FrontEndPackageCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackageCartDetails
        fields = ['package_cart_details_id', 'package_id', 'cart_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['cart_details'] = UserFrontEndCartSerializer(instance.cart_id ).data
        response['package_details'] = FrontEndPackageSerializer(instance.package_id ).data

        return response

#  FrontEnd package Serializer
class FrontEndPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = ['package_id', 'package_name', 'package_image', 'price_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

# User register android serializer
class UserRegisterAndroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        extra_kwargs = {'user_password': {'write_only': True}}

# User profile update android serializer
class UserProfileUpdateAndroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ["user_password"]
        extra_kwargs = {'user_password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# single User serializer
class SingleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ["user_password"]
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# UpdateRoomCartDetailsSerializer
class UpdateRoomCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        fields = ('room_cart_details_id', 'check_in_date', 'check_out_date', 'total_day', 'static_regular_price', 'static_offer_price')

# User login
class UserLoginAndroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['user_password']

# User profile photo change android serializer
class UserProfilePhotoUpdateAndroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["user_image"]

# recommended hotel details
class RecommendedHotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = "__all__"
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['city'] = CitySerializer(instance.city_id).data
        response['reviews'] = ReviewSerializer(models.Review.objects.filter(hotel_id__hotel_id = instance.hotel_id), many=True).data
        return response

class RoomDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name','room_no', 'image_galary_details_id', 'price_id','hotel_id','floor_id', 'allow_offer_percent', 'offer_discount_price']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['floor_details'] = FloorSerializer(instance.floor_id).data
        response['hotel_details'] = HotelRoomDealsSerializer(instance.hotel_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

# 24 Hours Deals Porzotok Serializer
class HotelRoomDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name', 'city_id']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['reviews'] = ReviewSerializer(models.Review.objects.filter(hotel_id__hotel_id = instance.hotel_id), many=True).data
        response['city'] = CitySerializer(instance.city_id).data
        return response

# releted Room Details 
class RelatedRoomDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name', 'room_no', 'room_status', 'room_description', 'price_id','is_deals']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        response['facilites_details'] = SingleRoomFacilitesGroupSerializer(models.FacilitesGroup.objects.filter(room_id__room_id=instance.room_id), many=True).data
        return response

# Single Room Details  
class SingleRoomDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name', 'room_no', 'room_status', 'room_description', 'price_id','is_deals']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        response['facilites_details'] = SingleRoomFacilitesGroupSerializer(models.FacilitesGroup.objects.filter(room_id__room_id=instance.room_id), many=True).data
        # response['related_rooms'] = RelatedRoomDetailsSerializer(models.Room.objects.filter(~Q(room_id=instance.room_id), hotel_id__city_id__city_name=instance.hotel_id.city_id.city_name, price_id__price__range=((instance.price_id.price - 5000), (instance.price_id.price + 5000))), many=True).data
        return response

# Single Room Facilites Group
class SingleRoomFacilitesGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesGroup
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['facilites_id'] = FacilitesSerializer(instance.facilites_id).data
        return response

# Hotel by City
class HotelByCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name','slug_name','hotel_info','image_galary_details_id', 'city_id']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['city'] = CitySerializer(instance.city_id).data
        return response

# Booking list
class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConfirmBooking
        fields = ['booking_id', 'booking_status', 'total_amount', 'created_at']

# single Booking details serializer 
class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConfirmBooking
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer_details'] = BookingDetailsCustomerSerializer(instance.user_id).data
        response['booking_information'] = CartRoomDetailsSerializer(models.RoomCartDetails.objects.filter(cart_id=instance.cart_id), many=True).data
        return response

# Booking Details Customer
class BookingDetailsCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_name', 'user_phone', 'user_short_address']
        extra_kwargs = {'user_image':{'required':False}}

# Room details Serializer
class CartRoomDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        exclude = ['is_hold', 'created_at']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['room_details'] = HotelDetailsInformationSerializer(instance.room_id).data
        return response

# Hotel Room Info Serializer
class HotelDetailsInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('room_id', 'room_name', 'room_no', 'hotel_id', 'image_galary_details_id')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = HotelInformationSerializer(instance.hotel_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        return response

# hotel information
class HotelInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'latitude', 'longitude', 'hotel_name', 'short_address', 'city_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# Booking
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        exclude = ['offer_id', 'hotel_discount_id', 'gift_card_id', 'cupon_id']
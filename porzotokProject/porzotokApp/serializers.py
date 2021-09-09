from rest_framework import serializers
from . import models

# hotel user type serializer
class HotelUserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserType
        fields = "__all__"
 
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



#HotelDiscount serializer
class HotelDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDiscount
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user'] = HotelUserOwnerSerializer(instance.hotel_user_owner_id).data
        response['offer_max_amount_id'] = OfferMaxAmountSerializer(instance.offer_max_amount_id).data
        return response


#Floor serializer
class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floor
        fields = "__all__"



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

# agent user serializer
class AgentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgentUser
        fields = '__all__'
        extra_kwargs = {'agent_user_password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# guide user serializer
class GuideUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GuideUser
        fields = '__all__'
        extra_kwargs = {'guide_password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# deffense user serializer
class DeffenseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeffenseUser
        fields = '__all__'
        extra_kwargs = {'deffense_password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# offer type serializer
class OfferTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OfferType
        fields = '__all__'

# offer max amount serializer
class OfferMaxAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OfferMaxAmount
        fields = '__all__'

# offer serializer
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['offer_type'] = OfferTypeSerializer(instance.offer_type_id).data
        response['offer_max_amount'] = OfferMaxAmountSerializer(instance.offer_max_amount_id).data
        return response



# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {'user_image':{'required':False}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# User login android serializer
class UserLoginAndroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['user_password']

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

# User profile photo change android serializer
class UserProfilePhotoUpdateAndroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["user_image"]

# User serializer
class SingleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ["user_password"]
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# GiftCard serializer
class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GiftCard
        fields = '__all__'

#Event serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


#Event details serializer
class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventDetails
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_id'] = UserSerializer(instance.user_id).data
        response['event_id'] = EventSerializer(instance.event_id).data
        return response


#Payment serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = "__all__"

#Cupon
class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cupon
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['offer_max_amount_id'] = OfferMaxAmountSerializer(instance.offer_max_amount_id).data
        return response




#ImageGalaryDetails serializer
class ImageGalaryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageGalaryDetails
        fields = '__all__'

#Image serializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'

#TouristSpot serializer
class TouristSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TouristSpot
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_galary_details_id'] = ImageGalaryDetailsSerializer(instance.image_galary_details_id).data
        response['city'] = CitySerializer(instance.city_id).data
        return response


#Price serializer
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        fields = '__all__'



#Room Serializer
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['floor_id'] = FloorSerializer(instance.floor_id).data
        response['hotel_id'] = HotelDetailsSerializer(instance.hotel_id).data
        response['image_galary_details_id'] = ImageGalaryDetailsSerializer(instance.image_galary_details_id).data
        response['price_id'] = PriceSerializer(instance.price_id).data
        response['hotel_discount_id'] = HotelDiscountSerializer(instance.hotel_discount_id).data
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

# Single Room Details Serializer 
class SingleRoomDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name', 'room_no', 'room_status', 'room_description', 'price_id','is_deals']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        response['facilites_details'] = SingleRoomFacilitesGroupSerializer(models.FacilitesGroup.objects.filter(room_id__room_id=instance.room_id), many=True).data
        return response


#FoodMenu Serializer
class FoodMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenu
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_id'] = HotelDetailsSerializer(instance.hotel_id).data
        response['price_id'] = PriceSerializer(instance.price_id).data
        return response

#Package Serializer
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response       

#RoomPackage Serializer
class RoomPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomPackage
        fields = "__all__"

#FoodMenuPackage Serializer
class FoodMenuPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenuPackage
        fields = "__all__"

#FacilitesPackage Serializer
class FacilitesPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesPackage
        fields = "__all__"

#TouristSpotPackage Serializer
class TouristSpotPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TouristSpotPackage
        fields = "__all__"


#PackageDetails Serializer
# class PackageDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.PackageDetails
#         fields = "__all__"

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['package'] = PackageSerializer(instance.package_id).data
#         response['price_details'] = PriceSerializer(instance.price_id).data
#         response['room_details'] = RoomSerializer(instance.room_id).data
#         response['food_menu_details'] = FoodMenuSerializer(instance.food_menu_id).data
#         response['facilites_details'] = FacilitesSerializer(instance.facilites_id).data
#         response['tourist_details'] = TouristSpotSerializer(instance.tourist_spot_id).data
#         return response



#Facilites Serializer
class FacilitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Facilites
        fields = "__all__"


#FacilitesGroupSerializer
class FacilitesGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesGroup
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['room_id'] = RoomSerializer(instance.room_id).data
        response['facilites_id'] = FacilitesSerializer(instance.facilites_id).data
        return response

# Single Room Facilites Group Serializer
class SingleRoomFacilitesGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesGroup
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['facilites_id'] = FacilitesSerializer(instance.facilites_id).data
        return response



#Hotel Facilites Serializer
class HotelFacilitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelFacilites
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = HotelDetailsSerializer(instance.hotel_id).data
        response['facilites_details'] = FacilitesSerializer(instance.facilites_id).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

# recommended hotel details serializer
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

#Booking serializer 
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        exclude = ['offer_id', 'hotel_discount_id', 'gift_card_id', 'cupon_id']

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['room_id'] = RoomSerializer(instance.room_id).data
    #     response['cupon_id'] = CuponSerializer(instance.cupon_id).data
    #     response['offer_id'] = OfferSerializer(instance.offer_id).data
    #     # response['hotel_discount_id'] = HotelDiscountSerializer(instance.hotel_discount_id).data
    #     return response




# Cart serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


#RoomCartDetails Serializer
class RoomCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        fields = "__all__"
        extra_kwargs = {'check_in_date':{'required':False},'check_out_date':{'required':False}, 'total_day':{'required':False}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['room_details'] = HotelDetailsFrontEndSingleRoomSerializer(instance.room_id).data
        return response


#FoodMenuCartDetails Serializer
class FoodMenuCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenuCartDetails
        fields = "__all__"


#FacilitesCartDetails Serializer
class FacilitesCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesCartDetails
        fields = "__all__"


#PackageCartDetails Serializer
class PackageCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackageCartDetails
        fields = "__all__"


#Invoice serializer
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Invoice
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['booking_id '] = BookingSerializer(instance.booking_id ).data
        return response



#Review serializer
# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Review
#         fields = '__all__'

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['booking_id'] = BookingSerializer(instance.booking_id).data
#         return response


#ReviewReplay serializer
# class ReviewReplaySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ReviewReplay
#         fields = '__all__'

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['review_id '] = ReviewSerializer(instance.review_id).data
#         return response




#ReportType serializer
class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReportType
        fields = '__all__'




#Report serializer
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_id'] = UserSerializer(instance.user_id).data
        response['report_type_id '] = ReportTypeSerializer(instance.report_type_id).data
        return response



#Affiliate serializer
class AffiliateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Affiliate
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_id'] = UserSerializer(instance.user_id).data
        response['booking_id'] = BookingSerializer(instance.booking_id).data
        return response


#MembarshipCard serializer
class MembarshipCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MembarshipCard
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_id'] = UserSerializer(instance.user_id).data
        response['booking_id'] = BookingSerializer(instance.booking_id).data
        return response



#History serializer
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.History
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_id'] = UserSerializer(instance.user_id).data
        response['hotel_user_type'] = HotelUserTypeSerializer(instance.hotel_user_type_id).data
        return response

#Biling Adress serializer
class BilingAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BilingAdress
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['payment_method_id'] = PaymentSerializer(instance.payment_method_id).data
        return response

#Transaction Details serializer
class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TransactionDetails
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['payment_method_id'] = PaymentSerializer(instance.payment_method_id).data
        return response


#Twenty Four Hours Deals Porzotok Serializer
class TwentyFourHoursDealsPorzotokSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TwentyFourHoursDealsPorzotok
        fields = "__all__"
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        return response
#Twenty Four Hours Deals Serializer Hotel
class TwentyFourHoursDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TwentyFourHoursDeals
        fields = "__all__"
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['room_details'] = RoomSerializer(instance.room_id).data
        response['twenty_four_hours_deals_porzotok_details'] = TwentyFourHoursDealsPorzotokSerializer(instance.twenty_four_hours_deals_porzotok_id).data
        return response

#Start 24 Hours Deals Porzotok Serializer
class HotelRoomDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name', 'city_id']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['reviews'] = ReviewSerializer(models.Review.objects.filter(hotel_id__hotel_id = instance.hotel_id), many=True).data
        response['city'] = CitySerializer(instance.city_id).data
        return response
class RoomDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name','room_no', 'image_galary_details_id', 'price_id','hotel_id','floor_id', 'allow_offer_percent', 'offer_discount_price']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['floor_details'] = FloorSerializer(instance.floor_id).data
        response['hotel_details'] = HotelRoomDealsSerializer(instance.hotel_id).data
        #response['image_galary_details_id'] = ImageGalaryDetailsSerializer(instance.image_galary_details_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response
#END 24 Hours Deals Porzotok Serializer

#Hotel by City  Serializer
class HotelByCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name','slug_name','hotel_info','image_galary_details_id', 'city_id']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['city'] = CitySerializer(instance.city_id).data
        return response
#Hotel by City  Serializer
#Hotel by State  Serializer
class HotelByCityStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ['city_id', 'city_name','state_id']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['state_details'] = StateSerializer(instance.state_id).data
        return response
class HotelByStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name','slug_name','hotel_info','image_galary_details_id', 'city_id']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['city'] = HotelByCityStateSerializer(instance.city_id).data
        return response
#Hotel by State  Serializer

""" start booking list and details api"""
# hotel information api for android
class HotelInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'latitude', 'longitude', 'hotel_name', 'short_address', 'city_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# Hotel Room Info Serializer for android api
class HotelDetailsInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('room_id', 'room_name', 'room_no', 'hotel_id', 'image_galary_details_id')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = HotelInformationSerializer(instance.hotel_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        return response

# Room details Serializer for android api
class CartRoomDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        exclude = ['is_hold', 'created_at']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['room_details'] = HotelDetailsInformationSerializer(instance.room_id).data
        return response

# Booking Details Customer Serializer for android api
class BookingDetailsCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_name', 'user_phone', 'user_short_address']
        extra_kwargs = {'user_image':{'required':False}}

# Booking list serializer 
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

""" end booking list and details api"""

# Check Room Availability Serializer 
class CheckRoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        fields = '__all__'

# get search keyword Serializer 
class SearchKeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecentSearch
        fields = ['keyword']

#UpdateRoomCartDetailsSerializer for android
class UpdateRoomCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        fields = ('room_cart_details_id', 'check_in_date', 'check_out_date', 'total_day', 'static_regular_price', 'static_offer_price')

'''
    * START
    * Porzotok FrontEnd Serializer
    * All frontend serializer for porzotok website start from here
''' 

#HotelDetailsFrontEndSingleSerializer
class HotelDetailsFrontEndSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name', 'latitude', 'longitude', 'city_id', 'image_galary_details_id', 'hotel_info', 'hotel_type']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city_id'] = CitySerializer(instance.city_id).data
        response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        return response

#HotelFacilitesFrontEndSerializer
class HotelFacilitesFrontEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelFacilites
        fields = ['hotel_facilites_id', 'facilites_id', 'hotel_id', 'price_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['facilites_details'] = FacilitesSerializer(instance.facilites_id).data
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

#FacilitesGroupSerializerFront
class FacilitesGroupSerializerFront(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesGroup
        fields = ("facilites_id", "facilites_group_id",)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['facilites_id'] = FacilitesSerializer(instance.facilites_id).data
        return response

#HotelDetailsFrontEndSingleRoomSerializer
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


#HotelInfoFrontEndRoomSerializer
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

# FrontEnd User Serializer
class UserFrontEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_id', 'user_name']
        extra_kwargs = {'user_image':{'required':False}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response

# FrontEnd Cart serializer
class UserFrontEndCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['cart_id', 'user_id', 'session_id', 'created_at']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['user_details'] = UserFrontEndSerializer(instance.user_id ).data
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

#  FrontEnd FoodMenu Serializer
class FrontEndFoodMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenu
        fields = ['food_menu_id', 'food_name', 'price_id', 'food_image']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = PriceSerializer(instance.price_id).data
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

#  FrontEnd package Serializer
class FrontEndPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = ['package_id', 'package_name', 'package_image', 'price_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response

# FrontEnd Checkout page cart Room with hotel Serializer
# class FrontEndRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Room
#         fields = ['room_id', 'hotel_id', 'room_name', 'room_no', 'price_id']

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['image_url'] = ImageSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
#         response['price_details'] = PriceSerializer(instance.price_id).data
#         response['hotels'] = PriceSerializer(instance.price_id).data
#         return response

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


# frontend search hotel details serializer
class FrontEndSearchHotelDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelDetails
        fields = ['hotel_name']

# frontend search city serializer
class FrontEndSearchCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = ['city_id', 'city_name']

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

# Front end search page Price serializer
class FrontEndSearchPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        fields = ['price_id', 'price', 'offer_price']

# Search page front end hotels with room price serializer
class HotelDetailsFrontEndSearchRoomPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('room_id', 'is_deals', 'price_id')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = FrontEndSearchPriceSerializer(instance.price_id).data
        return response

# frontend search hotel details serializer
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

# FrontEnd checkout page User details Serializer
class UserDetailsCheckoutFrontEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['user_password']
        extra_kwargs = {'user_image':{'required':False}}


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city'] = CitySerializer(instance.city_id).data
        return response


#HotelFoodMenuFrontEndSerializer
class HotelFoodMenuFrontEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodMenu
        fields = ['food_menu_id', 'food_name', 'hotel_id', 'price_id','food_image']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price_details'] = PriceSerializer(instance.price_id).data
        return response


#Start Review Serializer
class UsersReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_id','user_name', 'user_image']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = "__all__"
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_details'] = UsersReviewSerializer(instance.user_id).data
        response['replay'] = ReviewReplaySerializer(models.ReviewReplay.objects.filter(review_id = instance.review_id), many=True).data
        return response
class FrontEndHotelLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FrontEndHotelLogo
        fields = "__all__"
class ReviewReplayHotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id','hotel_name']

class ReviewReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewReplay
        fields = "__all__"
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = ReviewReplayHotelDetailsSerializer(instance.hotel_id).data
        response['photo_details'] = FrontEndHotelLogoSerializer(instance.logo_id).data
        return response

class BookingReviewBoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookingReviewBool
        fields = "__all__"
#End Review Serializer


# Map Serializer
class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ["hotel_id", "latitude", "longitude"]

'''
    * END 
    * Porzotok FrontEnd Serializer
    * All frontend serializer for porzotok website end
''' 
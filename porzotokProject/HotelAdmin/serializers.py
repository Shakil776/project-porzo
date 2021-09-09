from rest_framework import serializers
from porzotokApp import models
from porzotokApp import serializers as appserializers



# country serializer
class CountryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'

# state serializer
class StateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['country_details'] = CountryAdminSerializer(instance.country_id).data
        return response

# city serializer
class CityAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['state_details'] = StateAdminSerializer(instance.state_id).data
        return response




#ImageGalaryDetails serializer
class ImageGalaryDetailsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageGalaryDetails
        fields = '__all__'



#Image serializer
class ImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'



# hotel user type serializer
class HotelUserTypeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserType
        fields = "__all__"


# hotel user owner serializer
class HotelUserOwnerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserOwner
        fields = "__all__"
        extra_kwargs = {'hotel_user_password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_type_details'] = HotelUserTypeAdminSerializer(instance.hotel_user_type_id).data
        return response


# offer max amount serializer
class OfferMaxAmountAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OfferMaxAmount
        fields = '__all__'


class HotelDiscountAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDiscount
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_owner_details'] = HotelUserOwnerAdminSerializer(instance.hotel_user_owner_id).data
        # response['offer_max_amount_details'] = OfferMaxAmountAdminSerializer(instance.offer_max_amount_id).data
        return response

#Hotel Details Admin Serializer
class HotelDetailsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_details'] = HotelUserOwnerAdminSerializer(instance.hotel_user_id).data
        response['image_url'] = ImageAdminSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
        response['city_details'] = CityAdminSerializer(instance.city_id).data
        return response




#Price serializer
class PriceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        fields = '__all__'


#Floor serializer
class FloorHotelAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floor
        fields = "__all__"



class RoomHotelAdminSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = "__all__"

        # exclude = ('hotel_discount_id', )
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['price'] = PriceAdminSerializer(instance.price_id).data
    #     response['hotel_discount_details'] = RoomDiscountSerializer(instance.hotel_discount_id).data
    #     return response

#Room Serializer
class RoomHotelAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = "__all__"
        extra_kwargs = {'deal_start_date':{'required':False}, 'allow_offer_percent':{'required':False}, 'offer_discount_price':{'required':False}, 'hotel_discount_id':{'required':False}}
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['price'] = PriceAdminSerializer(instance.price_id).data
        response['hotel_details'] = TwentyFourHoursDealsListHotelNameSerializer(instance.hotel_id).data
        response['hotel_discount_details'] = RoomDiscountSerializer(instance.hotel_discount_id).data
        return response




#Facilites Serializer
class FacilitesAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Facilites
        fields = "__all__"


#Hotel Room Admin Facilites Serializer
class HotelRoomAdminFacilitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FacilitesGroup
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['room_details'] = RoomHotelAdminSerializer(instance.room_id).data
        response['facilites_details'] = FacilitesAdminSerializer(instance.facilites_id).data
        return response



class HotelAdminFacilitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelFacilites
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = HotelDetailsAdminSerializer(instance.hotel_id).data
        response['facilites_details'] = appserializers.FacilitesSerializer(instance.facilites_id).data
        response['price'] = PriceAdminSerializer(instance.price_id).data
        return response





# #Twenty Four Hours Deals Porzotok Hotel Admin Serializer
# class TwentyFourHoursDealsPorzotokHotelAdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.TwentyFourHoursDealsPorzotok
#         fields = "__all__"

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['image_url'] = ImageAdminSerializer(models.Image.objects.filter(image_galary_details_id = instance.image_galary_details_id), many=True).data
#         return response





# class TwentyFourHoursDealsHotelAdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.TwentyFourHoursDeals
#         fields = "__all__"

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['room_details'] = RoomHotelAdminSerializer(instance.room_id).data
#         response['twenty_four_hours_deals_porzotok_details'] = TwentyFourHoursDealsPorzotokHotelAdminSerializer(instance.twenty_four_hours_deals_porzotok_id).data
#         return response






#HotelDetailsFrontEndSingleSerializer
class HotelNameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name']





class HotelDiscountListAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDiscount
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_owner_details'] = HotelUserOwnerAdminSerializer(instance.hotel_user_owner_id).data
        response['offer_max_amount_details'] = OfferMaxAmountAdminSerializer(instance.offer_max_amount_id).data
        return response


class RoomDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDiscount
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_owner_details'] = HotelUserOwnerAdminSerializer(instance.hotel_user_owner_id).data
        response['offer_max_amount_details'] = OfferMaxAmountAdminSerializer(instance.offer_max_amount_id).data
        return response




class RoomHotelAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name','hotel_id', 'room_no', 'floor_id','room_status','price_id','hotel_discount_id','is_active']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['floor_details'] = appserializers.FloorSerializer(instance.floor_id).data
        response['price_details'] = PriceAdminSerializer(instance.price_id).data
        response['hotel_discount_details'] = RoomDiscountSerializer(instance.hotel_discount_id).data
        response['hotel_details'] = HotelNameRoomSerializer(instance.hotel_id).data
        return response






#TwentyFourHoursDealsListHotelName
class TwentyFourHoursDealsListHotelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name']


class TwentyFourHoursDealsListRoomNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name', 'room_no', 'hotel_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = TwentyFourHoursDealsListHotelNameSerializer(instance.hotel_id).data
        return response




class TwentyFourHoursDealsListRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name', 'room_no', 'hotel_id', 'price_id', 'is_deals', 'offer_discount_price']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = TwentyFourHoursDealsListHotelNameSerializer(instance.hotel_id).data
        response['price_details'] = PriceAdminSerializer(instance.price_id).data
        return response






# class TwentyFourHoursDealsListHotelAdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Room
#         fields = ['room_id', 'room_name', 'room_no', 'hotel_id','room_status','price_id','is_deals']

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['room_details'] = TwentyFourHoursDealsListRoomNameSerializer(instance.room_id).data
#         response['twenty_four_hours_deals_porzotok_details'] = TwentyFourHoursDealsPorzotokHotelAdminSerializer(instance.twenty_four_hours_deals_porzotok_id).data
#         return response




class HotelUserPhotoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserPhoto
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_owner_details'] = appserializers.HotelUserOwnerSerializer(instance.hotel_user_owner_id).data
        return response



class HotelUserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserOwner
        fields = "__all__"



class HotelUserLogoListAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserPhoto
        fields = ['photo_id', 'logo_photo', 'hotel_user_owner_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_owner_details'] = appserializers.HotelUserOwnerSerializer(instance.hotel_user_owner_id).data
        return response

class HotelUserBannerListAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserPhoto
        fields = ['photo_id', 'banner_photo', 'hotel_user_owner_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_user_owner_details'] = appserializers.HotelUserOwnerSerializer(instance.hotel_user_owner_id).data
        return response







#Start Room Booking Serializer

class RoomUserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_id','user_name']

class RoomCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        #fields = '__all__'
        fields = ['cart_id','user_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_details'] = RoomUserCartSerializer(instance.user_id).data
        response['books'] = RoomBookingSerializer(models.Booking.objects.filter(cart_id__cart_id = instance.cart_id), many=True).data
        #response['room_carts'] = HotelRoomCartSerializer(models.RoomCartDetails.objects.filter(cart_id__cart_id = instance.cart_id), many=True).data
        return response


class HotelRoomCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        #response['cart_details'] = RoomCartSerializer(instance.cart_id).data
        #response['cart_b_details'] = RoomCartSerializer(models.Booking.objects.filter(cart_id=instance.cart_id), many=True).data
        response['room_details'] = CartRoomSerializer(instance.room_id).data
        return response




class HotelCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDetails
        fields = ['hotel_id', 'hotel_name']



class CartRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name', 'room_no','hotel_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hotel_details'] = HotelCartSerializer(instance.hotel_id).data
        return response



class HotelRoomCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCartDetails
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cart_details'] = RoomCartSerializer(instance.cart_id).data
        #response['cart_b_details'] = RoomCartSerializer(models.Booking.objects.filter(cart_id=instance.cart_id), many=True).data
        response['room_details'] = CartRoomSerializer(instance.room_id).data
        return response

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = '__all__'

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['cartb_details'] = RoomCartSerializer(instance.cart_id).data
#         #response['cart_b_details'] = RoomCartSerializer(models.Booking.objects.filter(cart_id=instance.cart_id), many=True).data
#         #response['room_details'] = CartRoomSerializer(instance.room_id).data
#         return response






# Start Confirm Booking Serializer

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_id','user_name']



class BookingHotelRoomCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConfirmBooking
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_details'] = AdminUserSerializer(instance.user_id).data
        return response

#End Confirm Booking Serializer




#Start Hotel User Serializer

class HotelUserProfileAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserOwner
        fields = ['hotel_user_owner_id','hotel_name', 'hotel_owner_name', 'hotel_owner_national_id_card','hotel_user_email','hotel_user_phone','gendar','city_id','hotel_user_type_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['city_details'] = CityAdminSerializer(instance.city_id).data
        response['hotel_user_type_details'] = HotelUserTypeAdminSerializer(instance.hotel_user_type_id).data
        return response


class HotelUserProfileUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelUserOwner
        fields = '__all__'


#End Hotel User Serializer

class DiscountRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelDiscount
        fields = ['hotel_discount_id', 'hotel_discount_name']

#HotelRoomsGetSerializer
class HotelRoomsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name', 'allow_offer_percent', 'hotel_discount_id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['discount'] = DiscountRoomSerializer(instance.hotel_discount_id).data
        return response

#FacilitiesRoomsSerializer
class FacilitiesRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['room_id', 'room_name']


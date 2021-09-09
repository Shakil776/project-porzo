from django.urls import path, include
from rest_framework.routers import DefaultRouter
from porzotokApp import views
# Create a router and register our viewsets with it.
router = DefaultRouter()
# hotel-user-type
router.register('hotel-user-type', views.HotelUserTypeViewSet, basename='hotel_user_type')
# hotel-user-owner
router.register('hotel-user-owner', views.HotelUserOwnerViewSet, basename='hotel_user_owner')
# hotel-detail
router.register("hotel_details",views.HotelDetailViewSet,basename="hotel_details")
# country
router.register('country', views.CountryAPIView)
# state
router.register('state', views.StateAPIView)
# city
router.register('city', views.CityAPIView)
# agent user
router.register('agent', views.AgentUserViewSet, basename='agent')
# Guide user
router.register('guide', views.GuideUserViewSet, basename='guide')
# Deffense user
router.register('deffense', views.DeffenseUserViewSet, basename='deffense')
# offer type
router.register('offer-type', views.OfferTypeViewSet, basename='offer-type')
# offer max amount
router.register('offer-max-amount', views.OfferMaxAmountViewSet, basename='offer-max-amount')
# offer
router.register('offer', views.OfferViewSet, basename='offer')
# User
router.register('user', views.UserViewSet, basename='user')
# User
router.register('user-login', views.UserLoginAndroidViewSet, basename='user_login')
#GiftCard
router.register('giftcard', views.GiftCardViewSet, basename='giftcard')
#Event
router.register('event', views.EventViewSet, basename='event')
#EventDetails
router.register('eventdetails', views.EventDetailsViewSet, basename='eventdetails')
#Payment
router.register("payment",views.PaymentViewSet,basename="payment")
#HotelDiscount
router.register('hotel-discount', views.HotelDiscountViewSet, basename='hotel-discount')
#Cupon
router.register('cupon', views.CuponViewSet, basename='cupon')
#TouristSpot
router.register('tourist-spot', views.TouristSpotViewSet, basename='tourist_spot')
#Price
router.register("price",views.PriceViewSet,basename="price")
#ImageGalaryDetails
router.register('image-galary-details', views.ImageGalaryDetailsAPIView)
#Image
router.register('image', views.ImageAPIView, basename="image")
#Floor
router.register("floor",views.FloorViewSet,basename="floor")
#Room
router.register("room",views.RoomViewSet,basename="room")
#CheckBookingDate
router.register("check-booking-date",views.CheckBookingDate,basename="check_booking_date")

# Single Room Details
router.register("single-room",views.SingleRoomDetailsViewSet,basename="single_room")
#FoodMenu
router.register('food-menu', views.FoodMenuViewSet, basename='food-menu')
#Package
router.register('package', views.PackageViewSet, basename='package')
#Facilites
router.register("facilites",views.FacilitesViewSet,basename="facilites")
#FacilitesGroup
router.register('facilites-group', views.FacilitesGroupViewSet,basename="facilites-group")
#Hotel Facilites
router.register('hotelfacilites', views.HotelFacilitesViewSet,basename="hotelfacilites")
# Book
router.register('book', views.BookViewSet, basename='book')
# cart 
router.register('carts', views.CartModelViewSet, basename='carts')
# cart by user android 
router.register('cart-user', views.CartByUserModelViewSet, basename='cart_user')
# cart details
router.register('cart-details', views.CartDetailsModelViewSet, basename='cart-details')
#Invoice
router.register('invoice', views.InvoiceViewSet, basename='invoice')
#Review
router.register('review', views.ReviewViewSet, basename='review')
#BookingReviewBoolViewSet
router.register('review-bool', views.BookingReviewBoolViewSet, basename='review-bool')
#ReviewReplay
router.register('review-replay', views.ReviewReplayViewSet, basename='review-replay')
#ReportType
router.register('report-type', views.ReportTypeViewSet, basename='report-type')
#ReportType
router.register('report', views.ReportViewSet, basename='report')
#Affiliate
router.register('affiliate', views.AffiliateAPIView)
#History
router.register('history', views.HistoryViewSet, basename='history')
#MembarshipCard
router.register('membarship-card', views.MembarshipCardViewSet, basename='membarship-card')
# billing address
router.register('biling-address', views.BilingAdressViewSet, basename='biling-address')
#TransactionDetails
router.register('transaction-details', views.TransactionDetailsViewSet, basename='transaction-details')
#router.register('transaction-details', views.TransactionDetailsViewSet, basename='transaction-details')
#TwentyFourHoursDealsPorzotokViewSet URLS
router.register('porzotok-deals', views.TwentyFourHoursDealsPorzotokViewSet, basename='porzotok-deals')
#TwentyFourHoursDealsViewSet URLS
router.register('hotel-deals', views.TwentyFourHoursDealsViewSet, basename='hotel-deals')
#TwentyFourHoursDealsRoomViewSet
# router.register('room-deals', views.TwentyFourHoursDealsRoomViewSet, basename='room-deals')
#Hotel By City View
router.register('hotel-by-city', views.HotelByCityViewSet, basename='hotel_by_city')
#Hotel By State View
router.register('hotel-by-state', views.HotelByStateViewSet, basename='hotel_by_state')
# Booking Details
router.register('booking-details', views.BookingDetailsViewSet, basename='booking_details')
# chcek room availability
router.register('check-room-availablity', views.CheckRoomAvailablityViewSet, basename='check_room_availablity')
# get user search keyword
router.register('recent-search-key', views.SearchKeyWordViewSet, basename='recent_search_key')
# check user active or deactive status
router.register("check-user-status",views.CheckUserStatusViewSet, basename="check_user_status")
# recommended hotel api for android
router.register("recommended-hotels",views.RecommendedHotelViewSet, basename="recommended_hotels")
# change user password api for android
router.register("change-user-password", views.ChangeUserPasswordViewSet, basename="change_user_password")
# user profile photo update api for android
router.register("user-profile-photo", views.UpdateUserProfilePhotoViewSet, basename="user_profile_photo")
# user profile photo update api for web site
router.register("profile-photo-change", views.ChangeUserProfilePhotoViewSet, basename="profile_photo_change")
#map
router.register('map', views.MapViewSet, basename='map')
# otp
router.register('otp', views.OTPViewSet, basename='otp')
"""
	* FRONTEND URLS START
"""
# Single Hotel Details FrontEnd API URLS
router.register('single-hotel-details', views.SingleHotelDetailsFrontEndViewSet, basename='single-hotel-details')

# user cart details 
router.register('user-cart-details', views.UserCartDetailsModelViewSet, basename='user-cart-details')

# home page autocomplete search API urls 
router.register('search', views.SearchModelViewSet, basename="search"),
# search result details page API urls
router.register('search-result', views.SearchResultModelViewSet, basename="search_result"),
# user details in frontend checkout page 
router.register('user-details', views.UserDetailsFrontEndModelViewSet, basename="user_details"),
router.register('hotels', views.ListOfHotelsModelViewSet, basename="hotels_list"),
# check in time update frontend 
# router.register('check-in-out-update', views.CheckInOutTimeUpdateViewSet, basename='check_in_out_update')

"""
	* FRONTEND URLS END
"""
urlpatterns = [
    # API view Route
	path('api/', include(router.urls)),
	# Agent user by name
	path('api/agentbyname/<str:name>', views.AgentByNameViewSet.as_view(), name="agentbyname"),
	# Agent user by email
	path('api/agentbyemail/<str:email>', views.AgentByEmailViewSet.as_view(), name="agentbyemail"),
	# Agent user by phone
	path('api/agentbyphone/<str:phone>', views.AgentByPhoneViewSet.as_view(), name="agentbyphone"),
	# user by name
	path('api/userbyname/<str:name>', views.UserByNameViewSet.as_view(), name="userbyname"),
	# user by email
	path('api/userbyemail/<str:email>', views.UserByEmailViewSet.as_view(), name="userbyemail"),
	# user by phone
	path('api/userbyphone/<str:phone>', views.UserByPhoneViewSet.as_view(), name="userbyphone"),
	# get state by country
	path('api/state_by_country/<int:c_id>', views.GetStateByCountry.as_view(), name="state_by_country"),
	# get city by state
	path('api/city_by_state/<int:s_id>', views.GetCityByState.as_view(), name="city_by_state"),
	# front end search urls
	# Twenty Four Hours Deals Room list with pagination
    path('api/room-deals/', views.TwentyFourHoursDealsAPIView.as_view(), name='room_deals'),
    # Single hotel all images list with pagination
    path('api/hotel-images/', views.HotelImagesAPIView.as_view(), name='hotel_images'),
    # Single room all images list with pagination
    path('api/room-images/', views.RoomImagesAPIView.as_view(), name='room_images'),
]
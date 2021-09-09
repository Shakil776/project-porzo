from django.urls import path, include
from rest_framework.routers import DefaultRouter
from androidAPI_V1 import views
# Create a router and register our viewsets with it.
router = DefaultRouter()


# country
router.register('country', views.CountryAPIView)
# state
router.register('state', views.StateAPIView)
# city
router.register('city', views.CityAPIView)
# hotel-details
router.register("hotel_details", views.HotelDetailViewSet, basename="hotel_details")
# autocomplete search
router.register('search', views.SearchModelViewSet, basename="search")
# search result
router.register('search-result', views.SearchResultModelViewSet, basename="search_result")
# user recent search keyword
router.register('recent-search-key', views.SearchKeyWordViewSet, basename='recent_search_key')
# Single Hotel Details
router.register('single-hotel-details', views.SingleHotelDetailsFrontEndViewSet, basename='single_hotel_details')
# cart by user
router.register('cart-user', views.CartByUserModelViewSet, basename='cart_user')
# save cart 
router.register('carts', views.CartModelViewSet, basename='carts')
# save cart details
router.register('cart-details', views.CartDetailsModelViewSet, basename='cart_details')
# get user cart details 
router.register('user-cart-details', views.UserCartDetailsModelViewSet, basename='user_cart_details')
# User
router.register('user', views.UserViewSet, basename='user')
# User login
router.register('user-login', views.UserLoginAndroidViewSet, basename='user_login')
# change user password
router.register("change-user-password", views.ChangeUserPasswordViewSet, basename="change_user_password")
# user profile photo update
router.register("user-profile-photo", views.UpdateUserProfilePhotoViewSet, basename="user_profile_photo")
# get Review
router.register('review', views.ReviewViewSet, basename='review')
# recommended hotel
router.register("recommended-hotels",views.RecommendedHotelViewSet, basename="recommended_hotels")
# check user active or deactive status
router.register("check-user-status", views.CheckUserStatusViewSet, basename="check_user_status")
# Single Room Details
router.register("single-room", views.SingleRoomDetailsViewSet, basename="single_room")
# Hotel By City
router.register('hotel-by-city', views.HotelByCityViewSet, basename='hotel_by_city')
# Booking Details
router.register('booking-details', views.BookingDetailsViewSet, basename='booking_details')
# Booking
router.register('book', views.BookViewSet, basename='book')

urlpatterns = [
	path('api/v1/', include(router.urls)),
	# Twenty Four Hours Deals Room list with pagination
    path('api/v1/room-deals/', views.TwentyFourHoursDealsAPIView.as_view(), name='room_deals'),
    # Single hotel all images list with pagination
    path('api/v1/hotel-images/', views.HotelImagesAPIView.as_view(), name='hotel_images'),
    # Single room all images list with pagination
    path('api/v1/room-images/', views.RoomImagesAPIView.as_view(), name='room_images'),
]
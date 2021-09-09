from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'HotelAdmin'

router = DefaultRouter()
#HotelDetailAdminViewSet
router.register('hotel-admin-details', views.HotelDetailAdminViewSet, basename='hotel-admin-details')
#RoomHotelAdminViewSet
router.register('add-room-hotel-admin', views.RoomHotelAdminViewSet, basename='add-room-hotel-admin')
#HotelRoomAdminFacilitesViewSet
router.register('room-facilites', views.HotelRoomAdminFacilitesViewSet, basename='room-facilites')

#HotelAdminFacilitesViewSet
router.register('hotels-facilites', views.HotelAdminFacilitesViewSet, basename='hotels-facilites')
#TwentyFourHoursDealsHotelAdminSerializerViewSet
router.register('deals-hotels', views.TwentyFourHoursDealsHotelAdminSerializerViewSet, basename='deals-hotels')
#HotelDiscountAdminViewSet
router.register('discount-hotel', views.HotelDiscountAdminViewSet, basename='discount-hotel')
# get all rooms for a hotel
router.register('get-hotel-room', views.GetHotelRoomsViewSet, basename='get_hotel_room')
# get all hotels rooms facilities for a hotel
router.register('get-hotel-room-facilities-room', views.GetFacilitiesRoomsViewSet, basename='get_hotel_room')
# country
router.register('country', views.CountryAdminAPIView)
# state
router.register('state', views.StateAdminAPIView)
# city
router.register('city', views.CityAdminAPIView)
#Create Price
router.register('add-price', views.CreatePriceViewSet, basename='add-price')
#Create Offer Max Amount ViewSet
router.register('add-offer-max', views.CreateOfferMaxAmountViewSet, basename='add-offer-max')
#HotelUserPhotoAdminViewSet
router.register('hotel-user-photo', views.HotelUserPhotoAdminViewSet, basename='hotel_user_photo')
#HotelUserOwnarAdminViewSet
router.register('hotel-user-name', views.HotelUserOwnarAdminViewSet, basename='hotel-user-name')
#HotelUserProfileAdminViewSet
router.register('profile-user', views.HotelUserProfileAdminViewSet, basename='profile-user')
#RoomBookingAdminViewSet
# router.register('booking-list', views.RoomBookingAdminViewSet, basename='booking_list')

########## Start Search API for all list ##########
# Room
router.register('room-search', views.HotelAdminSearchViewSet, basename='room_search')
# Hotel Facilities
router.register('hotel-facilities-search', views.HotelFacilitiesSearchViewSet, basename='hotel_facilities_search')
# Hotel room Facilities
router.register('hotel-room-facilities-search', views.HotelRoomFacilitiesSearchViewSet, basename='hotel_room_facilities_search')
# 24 hour deals room
router.register('deals-room-search', views.Hotel24HourDealsSearchViewSet, basename='deals_room_search')
# hotel discount 
router.register('hotel-discount-search', views.HotelDiscountSearchViewSet, basename='hotel_discount_search')
# single booking 
# router.register('single-booking-search', views.HotelSingleBookingSearchViewSet, basename='single_booking_search')
# booking details 
# router.register('booking-details-search', views.HotelBookingDetailsSearchViewSet, basename='booking_details_search')
########## Start Search API for all list ##########



urlpatterns = [
    # Login View
    path('admin-api/', include(router.urls)),
    #HotelDashboard
    path('hotel-admin/', views.HotelDashboard.as_view(), name='hotel_dashboard'),
    #HotelLoginView
    path('hotel-admin/login/', views.HotelLoginView.as_view(), name='login'),
    #Logout
    path('hotel-admin/logout/', views.Logout.as_view(), name='logout'),
    #AdminRoomView
    path('hotel-admin/add-room/', views.AdminRoomView.as_view(), name='add-room'),
    #AdminRoomListView
    path('hotel-admin/list-room/', views.AdminRoomListView.as_view(), name='list-room'),
    #AdminFacilitesView
    path('hotel-admin/add-facilites/', views.AdminFacilitesView.as_view(), name='add-facilites'),
    #AdminFacilitesListView
    path('hotel-admin/facilites-list/', views.AdminFacilitesListView.as_view(), name='facilites-list'),
    #AdminRoomFacilitesView
    path('hotel-admin/add-room-facilites/', views.AdminRoomFacilitesView.as_view(), name='add-room-facilites'),
    #AdminRoomFacilitesListView
    path('hotel-admin/room-facilites_list/', views.AdminRoomFacilitesListView.as_view(), name='room-facilites_list'),
    #TwentyFourHoursDealsHotelAdminView
    path('hotel-admin/add-hotel-room-deals/', views.TwentyFourHoursDealsHotelAdminView.as_view(), name='add-hotel-room-deals'),
    #AdminHotelDiscountView
    path('hotel-admin/add-hotel-discount/', views.AdminHotelDiscountView.as_view(), name='add-hotel-discount'),
    #AdminHotelDiscountListView
    path('hotel-admin/discount-list/', views.AdminHotelDiscountListView.as_view(), name='discount-list'),
    # get state by country
    path('admin-api/state_by_country/<int:c_id>', views.GetStateByAdminHotelCountry.as_view(), name="state_by_country"),
    # get city by state
    path('admin-api/city_by_state/<int:s_id>', views.GetCityByAdminHotelState.as_view(), name="city_by_state"),
    #ImagesUploadView
    path('hotel-admin/logo/', views.HotelAdminLogoView.as_view(), name='logo'),
    #ImagesUploadListView
    path('hotel-admin/banner/', views.HotelAdminBannerView.as_view(), name='banner'),
    #Book List View
    path('hotel-admin/book-list/', views.BookingsListView.as_view(), name='book-list'),
    #RoomsBookingsListView
    path('hotel-admin/rooms-book-list/', views.RoomsBookingsListView.as_view(), name='rooms-book-list'),
    #HotelUserProfileView
    path('hotel-admin/user-profile/', views.HotelUserProfileView.as_view(), name='user_profile'),

    ########## Start Sorting and pagination API for all LIST ##########
    # Logo
    path('admin-api/logo-image-list/', views.HotelUserLogoListAdminAPIView.as_view(), name='logo_image_list'),
    # Banner
    path('admin-api/banner-image-list/', views.HotelUserBannerListAdminAPIView.as_view(), name='banner_image_list'),
    # Room
    path('admin-api/room-list/', views.RoomListHotelAdminAPIView.as_view(), name='room_list'),
    # Hotel Facilities
    path('admin-api/hotels-facilites-list/', views.FacilitesListHotelAdminAPIView.as_view(), name='hotels_facilites_list'),
    # Hotel Room Facilities
    path('admin-api/list_room-facilites/', views.HotelRoomAdminFacilitesListAPIView.as_view(), name='list_room_facilites'),
    # hotel 24 hour deals room
    path('admin-api/room-deals-list/', views.TwentyFourHoursDealsListRoomAPIView.as_view(), name='room_deals_list'),
    # Hotel Discount List
    path('admin-api/discount-list/', views.HotelDiscountListAdminAPIView.as_view(), name='discount_list'),
    # Single Room Booking Admin
    path('admin-api/single-booking/', views.SingleRoomBookingAdminAPIView.as_view(), name='single_booking'),
    # Room Book List Admin
    path('admin-api/room-booking/', views.RoomBookListAdminAPIView.as_view(), name='room_booking'),
    ########## End Sorting and pagination API for all list ##########
]
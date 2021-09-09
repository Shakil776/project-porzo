from django.urls import path, include
from webapp import views
app_name = 'webapp'
urlpatterns = [
    # frontend views urls start
    # home view urls
    path('', views.HomeView.as_view(), name='home'),
    # single hotel view urls
    path('hotel/<str:hotel_slug>/', views.SingleHotelView.as_view(), name='single-hotel'),
    # Checkout urls
    path('checkout/', views.CheckOutView.as_view(), name='checkout'),
    path('city-info/<str:city_slug>/', views.SingleCityView.as_view(), name='city_info'),
    path('spot-info/<str:spots_slug>/', views.SpotSingleView.as_view(), name='spot-info'),
    # Search URL
    path('search/', views.SearchView.as_view(), name='search'),
    # show cart details
    path('show-cart/', views.CartSView.as_view(), name='show_cart'),
    # front end customer/user registration 
    path('user-register/', views.UserRegistrationView.as_view(), name='user_register'),
    # front end customer/user login 
    path('user-login/', views.UserLoginView.as_view(), name='user_login'),
    # front end customer/user logoutt 
    path('user-logout/', views.UserLogOutView.as_view(), name='user_logout'),
    # front end customer confirm booking page 
    path('confirm-booking/', views.ConfirmBookingView.as_view(), name='confirm_booking'),
    #TwentyFourHoursDealsView
    path('twenty-four-deals/', views.TwentyFourHoursDealsView.as_view(), name='twenty-four-deals'),
    # under construction page 
    # about us
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),
    # contact us
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),
    # faq
    path('faq/', views.FaqView.as_view(), name='faq'),
    # blog
    path('blog/', views.BlogView.as_view(), name='blog'),
    # press
    path('press/', views.PressView.as_view(), name='press'),
    # terms of use
    path('terms-of-use/', views.TermsOfUseView.as_view(), name='terms_of_use'),
    # give us feedbacks
    path('give-feedback/', views.GiveFeedbackView.as_view(), name='give_us_feedback'),
    # help center
    path('help-center/', views.HelpCenterView.as_view(), name='help_center'),
    # privacy policy
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    # events
    path('event/', views.EventFrontEndView.as_view(), name='event'),
    # services
    path('services/', views.ServicesFrontEndView.as_view(), name='services'),
    # hotels
    path('hotel/', views.HotelsFrontEndView.as_view(), name='hotel'),
    # login from mobile device
    path('login/', views.UserLoginFromMobileDeviceView.as_view(), name='mobile_login'),
    # signup from mobile device
    path('register/', views.UserRegistrationFromMobileDeviceView.as_view(), name='mobile_signup'),
    # user profile view
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    # frontend views urls end

    # admin panel view urls start
    path('admin-login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('user-types/', views.UserTypeView.as_view(), name='user_type'),
    path('hotels/', views.HotelView.as_view(), name='hotels'),
    path('rooms/', views.RoomView.as_view(), name='rooms'),
    path('offer-types/', views.OfferTypeView.as_view(), name='offer-types'),
    path('offer-max-amounts/', views.OfferMaxAmountView.as_view(), name='offer-max-amounts'),
    path('offers/', views.OfferView.as_view(), name='offers'),
    path('coupon/', views.CuponView.as_view(), name='coupon'),
    path('giftcard/', views.GiftCardView.as_view(), name='giftcard'),
    path('events/', views.EventView.as_view(), name='events'),
    path('foodmenu/', views.FoodMenuView.as_view(), name='foodmenu'),
    path('touristspot/', views.TouristSpotView.as_view(), name='touristspot'),
    path('hotel-gallery/', views.HotelGallery.as_view(), name='hotel_gallery'),
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('packages/', views.PackageView.as_view(), name='packages'),
    path('carts/', views.CartView.as_view(), name='carts'),
    path('facilites/', views.FacilitesView.as_view(), name='facilites'),
    path('facilites-room/', views.FacilitesGroupView.as_view(), name='facilites-room'),
    path('hotel-facilites/', views.HotelFacilitesView.as_view(), name='hotel-facilites'),
    #TwentyFourHoursDealsPorzotokAppView
    path('porzotok-deals/', views.TwentyFourHoursDealsPorzotokAppView.as_view(), name='porzotok-deals'),
    #TwentyFourHoursDealsHotelView
    path('hotel-deals/', views.TwentyFourHoursDealsHotelView.as_view(), name='hotel-deals'),
    # admin panel view urls end
]
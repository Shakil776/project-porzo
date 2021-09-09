from django.shortcuts import render
from porzotokApp import models
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from porzotokApp.password import PassWord
from porzotokApp import serializers
from HotelAdmin import serializers as HotelSerializers
from .custom import custom
from datetime import datetime
from rest_framework import viewsets, generics, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from HotelAdmin.pagination import PaginationHandlerMixin
from rest_framework.views import APIView
from django.db.models import Q

# Basic Pagination size for all  
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'size'

class HotelLoginView(View):

    def get(self, request):
        context = {}
        if 'uid' not in request.session and 'uphone' not in request.session\
            and 'utype' not in request.session and 'time' not in request.session:
            return render(request, 'backEnd/hoteladmin/admin_login.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin")

    def post(self, request): 
        context = {}
        if 'uid' not in request.session and 'uphone' not in request.session\
            and 'utype' not in request.session and 'time' not in request.session:
            if 'phone' in request.POST and 'password' in request.POST:
                phone = request.POST['phone']
                password = PassWord(request.POST['password'])
                logged = models.HotelUserOwner.objects.filter(hotel_user_phone = phone, hotel_user_password = password)
                if len(logged) != 0:
                    request.session.create()
                    request.session['uid'] = logged[0].hotel_user_owner_id
                    request.session['uphone'] = logged[0].hotel_user_phone
                    request.session['utype'] = logged[0].hotel_user_type_id.hotel_user_type_name
                    request.session['time'] = str(datetime.now())
                    custom(request.session.session_key, request.session['uphone'])
                    return HttpResponseRedirect("/hotel-admin")

                else:
                    context['error'] = True
                    context['msg'] = "Username and password does not match"
            else:
                context['error'] = True
                context['msg'] = "Data Field missing"
            return render(request, 'backEnd/hoteladmin/admin_login.html', context)
        else:
            print("LS")
            return HttpResponseRedirect("/hotel-admin/login/")


class HotelDashboard(View):
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/dashboard.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

class Logout(View):
    def get(self, request):
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            del request.session['uid']
            del request.session['uphone']
            del request.session['utype']
            del request.session['time']
            return HttpResponseRedirect("/hotel-admin/login/")
        else:
            return HttpResponseRedirect("/hotel-admin")




# Hotel Admin Add Room
class AdminRoomView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/admin_room.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")
    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/admin_room.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")


# Hotel Admin Add Room
class AdminRoomListView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")
    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")







# Hotel Admin Add Hotel Facilites
class AdminFacilitesView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_facilites.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_facilites.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")


# Hotel Admin Add Hotel Facilites
class AdminFacilitesListView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_facilites_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_facilites_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")




# Hotel Admin Add Hotel Facilites
class AdminRoomFacilitesView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_facilites.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_facilites.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")


# Hotel Admin Add Hotel Facilites
class AdminRoomFacilitesListView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_facilites_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_facilites_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")





# Hotel Admin Add Hotel Facilites
class AdminHotelDiscountView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_discount.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_discount.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")


# Hotel Admin Add Hotel Facilites
class AdminHotelDiscountListView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_discount_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_discount_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")





# Hotel Admin Add Hotel Facilites
class TwentyFourHoursDealsHotelAdminView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_room_24_hours_deals.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/hotel_room_24_hours_deals.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")



# Hotel Admin Add Hotel Facilites
# class TwentyFourHoursDealsListView(View):
    
#     def get(self, request):
#         context = {}
#         if 'uid' in request.session and 'uphone' in request.session\
#          and 'utype' in request.session and 'time' in request.session:
#             context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
#             user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
#             try:
#                 context['user_image'] = user_image[len(user_image) - 1]
#             except:
#                 context['user_image'] = 0
#             return render(request, 'backEnd/hoteladmin/24_hours_deals_list.html', context)
#         else:
#             return HttpResponseRedirect("/hotel-admin/login/")

#     def post(self, request):
#         context = {}
#         if 'uid' in request.session and 'uphone' in request.session\
#          and 'utype' in request.session and 'time' in request.session:
#             context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
#             user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
#             try:
#                 context['user_image'] = user_image[len(user_image) - 1]
#             except:
#                 context['user_image'] = 0
#             return render(request, 'backEnd/hoteladmin/24_hours_deals_list.html', context)
#         else:
#             return HttpResponseRedirect("/hotel-admin/login/")


# Hotel Admin LOGO
class HotelAdminLogoView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/logo.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/logo.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")



class HotelAdminBannerView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/banner.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/banner.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")



#Start Hotel User Profile
class HotelUserProfileView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/user_profile.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/user_profile.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

#End Hotel User Profile 

##Start Book List
class BookingsListView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_booking_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_booking_list.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

#End Book List 



#Start Book List
class RoomsBookingsListView(View):
    
    def get(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_booking.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

    def post(self, request):
        context = {}
        if 'uid' in request.session and 'uphone' in request.session\
         and 'utype' in request.session and 'time' in request.session:
            context['user_details'] = models.HotelUserOwner.objects.get(hotel_user_owner_id=request.session['uid'])
            user_image = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=request.session['uid'])
            try:
                context['user_image'] = user_image[len(user_image) - 1]
            except:
                context['user_image'] = 0
            return render(request, 'backEnd/hoteladmin/room_booking.html', context)
        else:
            return HttpResponseRedirect("/hotel-admin/login/")

#End Book List 




#Hotel Admin Serializer View

# Country View 
class CountryAdminAPIView(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = HotelSerializers.CountryAdminSerializer

# State View
class StateAdminAPIView(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = HotelSerializers.StateAdminSerializer

# City  View
class CityAdminAPIView(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = HotelSerializers.CityAdminSerializer


#ImageGalaryDetailsAdmin
class ImageGalaryDetailsAdminAPIView(viewsets.ModelViewSet):
    queryset = models.ImageGalaryDetails.objects.all()
    serializer_class = HotelSerializers.ImageGalaryDetailsAdminSerializer 



#Image
class ImageAdminAPIView(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    def get_serializer_class(self):
        return HotelSerializers.ImageAdminSerializer 

    def get (self,request):
        return self.list(request)
    #serializer_class = serializers.ImageSerializer 
    def list(self, request):
        if request.GET.get('galley_id'):
            galley_id = request.GET.get('galley_id')
            
            imagelist = models.Image.objects.filter(image_galary_details_id__image_galary_details_id = int(galley_id))
        else:
            imagelist = models.Image.objects.all()
        serializer = HotelSerializers.ImageAdminSerializer(imagelist, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Image List", "data": serializer.data}
        return Response(response_dict)

    # def retrieve(self, request, pk=None):
    #     image = models.Image.objects.all()
    #     imagelist = get_object_or_404(image, pk=pk)
    #     serializer = serializers.ImageSerializer(imagelist, context={"request": request})
    #     serializer_data = serializer.data
    #     return Response({"error": False, "message": "Single Data Fetch", "Data": serializer_data})
    
    def create(self, request):
        print(request.data)
        try:
            images = request.FILES.getlist('Image')
            for image in list(images):
                image_list = []
                image_detail = {}
                image_detail["Image"] = image
                image_detail["image_galary_details_id"] = request.data["image_galary_details_id"]
                image_list.append(image_detail)
                serializer = HotelSerializers.ImageAdminSerializer(data=image_list, many=True, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
            response_dict = {"error": False, "message": f"Image Uploaded in Gallary and The ID {request.data['image_galary_details_id']}"}
        except Exception as e:
            print(str(e))
            response_dict = {"error": False, "message": f"Image Not Uploaded ",}

        return Response(response_dict)




class HotelDetailAdminViewSet(viewsets.ViewSet):
    queryset = models.HotelDetails.objects.all()
    def get_serializer_class(self):
        return HotelSerializers.HotelDetailsAdminSerializer 

    def get (self,request):
        return self.list(request)

    def list(self, request):
        if request.GET.get('user_id'):
            param  = request.GET.get('user_id')
            hotel_details = models.HotelDetails.objects.filter(hotel_user_id__hotel_user_owner_id=int(param)) 

            serializer = HotelSerializers.HotelDetailsAdminSerializer(hotel_details, many=True, context={"request": request})
            response_dict = {"error": False, "message": "User Hotel Details List", "data": serializer.data}
            return Response(response_dict)
        else:
            return Response({"error": False, "message": "User Id Not Found"})

    def create(self, request):

        try:
            # save into image gallery details serializer
            image_gallery_details_serializer = HotelSerializers.ImageGalaryDetailsAdminSerializer(data=request.data, context={"request":request})
            image_gallery_details_serializer.is_valid(raise_exception=True)
            image_gallery_details_serializer.save()

            image_galary_details_id = image_gallery_details_serializer.data['image_galary_details_id']

            # save hotel details info with image gallery details id into hotel details table
            hotel_details_list = []
            hotel_detail = {}
            hotel_detail["hotel_name"] = request.data["hotel_name"]
            hotel_detail["slug_name"] = request.data["slug_name"]
            hotel_detail["hotel_reg_no"] = request.data["hotel_reg_no"]
            hotel_detail["hotel_email"] = request.data["hotel_email"]
            hotel_detail["hotel_phone"] = request.data["hotel_phone"]
            hotel_detail["Map"] = request.data["Map"]
            hotel_detail["short_address"] = request.data["short_address"]
            hotel_detail["city_id"] = request.data["city_id"]
            hotel_detail["hotel_info"] = request.data["hotel_info"]
            hotel_detail["image_galary_details_id"] = image_galary_details_id
            hotel_detail["hotel_type"] = request.data["hotel_type"]
            hotel_detail["hotel_discount_id"] = request.data["hotel_discount_id"]
            hotel_detail["is_active"] = request.data["is_active"]
            hotel_details_list.append(hotel_detail)

            serializer = HotelSerializers.HotelDetailsAdminSerializer(data=hotel_details_list, many=True, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            try:
                images = request.FILES.getlist('image')

                for image in list(images):
                    image_list = []
                    image_detail = {}
                    image_detail["Image"] = image
                    image_detail["image_galary_details_id"] = image_galary_details_id
                    image_list.append(image_detail)
                    serializer = HotelSerializers.ImageAdminSerializer(data=image_list, many=True, context={"request": request})
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            except Exception as e:
                print(str(e))
  
            dict_response = {"error": False, "message": "Hotel Information Save Successfully!"}
        except Exception as e:
            print(str(e))
            dict_response = {"error": True, "message": "Hotel Information Not Save."}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = models.HotelDetails.objects.all()
        single_hotel_data = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelDetailsAdminSerializer(single_hotel_data, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})



    def update(self, request, pk=None):
        queryset = models.HotelDetails.objects.all()
        single_hotel_data_update = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelDetailsAdminSerializer(single_hotel_data_update, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has been Updated"})



    def destroy(self, request, pk=None):
        try:
            queryset = models.HotelDetails.objects.all()
            hotel_details = get_object_or_404(queryset, pk=pk)
            hotel_details.delete()
            return Response({"error": False, "message": "Hotel Details deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel Details Data Dosen't Deleted!"})


class RoomListHotelAdminAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.RoomHotelAdminListSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        instance = models.Room.objects.filter(is_active=True, hotel_id__hotel_user_id=int(user_id)).order_by('-room_id')
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HotelAdminSearchViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET and 'key' in request.GET:
            user_id = request.GET.get('user_id')
            key = request.GET.get('key')
            room = models.Room.objects.filter(is_active=True, hotel_id__hotel_user_id=int(user_id))
            queryset = room.filter(Q(hotel_id__hotel_name__contains=str(key)) | Q(price_id__price__contains=str(key)) | Q(room_name__contains=str(key)) | Q(room_no__contains=str(key))| Q(floor_id__floor_no__contains=str(key))).order_by('-room_id')
            total_count = len(queryset)
            results = queryset[:10]
            serializer = HotelSerializers.RoomHotelAdminListSerializer(results, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data, "count": total_count})


class RoomHotelAdminViewSet(viewsets.ViewSet):

    def list(self, request):

        if request.GET.get('hotel_id'):
            hotel_id = request.GET.get('hotel_id')
            rooms = models.Room.objects.filter(hotel_id__hotel_id=int(hotel_id)) 
            serializer = HotelSerializers.RoomHotelAdminSerializer(rooms, many=True, context={"request": request})
            return Response({"error": False, "message": "Room Data List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "Room Not found"})

        if request.GET.get('user_id'):
            user_id = request.GET.get('user_id')
            rooms = models.Room.objects.filter(hotel_id__hotel_user_id=int(user_id)) 

            serializer = HotelSerializers.RoomHotelAdminSerializer(rooms, many=True, context={"request": request})
            return Response({"error": False, "message": "Room Data List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "Room Not found"})



    def create(self, request):
        try:
            # save into image gallery details serializer
            image_gallery_details_serializer = HotelSerializers.ImageGalaryDetailsAdminSerializer(data=request.data, context={"request":request})
            image_gallery_details_serializer.is_valid(raise_exception=True)
            image_gallery_details_serializer.save()

            image_galary_details_id = image_gallery_details_serializer.data['image_galary_details_id']

            # save price details into price table
            price_detail = {}
            price_detail["price"] = request.data['price']
            try:
                price_detail["offer_price"] = request.data['offer_price']
            except:
                price_detail["offer_price"] = request.data['price']

            price_detail["price_entry_date"] = datetime.now().date()
            price_detail["price_type"] = request.data['price_type']
            price_serializer = HotelSerializers.PriceAdminSerializer(data=price_detail, context={"request": request})
            price_serializer.is_valid(raise_exception=True)
            price_serializer.save()
            price_details_id = price_serializer.data['price_id'] 

            # save room info with image gallery details id into room info table

            room_detail = {}
            room_detail["room_name"] = request.data["room_name"]
            room_detail["room_no"] = request.data["room_no"]
            room_detail["floor_id"] = request.data["floor_id"]
            room_detail["hotel_id"] = models.HotelDetails.objects.get(hotel_user_id__hotel_user_owner_id=int(request.data["hotel_owner_id"])).hotel_id
            room_detail["room_status"] = request.data["room_status"]
            room_detail["price_id"] = price_details_id
            room_detail["room_description"] = request.data["room_description"]
            room_detail["image_galary_details_id"] = image_galary_details_id
            room_detail["is_active"] = True
            room_detail["is_deals"] = False
            # try:
            #     room_detail["hotel_discount_id"] = request.data["hotel_discount_id"]
            # except:
            #     room_detail["hotel_discount_id"] = None

            room_serializer = HotelSerializers.RoomHotelAdminSerializer(data=room_detail, context={"request": request})
            room_serializer.is_valid(raise_exception=True)
            room_serializer.save()

            # save image into image table
            try:
                images = request.FILES.getlist('image')

                for image in list(images):
                    image_list = []
                    image_detail = {}
                    image_detail["Image"] = image
                    image_detail["image_galary_details_id"] = image_galary_details_id
                    image_list.append(image_detail)
                    serializer = HotelSerializers.ImageAdminSerializer(data=image_list, many=True, context={"request": request})
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            except Exception as e:
                print(str(e))
            
            dict_response = {"error": False, "message": "Room Information Save Successfully"}
        except Exception as e:
            print(str(e))
            dict_response = {"error": True, "message": f"{str(e)} Room Information Not Save."}
        return Response(dict_response)



    def retrieve(self, request, pk=None):
        queryset = models.Room.objects.all()
        room = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.RoomHotelAdminSerializer(room, context={"request": request})
        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})



    def update(self, request, pk=None):
        queryset = models.Room.objects.all()
        room = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.RoomHotelAdminSerializerUpdate(room, data=request.data, context={"request": request}, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has been Updated"})




    def destroy(self, request, pk=None):
        try:
            queryset = models.Room.objects.all()
            room = get_object_or_404(queryset, pk=pk)
            room.delete()
            return Response({"error": False, "message": "Room deleted successfully!"})
        except:
            return Response({"error": True, "message": "Room Not Deleted!"})

#Create Price ViewSet
class CreatePriceViewSet(viewsets.ViewSet):
    def update(self, request, pk=None):
        queryset = models.Price.objects.all()
        price = get_object_or_404(queryset, pk=pk)
        price_serializer = HotelSerializers.PriceAdminSerializer(price, data=request.data, context={"request": request})
        price_serializer.is_valid(raise_exception=True)
        price_serializer.save()
        return Response({"error": False, "message": "Price Updated"})

    # def create(self, request):
    #     price_list = []
    #     price_detail = {}
    #     price_detail["price"] = request.data['price']
    #     price_detail["offer_price"] = request.data['offer_price']
    #     price_detail["price_entry_date"] = request.data['price_entry_date']
    #     price_detail["price_type"] = 1
    #     price_list.append(price_detail)
    #     price_serializer = HotelSerializers.PriceAdminSerializer(data=price_list, many=True, context={"request": request})
    #     price_serializer.is_valid(raise_exception=True)
    #     price_serializer.save()
    #     price_details_id = price_serializer.data[0]['price_id']
    #     return Response({"error": False, "message": "Price Created", "price_id": price_details_id})
    



#Hotel Room Admin Facilites
class HotelRoomAdminFacilitesViewSet(viewsets.ViewSet):

    def list(self, request):
        facilities = models.Facilites.objects.all()
        serializer = HotelSerializers.FacilitesAdminSerializer(facilities, many=True, context={"request": request})
        return Response({"error": False, "data": serializer.data})


    def create(self, request):
        try:
            if 'room_id' in request.data and 'facilites_id' in request.data:

                # myList = zip(request.data['room_id'].split(','), request.data['facilites_id'].split(','))

                # for room in request.data['room_id'].split(','):
                #     roomList = []
                #     roomDetail["room"] = room
                #     # print(room)
                #     roomList.append(room_detail)
                

                for facility in request.data['facilites_id'].split(','):
                    for room in request.data['room_id'].split(','):
                        facilityGroup = models.FacilitesGroup.objects.create(
                            facilites_id = models.Facilites.objects.get(facilites_id=facility),
                            room_id = models.Room.objects.get(room_id=room)
                        )
                        facilityGroup.save()
                    # facilityList = []
                    # facilityDetail["facility"] = facility
                    # # print(facilityList)
                    # facilityList.append(facilityDetail)

                # finalList = zip(roomList, facilityList)

                # for room, facility in myList:
                #     # facilites_room_details_list = []
                #     facilites_room_detail = {}
                #     facilites_room_detail["facilites_id"] = facility
                #     facilites_room_detail["room_id"] = room
                #     # facilites_room_details_list.append(facilites_room_detail)
                #     facilites_room_serializer = HotelSerializers.HotelRoomAdminFacilitesSerializer(data=finalList, context={"request": request})
                #     facilites_room_serializer.is_valid(raise_exception=True)
                #     facilites_room_serializer.save()

            dict_response = {"error": False, "message": "Room Facilites Information Save Successfully!"}
        except Exception as e:
            dict_response = {"error": True, "message": "Room Facilites Information Not Save."}
        return Response(dict_response)


    
    def retrieve(self, request, pk=None):
        queryset = models.FacilitesGroup.objects.all()
        facilites_room = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelRoomAdminFacilitesSerializer(facilites_room, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "Data": serializer.data})


    def update(self, request, pk=None):
        queryset = models.FacilitesGroup.objects.all()
        facilites_room = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelRoomAdminFacilitesSerializer(facilites_room, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Hasbeen Updated"})


    def destroy(self, request, pk=None):
        try:
            queryset = models.FacilitesGroup.objects.all()
            facilites_room = get_object_or_404(queryset, pk=pk)
            facilites_room.delete()
            return Response({"error": False, "message": "Room Facilites deleted successfully!"})
        except:
            return Response({"error": True, "message": "Room Facilites Not Deleted!"})


class HotelRoomAdminFacilitesListAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.HotelRoomAdminFacilitesSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        instance = models.FacilitesGroup.objects.filter(room_id__hotel_id__hotel_user_id=int(user_id))
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class HotelRoomFacilitiesSearchViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET and 'key' in request.GET:
            user_id = request.GET.get('user_id')
            key = request.GET.get('key')
            facilities = models.FacilitesGroup.objects.filter(room_id__hotel_id__hotel_user_id=int(user_id))
            queryset = facilities.filter(Q(room_id__hotel_id__hotel_name__contains=str(key)) | Q(room_id__room_name__contains=str(key)) | Q(room_id__room_no__contains=str(key))| Q(facilites_id__facilites_name__contains=str(key)))
            total_count = len(queryset)
            results = queryset[:10]
            serializer = HotelSerializers.HotelRoomAdminFacilitesSerializer(results, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data, "count": total_count})



class FacilitesListHotelAdminAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.HotelAdminFacilitesSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        instance = models.HotelFacilites.objects.filter(hotel_id__hotel_user_id=int(user_id)).order_by('-hotel_facilites_id')
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class HotelFacilitiesSearchViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET and 'key' in request.GET:
            user_id = request.GET.get('user_id')
            key = request.GET.get('key')
            hotel_facilities = models.HotelFacilites.objects.filter(hotel_id__hotel_user_id=int(user_id))
            queryset = hotel_facilities.filter(Q(hotel_id__hotel_name__contains=str(key)) | Q(facilites_id__facilites_name__contains=str(key)) | Q(price_id__price__contains=str(key))).order_by('-hotel_facilites_id')
            total_count = len(queryset)
            results = queryset[:10]
            serializer = HotelSerializers.HotelAdminFacilitesSerializer(results, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data, "count": total_count})


#Hotel Admin Facilites 
class HotelAdminFacilitesViewSet(viewsets.ViewSet):

    def list(self, request):

        if request.GET.get('user_id'):
            user_id = request.GET.get('user_id')
            hotel_facilites = models.HotelFacilites.objects.filter(hotel_id__hotel_user_id=int(user_id)) 

            serializer = HotelSerializers.HotelAdminFacilitesSerializer(hotel_facilites, many=True, context={"request": request})
            return Response({"error": False, "message": "All Hotel Facilites Data List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "Hotel Facilites Not found"})


    def create(self, request):
        # hotel = models.HotelDetails.objects.get(hotel_user_id__hotel_user_owner_id=int(request.data["hotel_owner_id"]))
        # print(hotel.hotel_id)
        try:
            # save price details into price table
            price_detail = {}
            price_detail["price"] = request.data['price']
            try:
                price_detail["offer_price"] = request.data['offer_price']
            except:
                price_detail["offer_price"] = request.data['price']
            price_detail["price_entry_date"] = datetime.now().date()
            price_detail["price_type"] = request.data['price_type']
            price_serializer = HotelSerializers.PriceAdminSerializer(data=price_detail, context={"request": request})
            price_serializer.is_valid(raise_exception=True)
            price_serializer.save()
            price_details_id = price_serializer.data['price_id'] 

            # save
            hotel_facilites_details = {}
            hotel_facilites_details["facilites_id"] = request.data["facilites_id"]
            hotel_facilites_details["hotel_id"] = models.HotelDetails.objects.get(hotel_user_id__hotel_user_owner_id=int(request.data["hotel_owner_id"])).hotel_id
            hotel_facilites_details["price_id"] = price_details_id

            hotel_facilites_serializer = HotelSerializers.HotelAdminFacilitesSerializer(data=hotel_facilites_details, context={"request": request})
            hotel_facilites_serializer.is_valid(raise_exception=True)
            hotel_facilites_serializer.save()
            
            dict_response = {"error": False, "message": "Hotel Facilites Information Save Successfully!"}
        except Exception as e:
            dict_response = {"error": True, "message": "Hotel Facilites Information Not Save."}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = models.HotelFacilites.objects.all()
        hotel_facilites = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelAdminFacilitesSerializer(hotel_facilites, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch","data":serializer.data})


    def update(self, request, pk=None):
        queryset = models.HotelFacilites.objects.all()
        hotel_facilites = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelAdminFacilitesSerializer(hotel_facilites, data=request.data, context={"request": request}, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Hasbeen Updated"})


    def destroy(self, request, pk=None):
        try:
            queryset = models.HotelFacilites.objects.all()
            hotel_facilites = get_object_or_404(queryset, pk=pk)
            hotel_facilites.delete()
            return Response({"error": False, "message": "Hotel Facilites deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel Facilites Not Deleted!"})



# Get State By Country
class GetStateByAdminHotelCountry(generics.ListAPIView):
    serializer_class = HotelSerializers.StateAdminSerializer
    def get_queryset(self):
        c_id = self.kwargs["c_id"]
        return models.State.objects.filter(country_id__country_id=c_id)

# Get city By State
class GetCityByAdminHotelState(generics.ListAPIView):
    serializer_class = HotelSerializers.CityAdminSerializer
    def get_queryset(self):
        s_id = self.kwargs["s_id"]
        return models.City.objects.filter(state_id__state_id=s_id)



#TwentyFourHoursDealsListHotelAdmin
class TwentyFourHoursDealsListHotelAdminViewSet(viewsets.ViewSet):

    def list(self, request):
        if request.GET.get('user_id'):
            user_id = request.GET.get('user_id')
            deals_list = models.TwentyFourHoursDeals.objects.filter(room_id__hotel_id__hotel_user_id=int(user_id)) 

            serializer = HotelSerializers.TwentyFourHoursDealsListHotelAdminSerializer(deals_list, many=True, context={"request": request})
            return Response({"error": False, "message": "Twenty Four Hours Deals Data List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "Twenty Four Hours Deals Data List Not found"})



#Twenty Four Hours Deals Hotel Admin View
class TwentyFourHoursDealsHotelAdminSerializerViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            if 'room_id' in request.data:
                for room in request.data['room_id'].split(','):
                    ## Room Update for Deals
                    get_price = models.Room.objects.get(room_id=int(room))
                    get_price.is_deals = True
                    get_price.deal_start_date = datetime.now()
                    get_price.allow_offer_percent = int(request.data['allow_offer'])

                    ## Price Update for Deals
                    get_price.offer_discount_price = float(get_price.price_id.price) - float(get_price.price_id.price * int(request.data['allow_offer'])/100)
                    get_price.save()
            dict_response = {"error": False, "message": "Hotel Twenty Four Hours Deals Information Save Successfully!"}
        except Exception as e:
            dict_response = {"error": True, "message": "Hotel Twenty Four Hours Deals Information Not Save."}
        return Response(dict_response)

    def update(self, request, pk=None):

        if 'status' in request.data:
            # Room Update for Deals
            if request.data['status'] == 1:
                get_price = models.Room.objects.get(room_id=pk)
                get_price.is_deals = False
                get_price.deal_start_date = None
                get_price.allow_offer_percent = ''
                get_price.offer_discount_price = 0.00
                get_price.save()
            dict_response = {"error": False, "message": "Deactivated"}
        return Response(dict_response)




# TwentyFourHoursDealsListRoomAPIView
class TwentyFourHoursDealsListRoomAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.TwentyFourHoursDealsListRoomSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        instance = models.Room.objects.filter(is_deals=True, is_active=True, hotel_id__hotel_user_id=int(user_id)).order_by('-room_id')
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Hotel24HourDealsSearchViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET and 'key' in request.GET:
            user_id = request.GET.get('user_id')
            key = request.GET.get('key')
            room = models.Room.objects.filter(is_deals=True, is_active=True, hotel_id__hotel_user_id=int(user_id))
            queryset = room.filter(Q(hotel_id__hotel_name__contains=str(key)) | Q(price_id__price__contains=str(key)) | Q(room_name__contains=str(key)) | Q(room_no__contains=str(key)) | Q(offer_discount_price__contains=str(key))).order_by('-room_id')
            total_count = len(queryset)
            results = queryset[:10]
            serializer = HotelSerializers.TwentyFourHoursDealsListRoomSerializer(results, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data, "count": total_count})



class HotelDiscountAdminViewSet(viewsets.ViewSet):

    def list(self, request):
        if request.GET.get('user_id'):
            user_id = request.GET.get('user_id')
            hotel_discount = models.HotelDiscount.objects.filter(hotel_user_owner_id__hotel_user_owner_id=int(user_id)) 

            serializer = HotelSerializers.HotelDiscountAdminSerializer(hotel_discount, many=True, context={"request": request})
            return Response({"error": False, "message": "Hotel Discount List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "Hotel Discount Not found"})



    def create(self, request):
        try:
            # save Offer Max Amount details into Hotel Discount table
            # offer_max_amount_detail = {}
            # offer_max_amount_detail["max_amount"] = request.data['max_amount']
            # offer_max_amount_detail["min_amount"] = request.data['min_amount']
            # offer_max_amount_serializer = HotelSerializers.OfferMaxAmountAdminSerializer(data=offer_max_amount_detail, context={"request": request})
            # offer_max_amount_serializer.is_valid(raise_exception=True)
            # offer_max_amount_serializer.save()
            # offer_max_amount_details_id = offer_max_amount_serializer.data['offer_max_amount_id'] 

            # save hotel Discount info.
            hotel_discount_detail = {}
            hotel_discount_detail["hotel_discount_name"] = request.data["hotel_discount_name"]
            hotel_discount_detail["start_time_date"] = request.data["start_time_date"]
            hotel_discount_detail["end_time_date"] = request.data["end_time_date"]
            # hotel_discount_detail["offer_max_amount_id"] = int(offer_max_amount_details_id)
            hotel_discount_detail["hotel_user_owner_id"] = int(request.data["hotel_user_owner_id"])
            hotel_discount_serializer = HotelSerializers.HotelDiscountAdminSerializer(data=hotel_discount_detail, context={"request": request})
            hotel_discount_serializer.is_valid(raise_exception=True)
            hotel_discount_serializer.save()
            hotel_discount_id = hotel_discount_serializer.data['hotel_discount_id']

            # save discount in the hotel rooms
            if 'room_id' in request.data:
                for room in request.data['room_id'].split(','):
                    # Update room discount field
                    _room = models.Room.objects.get(room_id=int(room))
                    _room.allow_offer_percent = int(request.data['allow_offer'])
                    _room.offer_discount_price = float(_room.price_id.price) - float(_room.price_id.price * int(request.data['allow_offer'])/100)
                    _room.hotel_discount_id = models.HotelDiscount.objects.get(hotel_discount_id=int(hotel_discount_id))
                    _room.save()

            dict_response = {"error": False, "message": "Discount Information Added Successfully"}
        except Exception as e:
            dict_response = {"error": True, "message": "Discount Information Not Added."}
        return Response(dict_response)



    def retrieve(self, request, pk=None):
        queryset = models.HotelDiscount.objects.all()
        hotel_discount = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelDiscountAdminSerializer(hotel_discount, context={"request": request})
        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})



    def update(self, request, pk=None):
        queryset = models.HotelDiscount.objects.all()
        hotel_discount = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelDiscountAdminSerializer(hotel_discount, data=request.data, context={"request": request}, partial=True)
        print(serializer)
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has been Updated"})



    def destroy(self, request, pk=None):
        try:
            queryset = models.HotelDiscount.objects.all()
            hotel_discount = get_object_or_404(queryset, pk=pk)
            hotel_discount.delete()
            return Response({"error": False, "message": "Hotel Discount deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel Discount Not Deleted!"})


class GetHotelRoomsViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            rooms = models.Room.objects.filter(hotel_id__hotel_user_id__hotel_user_owner_id=int(user_id), is_active=True, is_deals=False) 
    
            serializer = HotelSerializers.HotelRoomsGetSerializer(rooms, many=True)
            return Response({"error": False, "data": serializer.data})
        else:
            return Response({"error": False, "data": []})

class GetFacilitiesRoomsViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            rooms = models.Room.objects.filter(hotel_id__hotel_user_id__hotel_user_owner_id=int(user_id), is_active=True) 
    
            serializer = HotelSerializers.FacilitiesRoomsSerializer(rooms, many=True)
            return Response({"error": False, "data": serializer.data})
        else:
            return Response({"error": False, "data": []})



class CreateOfferMaxAmountViewSet(viewsets.ViewSet):

    def update(self, request, pk=None):
        queryset = models.OfferMaxAmount.objects.all()
        offer_max = get_object_or_404(queryset, pk=pk)
        offer_max_serializer = HotelSerializers.OfferMaxAmountAdminSerializer(offer_max, data=request.data, context={"request": request}, partial=True)
        offer_max_serializer.is_valid(raise_exception=True)
        offer_max_serializer.save()
        return Response({"error": False, "message": "Offer Max Amount Updated"})


# HotelDiscountListAdminAPIView
class HotelDiscountListAdminAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.HotelDiscountListAdminSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        instance = models.HotelDiscount.objects.filter(hotel_user_owner_id__hotel_user_owner_id=int(user_id)).order_by('-hotel_discount_id')
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HotelDiscountSearchViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET and 'key' in request.GET:
            user_id = request.GET.get('user_id')
            key = request.GET.get('key')
            hotel_discount = models.HotelDiscount.objects.filter(hotel_user_owner_id__hotel_user_owner_id=int(user_id))
            queryset = hotel_discount.filter(Q(hotel_discount_name__contains=str(key)) | Q(start_time_date__contains=str(key)) | Q(end_time_date__contains=str(key)) | Q(offer_max_amount_id__max_amount__contains=str(key)) | Q(offer_max_amount_id__min_amount__contains=str(key))).order_by('-hotel_discount_id')
            total_count = len(queryset)
            results = queryset[:10]
            serializer = HotelSerializers.HotelDiscountListAdminSerializer(results, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data, "count": total_count})




#HotelUserPhotoAdminSerializer
class HotelUserPhotoAdminViewSet(viewsets.ViewSet):

    def list(self, request):
        if request.GET.get('user_id'):
            user_id = request.GET.get('user_id')
            photo = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=int(user_id)) 

            serializer = HotelSerializers.HotelUserPhotoAdminSerializer(photo, many=True, context={"request": request})
            return Response({"error": False, "message": "Images Data List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "Images Not found"})

    def create(self, request):

        try:
            photo_detail = {}
            try:
                photo_detail["logo_photo"] = request.data["logo_photo"]
            except:
                photo_detail["logo_photo"] = None
            try:
                photo_detail["banner_photo"] = request.data["banner_photo"]
            except:
                photo_detail["banner_photo"] = None
            photo_detail["hotel_user_owner_id"] = request.data["hotel_user_owner_id"]
            # photo_details_list.append(photo_detail)
            photo_serializer = HotelSerializers.HotelUserPhotoAdminSerializer(data=photo_detail, context={"request": request}, partial=True)
            photo_serializer.is_valid(raise_exception=True)
            photo_serializer.save()

            dict_response = {"error": False, "message": "Photo Information Save Successfully!"}
        except Exception as e:
            dict_response = {"error": True, "message": "Photo Information Not Save."}
        return Response(dict_response)

    

    def retrieve(self, request, pk=None):
        queryset = models.HotelUserPhoto.objects.all()
        photo = get_object_or_404(queryset, pk=pk)
        serializer = HotelSerializers.HotelUserPhotoAdminSerializer(photo, context={"request": request})
        return Response({"error": False, "message": "Single Food Menu Data", "data": serializer.data})


    def update(self, request, pk=None):
        try:
            queryset = models.HotelUserPhoto.objects.all()
            photo = get_object_or_404(queryset, pk=pk)
            serializer = HotelSerializers.HotelUserPhotoAdminSerializer(photo, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Photo Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Photo Not Updated"}
        return Response(dict_response)


    def destroy(self, request, pk=None):
        try:
            queryset = models.HotelUserPhoto.objects.all()
            photo = get_object_or_404(queryset, pk=pk)
            photo.delete()
            return Response({"error": False, "message": "Photo deleted successfully!"})
        except:
            return Response({"error": True, "message": "Photo Not Deleted!"}) 




class HotelUserOwnarAdminViewSet(viewsets.ViewSet):

    def list(self, request):
        if request.GET.get('user_id'):
            user_id = request.GET.get('user_id')
            hotel_user = models.HotelUserOwner.objects.filter(hotel_user_owner_id=int(user_id)) 

            serializer = HotelSerializers.HotelUserAdminSerializer(hotel_user, many=True, context={"request": request})
            return Response({"error": False, "message": "Hotel User Data List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "Hotel User Not found"})  



#Hotel User LOGO List Admin 
class HotelUserLogoListAdminAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.HotelUserLogoListAdminSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        instance = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=int(user_id))
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

#Hotel User Banner List Admin 
class HotelUserBannerListAdminAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.HotelUserBannerListAdminSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        instance = models.HotelUserPhoto.objects.filter(hotel_user_owner_id__hotel_user_owner_id=int(user_id))
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




#Start Hotel User Profile View Set

class HotelUserProfileAdminViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = models.HotelUserOwner.objects.all()
        user = get_object_or_404(queryset, hotel_user_owner_id=pk)
        serializer = HotelSerializers.HotelUserProfileAdminSerializer(user, context={"request": request})
        return Response({"error": False, "message": "Single User Data", "data": serializer.data})


    def update(self, request, pk=None):
            
            queryset = models.HotelUserOwner.objects.all()
            up_profile = get_object_or_404(queryset, pk=pk)
            serializer = HotelSerializers.HotelUserProfileUpdateAdminSerializer(up_profile, data=request.data, context={"request": request}, partial=True)
            print(serializer)
            serializer.is_valid()
            serializer.save()
            return Response({"error": False, "message": "Data Has been Updated"})  

#End Hotel User Profile View Set


#Start Room Booking List

# class RoomBookListAdminAPIView(viewsets.ViewSet):

#     def list(self, request):
#         if request.GET.get('user_id'):
#             user_id = request.GET.get('user_id')
#             room_list = models.RoomCartDetails.objects.filter(room_id__hotel_id__hotel_user_id=int(user_id)) 

#             serializer = HotelSerializers.HotelRoomCartSerializer(room_list, many=True, context={"request": request})
#             return Response({"error": False, "message": "Room Book Data List", "data": serializer.data})
#         else:
#             return Response({"error": False, "message": "Room Book Not found"})

# RoomBookListAdminAPIView
class RoomBookListAdminAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.HotelRoomCartSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        instance = models.RoomCartDetails.objects.filter(room_id__hotel_id__hotel_user_id=int(user_id)).order_by('-room_id')
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# class HotelBookingDetailsSearchViewSet(viewsets.ViewSet):

#     def list(self, request):
#         if 'user_id' in request.GET and 'key' in request.GET:
#             user_id = request.GET.get('user_id')
#             key = request.GET.get('key')
#             booking_datail = models.RoomCartDetails.objects.filter(hotel_user_owner_id__hotel_user_owner_id=int(user_id))
#             queryset = booking_datail.filter(Q(hotel_discount_name__contains=str(key)) | Q(start_time_date__contains=str(key)) | Q(end_time_date__contains=str(key)) | Q(offer_max_amount_id__max_amount__contains=str(key)) | Q(offer_max_amount_id__min_amount__contains=str(key))).order_by('-hotel_discount_id')
#             total_count = len(queryset)
#             results = queryset[:10]
#             serializer = HotelSerializers.HotelRoomCartSerializer(results, many=True, context={"request": request})
#             return Response({"error": False, "data": serializer.data, "count": total_count})




# class RecommendedHotelViewSet(viewsets.ViewSet):
#     def list(self, request):
#         hotel_details = models.HotelDetails.objects.filter(is_recommended=True, is_active=True)
#         serializer = serializers.RecommendedHotelDetailsSerializer(hotel_details, many=True, context={"request": request})
#         if len(serializer.data) != 0:
#             return Response({"error": False, "message": "All Recommended Hotel Details List", "data": serializer.data})
#         else:
#             return Response({"error": False, "message": "No Recommended Hotel Found", "data": []})


# SingleRoomBookingAdminAPIView
class SingleRoomBookingAdminAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = HotelSerializers.BookingHotelRoomCartSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        custom_serializer = []
        room_cart = models.RoomCartDetails.objects.filter(room_id__hotel_id__hotel_user_id=int(user_id))
        cart_id_list = []
        for each in room_cart:
            if each.cart_id.cart_id not in cart_id_list:
                cart_id_list.append(each.cart_id.cart_id)
                try:
                    book_list = models.ConfirmBooking.objects.get(cart_id = each.cart_id)
                    custom_serializer.append(book_list)  
                except Exception as e:
                    print(str(e))


        instance = custom_serializer
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HotelSingleBookingSearchViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET and 'key' in request.GET:
            user_id = request.GET.get('user_id')
            key = request.GET.get('key')
            booking = models.ConfirmBooking.objects.filter(user_id__user_id=int(user_id))
            print(booking)
            queryset = booking.filter(Q(booking_id__contains=str(key)) | Q(total_payable_amount__contains=str(key)) | Q(booking_status__contains=str(key)) | Q(user_id__user_name__contains=str(key))).order_by('-booking_id')
            total_count = len(queryset)
            results = queryset[:10]
            serializer = HotelSerializers.BookingHotelRoomCartSerializer(results, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data, "count": total_count})
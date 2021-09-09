from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
from collections import OrderedDict
from . import models
from .password import PassWord, saveRecentSearchHistory, CheckAvailable, OTP, OTPverify
from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers 
import requests
import datetime
from django_filters.rest_framework import DjangoFilterBackend
from HotelAdmin.pagination import PaginationHandlerMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django.db.models import Q
import base64
import io
import PIL.Image as Image
from django.core.files.base import ContentFile
import uuid
import re


# Create your views here.
# Basic Pagination limit/size 
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

""" ViewSet """
# hotel user type  
class HotelUserTypeViewSet(viewsets.ViewSet):

    def list(self, request):
        user_type = models.HotelUserType.objects.all()
        serializer = serializers.HotelUserTypeSerializer(user_type, many=True, context={"request": request})
        response_dict = {"error": False,"message": "All Hotel User Type List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.HotelUserTypeSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Hotel User Type Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel User Type Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.HotelUserType.objects.all()
        user_type = get_object_or_404(queryset, pk=pk)
        serializer = serializers.HotelUserTypeSerializer(user_type, context={"request": request})
        return Response({"error": False, "message": "Single Hotel User Type Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.HotelUserType.objects.all()
            user_type = get_object_or_404(queryset, pk=pk)
            serializer = serializers.HotelUserTypeSerializer(user_type, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Hotel User Type Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel User Type Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.HotelUserType.objects.all()
            user_type = get_object_or_404(queryset, pk=pk)
            user_type.delete()
            return Response({"error": False, "message": "Hotel User Type deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel User Type Not Deleted!"})

# hotel user owner 
class HotelUserOwnerViewSet(viewsets.ViewSet):

    def list(self, request):
        hotel_user_owner = models.HotelUserOwner.objects.all()
        serializer = serializers.HotelUserOwnerSerializer(hotel_user_owner, many=True, context={"request": request})
        response_dict = {"error": False,"message": "All Hotel User Owner List", "data": serializer.data}
        return Response(response_dict)

    # def list(self, request):
    #     hotel_user_owner = models.HotelUserOwner.objects.all()
    #     serializer = serializers.HotelUserOwnerSerializer(hotel_user_owner, many=True, context={"request": request})
    #     user_owner_data = serializer.data
    #     ownerlist=[]

    #     for owner in user_owner_data:
    #         user_type_details = HotelUserType.objects.filter(hotel_user_type_id=owner["hotel_user_type_id"])
    #         user_type_details_serializers = HotelUserTypeSerializer(user_type_details, many=True)
    #         owner["user_type_details"] = user_type_details_serializers.data
    #         ownerlist.append(owner)

    #     response_dict = {"error": False,"message": "All Hotel User Owner List", "data": ownerlist}
    #     return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.HotelUserOwnerSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Hotel User Owner Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel User Owner Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.HotelUserOwner.objects.all()
        hotel_user_owner = get_object_or_404(queryset, pk=pk)
        serializer = serializers.HotelUserOwnerSerializer(hotel_user_owner, context={"request": request})
        return Response({"error": False, "message": "Single Hotel User Owner Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.HotelUserOwner.objects.all()
            hotel_user_owner = get_object_or_404(queryset, pk=pk)
            serializer = serializers.HotelUserOwnerSerializer(hotel_user_owner, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Hotel User Owner Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel User Owner Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.HotelUserOwner.objects.all()
            hotel_user_owner = get_object_or_404(queryset, pk=pk)
            hotel_user_owner.delete()
            return Response({"error": False, "message": "Hotel User Owner deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel User Owner Not Deleted!"})

# hotel detail 
class HotelDetailViewSet(viewsets.ViewSet):
    queryset = models.HotelDetails.objects.all()
    def get_serializer_class(self):
        return serializers.HotelDetailsSerializer 

    def get (self,request):
        return self.list(request)

    def list(self, request):
        if request.GET.get('active') == 'True':
            param  = request.GET.get('active')
            hotel_details = models.HotelDetails.objects.filter(is_active=True) 
        else:
            hotel_details = models.HotelDetails.objects.all()

        serializer = serializers.HotelDetailsSerializer(hotel_details, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Hotel Details List", "data": serializer.data}
        return Response(response_dict)


    def create(self, request):
        try:
            # save into image gallery details serializer
            image_gallery_details_serializer = serializers.ImageGalaryDetailsSerializer(data=request.data, context={"request":request})
            image_gallery_details_serializer.is_valid(raise_exception=True)
            image_gallery_details_serializer.save()
            image_galary_details_id = image_gallery_details_serializer.data['image_galary_details_id']
            # save hotel details info with image gallery details id into hotel details table
            try:
                slug_name = str(request.data["hotel_name"]).replace(' ','-').lower()
            except:
                slug_name = str(request.data["hotel_name"]).replace(' ','-').lower() + str(request.data["hotel_id"])

            hotel_details_list = []
            hotel_detail = {}
            hotel_detail["hotel_name"] = request.data["hotel_name"]
            hotel_detail["slug_name"] = slug_name
            hotel_detail["hotel_reg_no"] = request.data["hotel_reg_no"]
            hotel_detail["hotel_email"] = request.data["hotel_email"]
            hotel_detail["hotel_phone"] = request.data["hotel_phone"]
            hotel_detail["latitude"] = request.data["latitude"]
            hotel_detail["longitude"] = request.data["longitude"]
            hotel_detail["short_address"] = request.data["short_address"]
            hotel_detail["hotel_info"] = request.data["hotel_description"]
            hotel_detail["city_id"] = request.data["city_id"]
            hotel_detail["image_galary_details_id"] = image_galary_details_id
            hotel_detail["hotel_user_id"] = request.data["hotel_user_id"]
            hotel_detail["hotel_type"] = request.data["hotel_type"]
            hotel_details_list.append(hotel_detail)
            serializer = serializers.HotelDetailsSerializer(data=hotel_details_list, many=True, context={"request": request})
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
                    serializer = serializers.ImageSerializer(data=image_list, many=True, context={"request": request})
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
        room = get_object_or_404(queryset, pk=pk)
        serializer = serializers.HotelDetailsSerializer(room, context={"request": request})

        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        print(request.data)
        queryset = models.HotelDetails.objects.all()
        hotel_details = get_object_or_404(queryset, pk=pk)
        print(hotel_details)
        serializer = serializers.HotelDetailsSerializer(hotel_details, data=request.data, context={"request": request})
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            dic = {"error": False, "message": "Data Has been Updated"}
        else:
            dic = {"error": False, "message": "Data Has missing"}
        return Response(dic)
        


    def destroy(self, request, pk=None):
        try:
            queryset = models.HotelDetails.objects.all()
            hotel_details = get_object_or_404(queryset, pk=pk)
            hotel_details.delete()
            return Response({"error": False, "message": "Hotel Details deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel Details Data Dosen't Deleted!"})



# recommended hotel details
class RecommendedHotelViewSet(viewsets.ViewSet):
    def list(self, request):
        hotel_details = models.HotelDetails.objects.filter(is_recommended=True, is_active=True)
        serializer = serializers.RecommendedHotelDetailsSerializer(hotel_details, many=True, context={"request": request})
        if len(serializer.data) != 0:
            return Response({"error": False, "message": "All Recommended Hotel Details List", "data": serializer.data})
        else:
            return Response({"error": False, "message": "No Recommended Hotel Found", "data": []})

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

# agent user 
class AgentUserViewSet(viewsets.ViewSet):

    def list(self, request):
        agents = models.AgentUser.objects.all()
        serializer = serializers.AgentUserSerializer(agents, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Agents List", "data": serializer.data}
        return Response(response_dict)


    def create(self, request):
        try:
            serializer = serializers.AgentUserSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Agent Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Agent Information Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.AgentUser.objects.all()
        agent = get_object_or_404(queryset, pk=pk)
        serializer = serializers.AgentUserSerializer(agent, context={"request": request})
        return Response({"error": False, "message": "Single Agent User Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.AgentUser.objects.all()
            agent = get_object_or_404(queryset, pk=pk)
            serializer = serializers.AgentUserSerializer(agent, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Hotel Agent User Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel Agent User Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.AgentUser.objects.all()
            agent = get_object_or_404(queryset, pk=pk)
            agent.delete()
            return Response({"error": False, "message": "Hotel Agent User deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel Agent User Not Deleted!"})

# get agent by using name
class AgentByNameViewSet(generics.ListAPIView):
    serializer_class = serializers.AgentUserSerializer
    def get_queryset(self):
        name = self.kwargs["name"]
        return models.AgentUser.objects.filter(agent_name=name)

# get agent by using email
class AgentByEmailViewSet(generics.ListAPIView):
    serializer_class = serializers.AgentUserSerializer
    def get_queryset(self):
        email = self.kwargs["email"]
        return models.AgentUser.objects.filter(agent_user_email=email)

# get agent by using phone
class AgentByPhoneViewSet(generics.ListAPIView):
    serializer_class = serializers.AgentUserSerializer
    def get_queryset(self):
        phone = self.kwargs["phone"]
        return models.AgentUser.objects.filter(agent_user_phone=phone)

# guide user 
class GuideUserViewSet(viewsets.ViewSet):

    def list(self, request):
        guides = models.GuideUser.objects.all()
        serializer = serializers.GuideUserSerializer(guides, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Guides List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.GuideUserSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Guides Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Guides Information Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.GuideUser.objects.all()
        guides = get_object_or_404(queryset, pk=pk)
        serializer = serializers.GuideUserSerializer(guides, context={"request": request})
        return Response({"error": False, "message": "Single Guides User Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.GuideUser.objects.all()
            guides = get_object_or_404(queryset, pk=pk)
            serializer = serializers.GuideUserSerializer(guides, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Hotel Guides User Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel Guides User Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.GuideUser.objects.all()
            guides = get_object_or_404(queryset, pk=pk)
            guides.delete()
            return Response({"error": False, "message": "Hotel Guide User deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel Guide User Not Deleted!"})

# deffense user 
class DeffenseUserViewSet(viewsets.ViewSet):

    def list(self, request):
        deffense = models.DeffenseUser.objects.all()
        serializer = serializers.DeffenseUserSerializer(deffense, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Deffense List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.DeffenseUserSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Deffense Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Deffense Information Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.DeffenseUser.objects.all()
        deffense = get_object_or_404(queryset, pk=pk)
        serializer = serializers.DeffenseUserSerializer(deffense, context={"request": request})
        return Response({"error": False, "message": "Single Deffense User Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.DeffenseUser.objects.all()
            deffense = get_object_or_404(queryset, pk=pk)
            serializer = serializers.DeffenseUserSerializer(deffense, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Deffense User Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Deffense User Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.DeffenseUser.objects.all()
            deffense = get_object_or_404(queryset, pk=pk)
            deffense.delete()
            return Response({"error": False, "message": "Deffense User deleted successfully!"})
        except:
            return Response({"error": True, "message": "Deffense User Not Deleted!"})

# offer type 
class OfferTypeViewSet(viewsets.ViewSet):

    def list(self, request):
        offer_type = models.OfferType.objects.all()
        serializer = serializers.OfferTypeSerializer(offer_type, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Offer Type List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.OfferTypeSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Offer Type Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Offer Type Informatioin Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.OfferType.objects.all()
        offer_type = get_object_or_404(queryset, pk=pk)
        serializer = serializers.OfferTypeSerializer(offer_type, context={"request": request})
        return Response({"error": False, "message": "Single Offer Type Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.OfferType.objects.all()
            offer_type = get_object_or_404(queryset, pk=pk)
            serializer = serializers.OfferTypeSerializer(offer_type, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Offer Type Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Offer Type Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.OfferType.objects.all()
            offer_type = get_object_or_404(queryset, pk=pk)
            offer_type.delete()
            return Response({"error": False, "message": "Offer Type deleted successfully!"})
        except:
            return Response({"error": True, "message": "Offer Type Not Deleted!"})

# offer max amount 
class OfferMaxAmountViewSet(viewsets.ViewSet):

    def list(self, request):
        offer_max_amount = models.OfferMaxAmount.objects.all()
        serializer = serializers.OfferMaxAmountSerializer(offer_max_amount, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Offer Max Amount List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.OfferMaxAmountSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Offer Max Amount Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Offer Max Amount Informatioin Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.OfferMaxAmount.objects.all()
        offer_max_amount = get_object_or_404(queryset, pk=pk)
        serializer = serializers.OfferMaxAmountSerializer(offer_max_amount, context={"request": request})
        return Response({"error": False, "message": "Single Offer Max Amount Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.OfferMaxAmount.objects.all()
            offer_max_amount = get_object_or_404(queryset, pk=pk)
            serializer = serializers.OfferMaxAmountSerializer(offer_max_amount, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Offer Max Amount Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Offer Max Amount Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.OfferMaxAmount.objects.all()
            offer_max_amount = get_object_or_404(queryset, pk=pk)
            offer_max_amount.delete()
            return Response({"error": False, "message": "Offer Max Amount deleted successfully!"})
        except:
            return Response({"error": True, "message": "Offer Max Amount Not Deleted!"})

# offer
class OfferViewSet(viewsets.ViewSet):

    def list(self, request):
        offer = models.Offer.objects.all()
        serializer = serializers.OfferSerializer(offer, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Offer List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):

        try:
            serializer = serializers.OfferSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Offer Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Offer Informatioin Not Save."}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = models.Offer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)
        serializer = serializers.OfferSerializer(offer, context={"request": request})
        return Response({"error": False, "message": "Single Offer Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.Offer.objects.all()
            offer = get_object_or_404(queryset, pk=pk)
            serializer = serializers.OfferSerializer(offer, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Offer Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Offer Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.Offer.objects.all()
            offer = get_object_or_404(queryset, pk=pk)
            offer.delete()
            return Response({"error": False, "message": "Offer deleted successfully!"})
        except:
            return Response({"error": True, "message": "Offer Not Deleted!"})

# user 
class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        users = models.User.objects.all()
        serializer = serializers.UserSerializer(users, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All users List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):

        try:
            # user_details_list = []
            user_detail = {}
            user_detail["user_name"] = request.data["name"]
            user_detail["user_email"] = request.data["email"]
            user_detail["user_phone"] = request.data["mobile"]
            user_detail["user_password"] = PassWord(request.data["password"])
            # user_details_list.append(user_detail)

            serializer = serializers.UserRegisterAndroidSerializer(data=user_detail, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            code = OTP(serializer.data['user_id'])
            # sms send code implement here
            da = {'sender_id': 702, 'apiKey': 'QXJlbmFXZWJTZWN1cml0eTpXZWJTZWN1cml0eTcwMw==', 'mobileNo': f'{request.data["mobile"]}', 'message': f'Your Porzotok verification code: {code}'}
            js = json.loads(json.dumps(da))
            res = requests.post(url, data=js)
            
            dict_response = {"error": False, "message": "User Registration Completed Successfully!", "success": True, "data": serializer.data, "code": code}
        except Exception as e:
            dict_response = {"error": True, "message": "Registration Failed. Please try again.", "success": False, "data": {}}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.User.objects.filter(is_active=True)
        user = get_object_or_404(queryset, user_id=pk)
        serializer = serializers.SingleUserSerializer(user, context={"request": request})
        return Response({"error": False, "message": "Single User Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.User.objects.filter(is_active=True)
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

    def destroy(self, request, pk=None):
        try:
            queryset = models.User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            user.delete()
            return Response({"error": False, "message": "User deleted successfully!"})
        except:
            return Response({"error": True, "message": "User Not Deleted!"})

# user login android api
class UserLoginAndroidViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            mobile = request.data["mobile"]
            password = request.data["password"]
            user = models.User.objects.get(user_phone=mobile, user_password=PassWord(password))
            serializer = serializers.UserLoginAndroidSerializer(user, context={"request": request})
            dict_response = {"error": False, "message": "Successfully Login.", "success": True, "data": serializer.data}
        except Exception as e:
            dict_response = {"error": True, "message": "Invalid cradentials.", "success": False, "data": {}}
        return Response(dict_response)


# get user by using name
class UserByNameViewSet(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    def get_queryset(self):
        name = self.kwargs["name"]
        return models.User.objects.filter(user_name=name)

# get user by using email
class UserByEmailViewSet(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    def get_queryset(self):
        email = self.kwargs["email"]
        return models.User.objects.filter(user_email=email)

# get user by using phone
class UserByPhoneViewSet(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    def get_queryset(self):
        phone = self.kwargs["phone"]
        return models.User.objects.filter(user_phone=phone)

#GiftCard
class GiftCardViewSet(viewsets.ViewSet):

    def list(self, request):
        gift_card = models.GiftCard.objects.all()
        serializer = serializers.GiftCardSerializer(gift_card, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Gift Card List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.GiftCardSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Gift Card Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Gift Card Informatioin Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.GiftCard.objects.all()
        gift_card = get_object_or_404(queryset, pk=pk)
        serializer = serializers.GiftCardSerializer(gift_card, context={"request": request})
        return Response({"error": False, "message": "Single Gift Card User Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.GiftCard.objects.all()
            gift_card = get_object_or_404(queryset, pk=pk)
            serializer = serializers.GiftCardSerializer(gift_card, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Gift Card User Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Gift Card User Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.GiftCard.objects.all()
            gift_card = get_object_or_404(queryset, pk=pk)
            gift_card.delete()
            return Response({"error": False, "message": "Gift Card User deleted successfully!"})
        except:
            return Response({"error": True, "message": "Gift Card User Not Deleted!"})

#Event
class EventViewSet(viewsets.ViewSet):

    def list(self, request):
        event = models.Event.objects.all()
        serializer = serializers.EventSerializer(event, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Event List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.EventSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Event Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Event Informatioin Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)
        serializer = serializers.EventSerializer(event, context={"request": request})
        return Response({"error": False, "message": "Single Event User Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.Event.objects.all()
            event = get_object_or_404(queryset, pk=pk)
            serializer = serializers.EventSerializer(event, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Event User Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Event User Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.Event.objects.all()
            event = get_object_or_404(queryset, pk=pk)
            event.delete()
            return Response({"error": False, "message": "Event User deleted successfully!"})
        except:
            return Response({"error": True, "message": "Event User Not Deleted!"})

#EventDetails
class EventDetailsViewSet(viewsets.ViewSet):

    def list(self, request):
        events = models.EventDetails.objects.all()
        serializer = serializers.EventDetailsSerializer(events, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Event Details List", "data": serializer.data}
        return Response(response_dict)
     
    def create(self, request):
        try:
            serializer = serializers.EventDetailsSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Event Details Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Event Details Information Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.EventDetails.objects.all()
        event_details = get_object_or_404(queryset, pk=pk)
        serializer = serializers.EventDetailsSerializer(event_details, context={"request": request})
        return Response({"error": False, "message": "Single Event Details Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.EventDetails.objects.all()
            event_details = get_object_or_404(queryset, pk=pk)
            serializer = serializers.EventDetailsSerializer(event_details, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Event Details Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Event Details Not Updated"}
        return Response(dict_response)


    def destroy(self, request, pk=None):
        try:
            queryset = models.EventDetails.objects.all()
            event_details = get_object_or_404(queryset, pk=pk)
            event_details.delete()
            return Response({"error": False, "message": "Event Details deleted successfully!"})
        except:
            return Response({"error": True, "message": "Event Details Not Deleted!"})

#Payment
class PaymentViewSet(viewsets.ViewSet):
    def list(self, request):
        payment = models.Payment.objects.all()
        serializer = serializers.PaymentSerializer(payment, many=True, context={"request": request})
        return Response({"error": False, "message": "All Payment List", "data": serializer.data})

    def create(self, request):
        try:
            serializer = serializers.PaymentSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Payment Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Payment Data"}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Payment.objects.all()
        payment = get_object_or_404(queryset, pk=pk)
        serializer = serializers.PaymentSerializer(payment, context={"request": request})
        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "Data": serializer_data})

    def update(self, request, pk=None):
        queryset = models.Payment.objects.all()
        payment = get_object_or_404(queryset, pk=pk)
        serializer = serializers.PaymentSerializer(payment, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Hasbeen Updated"})


    def destroy(self, request, pk=None):
        try:
            queryset = models.Payment.objects.all()
            payment = get_object_or_404(queryset, pk=pk)
            payment.delete()
            return Response({"error": False, "message": "Payment deleted successfully!"})
        except:
            return Response({"error": True, "message": "Payment Not Deleted!"})  

#HotelDiscount
class HotelDiscountViewSet(viewsets.ViewSet):
    queryset = models.HotelDiscount.objects.all()
    serializer_class = serializers.HotelDiscountSerializer
    def list(self, request):
        hotel_discount = models.HotelDiscount.objects.all()
        serializer = serializers.HotelDiscountSerializer(hotel_discount, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Hotel Discount List", "data": serializer.data}
        return Response(response_dict)
    def create(self, request):
        try:
            serializer = serializers.HotelDiscountSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Hotel Discount Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel Discount Informatioin Not Save."}
        return Response(dict_response)
    def retrieve(self, request, pk=None):
        queryset = models.HotelDiscount.objects.all()
        hotel_discount = get_object_or_404(queryset, pk=pk)
        serializer = serializers.HotelDiscountSerializer(hotel_discount, context={"request": request})
        return Response({"error": False, "message": "Single Hotel Discount Data", "data": serializer.data})
    def update(self, request, pk=None):
        try:
            queryset = models.HotelDiscount.objects.all()
            hotel_discount = get_object_or_404(queryset, pk=pk)
            serializer = serializers.HotelDiscountSerializer(hotel_discount, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Hotel Discount Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel Discount Not Updated"}
        return Response(dict_response)
    def destroy(self, request, pk=None):
        try:
            queryset = models.HotelDiscount.objects.all()
            hotel_discount = get_object_or_404(queryset, pk=pk)
            hotel_discount.delete()
            return Response({"error": False, "message": "Hotel Discount deleted successfully!"})
        except:
            return Response({"error": True, "message": "Hotel Discount Not Deleted!"})  

#Cupon
class CuponViewSet(viewsets.ViewSet):
    def list(self, request):
        cupon = models.Cupon.objects.all()
        serializer = serializers.CuponSerializer(cupon, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Cupon List", "data": serializer.data}
        return Response(response_dict)
    def create(self, request):
        try:
            serializer = serializers.CuponSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Cupon Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Cupon Informatioin Not Save."}
        return Response(dict_response)
    def retrieve(self, request, pk=None):
        queryset = models.Cupon.objects.all()
        cupon = get_object_or_404(queryset, pk=pk)
        serializer = serializers.CuponSerializer(cupon, context={"request": request})
        return Response({"error": False, "message": "Single Cupon Data", "data": serializer.data})
    def update(self, request, pk=None):
        try:
            queryset = models.Cupon.objects.all()
            cupon = get_object_or_404(queryset, pk=pk)
            serializer = serializers.CuponSerializer(cupon, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Cupon Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Cupon Not Updated"}
        return Response(dict_response)
    def destroy(self, request, pk=None):
        try:
            queryset = models.Cupon.objects.all()
            cupon = get_object_or_404(queryset, pk=pk)
            cupon.delete()
            return Response({"error": False, "message": "Cupon deleted successfully!"})
        except:
            return Response({"error": True, "message": "Cupon Not Deleted!"}) 

# TouristSpot
class TouristSpotViewSet(viewsets.ViewSet):

    def list(self, request):
        tourist_spots = models.TouristSpot.objects.all()
        serializer = serializers.TouristSpotSerializer(tourist_spots, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Tourist Spots List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            # save into image gallery details serializer
            image_gallery_details_serializer = serializers.ImageGalaryDetailsSerializer(data=request.data, context={"request":request})
            image_gallery_details_serializer.is_valid(raise_exception=True)
            image_gallery_details_serializer.save()
            image_galary_details_id = image_gallery_details_serializer.data['image_galary_details_id']
            # save tourist spot with image gallery details id into tourist spot table
            tourist_spot_list = []
            tourist_spot_detail = {}
            tourist_spot_detail["tourist_spot_name"] = request.data["tourist_spot_name"]
            tourist_spot_detail["slug_name"] = request.data["slug_name"]
            tourist_spot_detail["tag_line"] = request.data["tag_line"]
            tourist_spot_detail["description"] = request.data["description"]
            tourist_spot_detail["location"] = request.data["location"]
            tourist_spot_detail["map_address"] = request.data["map_address"]
            tourist_spot_detail["image_galary_details_id"] = image_galary_details_id
            tourist_spot_detail["city_id"] = request.data["city_id"]
            tourist_spot_list.append(tourist_spot_detail)
            serializer = serializers.TouristSpotSerializer(data=tourist_spot_list, many=True, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # save image into image table
            try:
                images = request.FILES.getlist('image')
                for image in list(images):
                    image_list = []
                    image_detail = {}
                    image_detail["Image"] = image
                    image_detail["image_galary_details_id"] = image_galary_details_id
                    image_list.append(image_detail)
                    serializer = serializers.ImageSerializer(data=image_list, many=True, context={"request": request})
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            except Exception as e:
                print(str(e))
            dict_response = {"error": False, "message": "Tourist Spot Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Tourist Spot Information Not Save."}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = models.TouristSpot.objects.all()
        tourist_spot = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TouristSpotSerializer(tourist_spot, context={"request": request})
        return Response({"error": False, "message": "Single Tourist Spot Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.TouristSpot.objects.all()
            tourist_spot = get_object_or_404(queryset, pk=pk)
            serializer = serializers.TouristSpotSerializer(tourist_spot, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Tourist Spot Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Tourist Spot Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.TouristSpot.objects.all()
            tourist_spot = get_object_or_404(queryset, pk=pk)
            tourist_spot.delete()
            return Response({"error": False, "message": "Tourist Spot deleted successfully!"})
        except:
            return Response({"error": True, "message": "Tourist Spot Not Deleted!"})

# Prices
class PriceViewSet(viewsets.ViewSet):
    def list(self, request):
        price = models.Price.objects.all()
        serializer = serializers.PriceSerializer(price, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Price List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.PriceSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Price Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Price Data"}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Price.objects.all()
        price = get_object_or_404(queryset, pk=pk)
        serializer = serializers.PriceSerializer(price, context={"request": request})
        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "Data": serializer_data})

    def update(self, request, pk=None):
        queryset = models.Price.objects.all()
        price = get_object_or_404(queryset, pk=pk)
        serializer = serializers.PriceSerializer(price, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Hasbeen Updated"})


    def destroy(self, request, pk=None):
        try:
            queryset = models.Price.objects.all()
            price = get_object_or_404(queryset, pk=pk)
            price.delete()
            return Response({"error": False, "message": "Price deleted successfully!"})
        except:
            return Response({"error": True, "message": "Price Not Deleted!"})

#ImageGalaryDetails
class ImageGalaryDetailsAPIView(viewsets.ModelViewSet):
    queryset = models.ImageGalaryDetails.objects.all()
    serializer_class = serializers.ImageGalaryDetailsSerializer 

#Image
class ImageAPIView(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    def get_serializer_class(self):
        return serializers.ImageSerializer 

    def get (self,request):
        return self.list(request)
    #serializer_class = serializers.ImageSerializer 
    def list(self, request):
        if request.GET.get('galley_id'):
            galley_id = request.GET.get('galley_id')
            
            imagelist = models.Image.objects.filter(image_galary_details_id__image_galary_details_id = int(galley_id))
        else:
            imagelist = models.Image.objects.all()
        serializer = serializers.ImageSerializer(imagelist, many=True, context={"request": request})
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
                serializer = serializers.ImageSerializer(data=image_list, many=True, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
            response_dict = {"error": False, "message": f"Image Uploaded in Gallary and The ID {request.data['image_galary_details_id']}"}
        except Exception as e:
            print(str(e))
            response_dict = {"error": False, "message": f"Image Not Uploaded ",}

        return Response(response_dict)
#Floor
class FloorViewSet(viewsets.ViewSet):
    def list(self, request):
        floor = models.Floor.objects.all()
        serializer = serializers.FloorSerializer(floor, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Floor List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.FloorSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Floor Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Floor Data"}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Floor.objects.all()
        floor = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FloorSerializer(floor, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "Data": serializer.data})

    def update(self, request, pk=None):
        queryset = models.Floor.objects.all()
        floor = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FloorSerializer(floor, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Hasbeen Updated"})
    def destroy(self, request, pk=None):
        try:
            queryset = models.Floor.objects.all()
            floor = get_object_or_404(queryset, pk=pk)
            floor.delete()
            return Response({"error": False, "message": "Floor deleted successfully!"})
        except:
            return Response({"error": True, "message": "Floor Not Deleted!"})

# Room 
class RoomViewSet(viewsets.ViewSet):

    # queryset = models.Room.objects.all()
    # def get_serializer_class(self):
    #     return serializers.RoomSerializer 

    # def get (self,request):
    #     return self.list(request)

    def list(self, request):
        if request.GET.get('hotel_id'):
            hotel_id = request.GET.get('hotel_id')
            rooms = models.Room.objects.filter(hotel_id__hotel_id=int(hotel_id)) 
        else:
            rooms = models.Room.objects.all()

        serializer = serializers.RoomSerializer(rooms, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Room List", "data": serializer.data}
        return Response(response_dict)



    def create(self, request):

        try:
            # save into image gallery details serializer
            image_gallery_details_serializer = serializers.ImageGalaryDetailsSerializer(data=request.data, context={"request":request})
            image_gallery_details_serializer.is_valid(raise_exception=True)
            image_gallery_details_serializer.save()

            image_galary_details_id = image_gallery_details_serializer.data['image_galary_details_id']

            # save price details into price table
            price_list = []
            price_detail = {}
            price_detail["price"] = request.data['price']
            price_detail["offer_price"] = request.data['offer_price']
            price_detail["price_entry_date"] = request.data['price_entry_date']
            price_detail["price_type"] = request.data['price_type']
            price_list.append(price_detail)
            price_serializer = serializers.PriceSerializer(data=price_list, many=True, context={"request": request})
            price_serializer.is_valid(raise_exception=True)
            price_serializer.save()
            price_details_id = price_serializer.data[0]['price_id'] 

            # save room info with image gallery details id into room info table
            room_details_list = []
            room_detail = {}
            room_detail["room_name"] = request.data["room_name"]
            room_detail["room_no"] = request.data["room_no"]
            room_detail["hotel_id"] = request.data["hotel_id"]
            room_detail["floor_id"] = request.data["floor_id"]
            room_detail["room_status"] = request.data["room_status"]
            room_detail["price_id"] = price_details_id
            room_detail["room_description"] = request.data["room_description"]
            room_detail["image_galary_details_id"] = image_galary_details_id
            room_detail["is_active"] = request.data["is_active"]
            room_detail["hotel_discount_id"] = request.data["hotel_discount_id"]
            room_details_list.append(room_detail)

            room_serializer = serializers.RoomSerializer(data=room_details_list, many=True, context={"request": request})
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
                    serializer = serializers.ImageSerializer(data=image_list, many=True, context={"request": request})
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            except Exception as e:
                print(str(e))
                
            dict_response = {"error": False, "message": "Room Information Save Successfully!"}
        except Exception as e:
            print(str(e))
            dict_response = {"error": True, "message": "Room Information Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Room.objects.all()
        room = get_object_or_404(queryset, pk=pk)
        serializer = serializers.RoomSerializer(room, context={"request": request})

        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "Data": serializer_data})

    def update(self, request, pk=None):
        queryset = models.Room.objects.all()
        room = get_object_or_404(queryset, pk=pk)
        serializer = serializers.RoomSerializer(room, data=request.data, context={"request": request})
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

#FoodMenu
class FoodMenuViewSet(viewsets.ViewSet):
    def list(self, request):
        food_menu = models.FoodMenu.objects.all()
        serializer = serializers.FoodMenuSerializer(food_menu, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Food Menu List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):

        try:
            # save price details into price table
            price_list = []
            price_detail = {}
            price_detail["price"] = request.data['price']
            price_detail["offer_price"] = request.data['offer_price']
            price_detail["price_entry_date"] = request.data['price_entry_date']
            price_detail["price_type"] = request.data['price_type']
            price_list.append(price_detail)
            price_serializer = serializers.PriceSerializer(data=price_list, many=True, context={"request": request})
            price_serializer.is_valid(raise_exception=True)
            price_serializer.save()
            price_details_id = price_serializer.data[0]['price_id']
            # save Food Menu info with image gallery details id into Food Menu info table
            food_menu_details_list = []
            food_menu_detail = {}
            food_menu_detail["food_name"] = request.data["food_name"]
            food_menu_detail["hotel_id"] = request.data["hotel_id"]
            food_menu_detail["price_id"] = price_details_id
            food_menu_detail["food_image"] = request.FILES["food_image"]
            food_menu_detail["is_active"] = request.data["is_active"]
            food_menu_details_list.append(food_menu_detail)
            food_menu_serializer = serializers.FoodMenuSerializer(data=food_menu_details_list, many=True, context={"request": request})
            food_menu_serializer.is_valid(raise_exception=True)
            food_menu_serializer.save()
            dict_response = {"error": False, "message": "Food Menu Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Food Menu Information Not Save."}
        return Response(dict_response)
    
    def retrieve(self, request, pk=None):
        queryset = models.FoodMenu.objects.all()
        food_menu = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FoodMenuSerializer(food_menu, context={"request": request})
        return Response({"error": False, "message": "Single Food Menu Data", "data": serializer.data})
    def update(self, request, pk=None):
        try:
            queryset = models.FoodMenu.objects.all()
            food_menu = get_object_or_404(queryset, pk=pk)
            serializer = serializers.FoodMenuSerializer(food_menu, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Food Menu Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Food Menu Not Updated"}
        return Response(dict_response)
    def destroy(self, request, pk=None):
        try:
            queryset = models.FoodMenu.objects.all()
            food_menu = get_object_or_404(queryset, pk=pk)
            food_menu.delete()
            return Response({"error": False, "message": "Food Menu deleted successfully!"})
        except:
            return Response({"error": True, "message": "Food Menu Not Deleted!"}) 

#Package
class PackageViewSet(viewsets.ViewSet):

    def list(self, request):
        package = models.Package.objects.all()
        serializer = serializers.PackageSerializer(package, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Package List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        print(request.data)
        try:
            # save price details into price table
            price_list = []
            price_detail = {}
            price_detail["price"] = request.data['price']
            price_detail["offer_price"] = request.data['offer_price']
            price_detail["price_entry_date"] = request.data['price_entry_date']
            price_detail["price_type"] = request.data['price_type']
            price_list.append(price_detail)
            price_serializer = serializers.PriceSerializer(data=price_list, many=True, context={"request": request})
            price_serializer.is_valid(raise_exception=True)
            price_serializer.save()
            price_details_id = price_serializer.data[0]['price_id']
            # save into package table
            package_list = []
            package_detail = {}
            package_detail["package_name"] = request.data['package_name']
            package_detail["package_image"] = request.FILES["package_image"]
            package_detail["price_id"] = price_details_id
            package_detail["description"] = request.data["description"]
            package_list.append(package_detail)
            package_serializer = serializers.PackageSerializer(data=package_list, many=True, context={"request": request})
            package_serializer.is_valid(raise_exception=True)
            package_serializer.save()
            package_id = package_serializer.data[0]['package_id']

            # save package info
            # save room package
            if 'room_id' in request.data:
                for room in request.data['room_id'].split(','):
                    room_package_list = []
                    room_package_detail = {}
                    room_package_detail["package_id"] = package_id
                    room_package_detail["room_id"] = room
                    room_package_list.append(room_package_detail)
                    room_package_serializer = serializers.RoomPackageSerializer(data=room_package_list, many=True, context={"request": request})
                    room_package_serializer.is_valid(raise_exception=True)
                    room_package_serializer.save()
            # save food menu package
            if 'food_menu_id' in request.data:
                for food_menu in request.data['food_menu_id'].split(','):
                    food_package_list = []
                    food_package_detail = {}
                    food_package_detail["package_id"] = package_id
                    food_package_detail["food_id"] = food_menu
                    food_package_list.append(food_package_detail)
                    food_package_serializer = serializers.FoodMenuPackageSerializer(data=food_package_list, many=True, context={"request": request})
                    food_package_serializer.is_valid(raise_exception=True)
                    food_package_serializer.save()

            # save Facilities package
            if 'facilites_id' in request.data:
                for facilities in request.data['facilites_id'].split(','):
                    facilities_package_list = []
                    facilities_package_detail = {}
                    facilities_package_detail["package_id"] = package_id
                    facilities_package_detail["facilities_id"] = facilities
                    facilities_package_list.append(facilities_package_detail)
                    facilities_package_serializer = serializers.FacilitesPackageSerializer(data=facilities_package_list, many=True, context={"request": request})
                    facilities_package_serializer.is_valid(raise_exception=True)
                    facilities_package_serializer.save()

            # save Tourist Spot package
            if 'tourist_spot_id' in request.data:
                for tourist_spot in request.data['tourist_spot_id'].split(','):
                    tourist_spot_package_list = []
                    tourist_spot_package_detail = {}
                    tourist_spot_package_detail["package_id"] = package_id
                    tourist_spot_package_detail["tourist_spot_id"] = tourist_spot
                    tourist_spot_package_list.append(tourist_spot_package_detail)
                    tourist_spot_package_serializer = serializers.TouristSpotPackageSerializer(data=tourist_spot_package_list, many=True, context={"request": request})
                    tourist_spot_package_serializer.is_valid(raise_exception=True)
                    tourist_spot_package_serializer.save()


            dict_response = {"error": False, "message": "Package Information Save Successfully!"}

        except:
            dict_response = {"error": True, "message": "Package Information Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Package.objects.all()
        package = get_object_or_404(queryset, pk=pk)
        serializer = serializers.PackageSerializer(package, context={"request": request})
        return Response({"error": False, "message": "Single Package Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.Package.objects.all()
            package = get_object_or_404(queryset, pk=pk)
            serializer = serializers.PackageSerializer(package, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Package Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Package Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.Package.objects.all()
            package = get_object_or_404(queryset, pk=pk)
            package.delete()
            return Response({"error": False, "message": "Package deleted successfully!"})
        except:
            return Response({"error": True, "message": "Package Not Deleted!"})

#Facilites
class FacilitesViewSet(viewsets.ViewSet):
    def list(self, request):
        facilites = models.Facilites.objects.all()
        serializer = serializers.FacilitesSerializer(facilites, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Facilites Data List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.FacilitesSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Facilites Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Facilites Data"}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Facilites.objects.all()
        facilites = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FacilitesSerializer(facilites, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "Data": serializer.data})

    def update(self, request, pk=None):
        queryset = models.Facilites.objects.all()
        facilites = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FacilitesSerializer(facilites, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Hasbeen Updated"})
    def destroy(self, request, pk=None):
        try:
            queryset = models.Facilites.objects.all()
            facilites = get_object_or_404(queryset, pk=pk)
            facilites.delete()
            return Response({"error": False, "message": "Facilites deleted successfully!"})
        except:
            return Response({"error": True, "message": "Facilites Not Deleted!"})

#FacilitesGroup
class FacilitesGroupViewSet(viewsets.ViewSet):
    def list(self, request):
        facilites_group = models.FacilitesGroup.objects.all()
        serializer = serializers.FacilitesGroupSerializer(facilites_group, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Facilites Group Data List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:

            facilites_group_details_list = []
            facilites_group_detail = {}
            facilites_group_detail["facilites_id"] = request.data["facilites_id"]
            facilites_group_detail["room_id"] = request.data["room_id"]
            facilites_group_details_list.append(facilites_group_detail)
            facilites_group_serializer = serializers.FacilitesGroupSerializer(data=facilites_group_details_list, many=True, context={"request": request})
            facilites_group_serializer.is_valid(raise_exception=True)
            facilites_group_serializer.save()
            dict_response = {"error": False, "message": "Facilites Group Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Facilites Group Information Not Save."}
        return Response(dict_response)
    
    def retrieve(self, request, pk=None):
        queryset = models.FacilitesGroup.objects.all()
        facilites_group = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FacilitesGroupSerializer(facilites_group, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "Data": serializer.data})
    def update(self, request, pk=None):
        queryset = models.FacilitesGroup.objects.all()
        facilites_group = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FacilitesGroupSerializer(facilites_group, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Hasbeen Updated"})
    def destroy(self, request, pk=None):
        try:
            queryset = models.FacilitesGroup.objects.all()
            facilites_group = get_object_or_404(queryset, pk=pk)
            facilites_group.delete()
            return Response({"error": False, "message": "Facilites Group deleted successfully!"})
        except:
            return Response({"error": True, "message": "Facilites Group Not Deleted!"})

#HotelFacilitesGroup
class HotelFacilitesViewSet(viewsets.ViewSet):

    def list(self, request):
        hotel_facilites = models.HotelFacilites.objects.all()
        serializer = serializers.HotelFacilitesSerializer(hotel_facilites, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Hotel Facilites Data List", "data": serializer.data}
        return Response(response_dict)


    def create(self, request):
        try:
                        # save price details into price table
            price_list = []
            price_detail = {}
            price_detail["price"] = request.data['price']
            price_detail["offer_price"] = request.data['offer_price']
            price_detail["price_entry_date"] = request.data['price_entry_date']
            price_detail["price_type"] = request.data['price_type']
            price_list.append(price_detail)
            price_serializer = serializers.PriceSerializer(data=price_list, many=True, context={"request": request})
            price_serializer.is_valid(raise_exception=True)
            price_serializer.save()
            price_details_id = price_serializer.data[0]['price_id'] 

            # save room info with image gallery details id into room info table
            hotel_facilites_details_list = []
            hotel_facilites_details = {}
            hotel_facilites_details["facilites_id"] = request.data["facilites_id"]
            hotel_facilites_details["hotel_id"] = request.data["hotel_id"]
            hotel_facilites_details["price_id"] = price_details_id
            hotel_facilites_details_list.append(hotel_facilites_details)

            hotel_facilites_serializer = serializers.HotelFacilitesSerializer(data=hotel_facilites_details_list, many=True, context={"request": request})
            hotel_facilites_serializer.is_valid(raise_exception=True)
            hotel_facilites_serializer.save()
            
                
            dict_response = {"error": False, "message": "Hotel Facilites Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel Facilites Information Not Save."}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = models.HotelFacilites.objects.all()
        hotel_facilites = get_object_or_404(queryset, pk=pk)
        serializer = serializers.HotelFacilitesSerializer(hotel_facilites, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "      ": serializer.data})


    def update(self, request, pk=None):
        queryset = models.HotelFacilites.objects.all()
        hotel_facilites = get_object_or_404(queryset, pk=pk)
        serializer = serializers.HotelFacilitesSerializer(hotel_facilites, data=request.data, context={"request": request})
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

#Book
class BookViewSet(viewsets.ViewSet):

    def list(self, request):
        bookings = models.Booking.objects.all()
        serializer = serializers.BookingSerializer(bookings, many=True, context={"request": request})
        booking_datas = serializer.data
        booking_details_list = []

        for booking_data in booking_datas:
            booking_detail = models.Booking.objects.filter(booking_id=booking_data['booking_id'])
            booking_details_serializers = serializers.BookingDetailsSerializer(booking_detail, many=True)
            booking_data["booking_details"] = booking_details_serializers.data
            booking_details_list.append(booking_data)

        response_dict = {"error": False,"message": "All Booking Details List", "data": booking_details_list}
        return Response(response_dict)
        

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
                # serializer.save()
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

#BookingDetailsViewSet
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

#CheckBookingDate frontend
class CheckBookingDate(viewsets.ViewSet):

    def list(self, request):
        if 'cart_id' in request.GET:
            cart_id = request.GET.get('cart_id')
            queryset = models.RoomCartDetails.objects.filter(cart_id__cart_id=cart_id)
            booking = True
            for check in queryset:
                if check.check_in_date is None and check.check_out_date is None:
                    booking = False
                    break

        return Response({"status": booking})

        

        

# cart modelViewSet
class CartModelViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer


# CartByUserModelViewSet
class CartByUserModelViewSet(viewsets.ViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            cart_user = models.Cart.objects.filter(user_id__user_id=user_id, is_active=True).order_by('-cart_id')
            serializer = serializers.CartSerializer(cart_user, many=True, context={"request": request})
            return Response({"error": False, "data":serializer.data})

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
                
            # check_room = models.RoomCartDetails.objects.filter(room_id__room_id=room_id, room_status = '3')
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

#Invoice
class InvoiceViewSet(viewsets.ViewSet):

    def list(self, request):
        invoice = models.Invoice.objects.all()
        serializer = serializers.InvoiceSerializer(invoice, many=True, context={"request": request})
        response_dict = {"error": False, "message": "Invoice List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.InvoiceSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Invoice Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Invoice Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Invoice.objects.all()
        invoice = get_object_or_404(queryset, pk=pk)
        serializer = serializers.InvoiceSerializer(invoice, context={"request": request})
        return Response({"error": False, "message": "Single Invoice Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.Invoice.objects.all()
            invoice = get_object_or_404(queryset, pk=pk)
            serializer = serializers.InvoiceSerializer(invoice, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Invoice Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Invoice Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.Invoice.objects.all()
            invoice = get_object_or_404(queryset, pk=pk)
            invoice.delete()
            return Response({"error": False, "message": "Invoice deleted successfully!"})
        except:
            return Response({"error": True, "message": "Invoice Not Deleted!"})


#ReportType
class ReportTypeViewSet(viewsets.ViewSet):

    def list(self, request):
        reportType = models.ReportType.objects.all()
        serializer = serializers.ReportTypeSerializer(reportType, many=True, context={"request": request})
        response_dict = {"error": False, "message": "ReportType List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.ReportTypeSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "ReportType Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "ReportType Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.ReportType.objects.all()
        reportType = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ReportTypeSerializer(reportType, context={"request": request})
        return Response({"error": False, "message": "Single ReportType Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.ReportType.objects.all()
            reportType = get_object_or_404(queryset, pk=pk)
            serializer = serializers.ReportTypeSerializer(reportType, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "ReportType Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "ReportType Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.ReportType.objects.all()
            reportType = get_object_or_404(queryset, pk=pk)
            reportType.delete()
            return Response({"error": False, "message": "ReportType deleted successfully!"})
        except:
            return Response({"error": True, "message": "ReportType Not Deleted!"})

#Report
class ReportViewSet(viewsets.ViewSet):

    def list(self, request):
        report = models.Report.objects.all()
        serializer = serializers.ReportSerializer(report, many=True, context={"request": request})
        response_dict = {"error": False, "message": "Report List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.ReportSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Report Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Report Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.Report.objects.all()
        report = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ReportSerializer(report, context={"request": request})
        return Response({"error": False, "message": "Single Report Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.Report.objects.all()
            report = get_object_or_404(queryset, pk=pk)
            serializer = serializers.ReportSerializer(report, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Report Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Report Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.Report.objects.all()
            report = get_object_or_404(queryset, pk=pk)
            report.delete()
            return Response({"error": False, "message": "Report deleted successfully!"})
        except:
            return Response({"error": True, "message": "Report Not Deleted!"})

#Affiliate
class AffiliateAPIView(viewsets.ModelViewSet):
    queryset = models.Affiliate.objects.all()
    serializer_class = serializers.AffiliateSerializer

#History
class HistoryViewSet(viewsets.ViewSet):

    def list(self, request):
        history = models.History.objects.all()
        serializer = serializers.HistorySerializer(history, many=True, context={"request": request})
        response_dict = {"error": False, "message": "History List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.HistorySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "History Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "History Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.History.objects.all()
        history = get_object_or_404(queryset, pk=pk)
        serializer = serializers.HistorySerializer(history, context={"request": request})
        return Response({"error": False, "message": "Single History Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.History.objects.all()
            history = get_object_or_404(queryset, pk=pk)
            serializer = serializers.HistorySerializer(history, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "History Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "History Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.History.objects.all()
            history = get_object_or_404(queryset, pk=pk)
            history.delete()
            return Response({"error": False, "message": "History deleted successfully!"})
        except:
            return Response({"error": True, "message": "History Not Deleted!"})

#MembarshipCard
class MembarshipCardViewSet(viewsets.ViewSet):

    def list(self, request):
        membarship_card = models.MembarshipCard.objects.all()
        serializer = serializers.MembarshipCardSerializer(membarship_card, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Membarship Card List", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = serializers.MembarshipCardSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Membarship Card Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Membarship Card Informatioin Not Save."}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = models.MembarshipCard.objects.all()
        membarship_card = get_object_or_404(queryset, pk=pk)
        serializer = serializers.MembarshipCardSerializer(membarship_card, context={"request": request})
        return Response({"error": False, "message": "Single Membarship Card User Data", "data": serializer.data})

    def update(self, request, pk=None):
        try:
            queryset = models.MembarshipCard.objects.all()
            membarship_card = get_object_or_404(queryset, pk=pk)
            serializer = serializers.MembarshipCardSerializer(membarship_card, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Membarship Card User Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Membarship Card User Not Updated"}
        return Response(dict_response)

    def destroy(self, request, pk=None):
        try:
            queryset = models.MembarshipCard.objects.all()
            membarship_card = get_object_or_404(queryset, pk=pk)
            membarship_card.delete()
            return Response({"error": False, "message": "Membarship Card User deleted successfully!"})
        except:
            return Response({"error": True, "message": "Membarship Card User Not Deleted!"})

#BilingAdress
class BilingAdressViewSet(viewsets.ViewSet):
    def list(self, request):
        biling_adress = models.BilingAdress.objects.all()
        serializer = serializers.BilingAdressSerializer(biling_adress, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Biling Address List", "data": serializer.data}
        return Response(response_dict)
    def create(self, request):
        try:
            serializer = serializers.BilingAdressSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Biling Address Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Biling Address Informatioin Not Save."}
        return Response(dict_response)
    def retrieve(self, request, pk=None):
        queryset = models.BilingAdress.objects.all()
        biling_adress = get_object_or_404(queryset, pk=pk)
        serializer = serializers.BilingAdressSerializer(biling_adress, context={"request": request})
        return Response({"error": False, "message": "Single Biling Address Data", "data": serializer.data})
    def update(self, request, pk=None):
        try:
            queryset = models.BilingAdress.objects.all()
            biling_adress = get_object_or_404(queryset, pk=pk)
            serializer = serializers.BilingAdressSerializer(biling_adress, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Biling Address Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Biling Address Not Updated"}
        return Response(dict_response)
    def destroy(self, request, pk=None):
        try:
            queryset = models.BilingAdress.objects.all()
            biling_adress = get_object_or_404(queryset, pk=pk)
            biling_adress.delete()
            return Response({"error": False, "message": "Biling Address deleted successfully!"})
        except:
            return Response({"error": True, "message": "Biling Address Not Deleted!"})

#TransactionDetails
class TransactionDetailsViewSet(viewsets.ViewSet):
    def list(self, request):
        transaction_details = models.TransactionDetails.objects.all()
        serializer = serializers.TransactionDetailsSerializer(transaction_details, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Transaction Details List", "data": serializer.data}
        return Response(response_dict)
    def create(self, request):
        try:
            serializer = serializers.TransactionDetailsSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Transaction Details Informatioin Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Transaction Details Informatioin Not Save."}
        return Response(dict_response)
    def retrieve(self, request, pk=None):
        queryset = models.TransactionDetails.objects.all()
        transaction_details = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TransactionDetailsSerializer(transaction_details, context={"request": request})
        return Response({"error": False, "message": "Single Transaction Details Data", "data": serializer.data})
    def update(self, request, pk=None):
        try:
            queryset = models.TransactionDetails.objects.all()
            transaction_details = get_object_or_404(queryset, pk=pk)
            serializer = serializers.TransactionDetailsSerializer(transaction_details, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                dict_response = {"error": False, "message": "Transaction Details Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Transaction Details Not Updated"}
        return Response(dict_response)
    def destroy(self, request, pk=None):
        try:
            queryset = models.TransactionDetails.objects.all()
            transaction_details = get_object_or_404(queryset, pk=pk)
            transaction_details.delete()
            return Response({"error": False, "message": "Transaction Details deleted successfully!"})
        except:
            return Response({"error": True, "message": "Transaction Details Not Deleted!"})

# Get State By Country
class GetStateByCountry(generics.ListAPIView):
    serializer_class = serializers.StateSerializer
    def get_queryset(self):
        c_id = self.kwargs["c_id"]
        return models.State.objects.filter(country_id__country_id=c_id)

# Get city By State
class GetCityByState(generics.ListAPIView):
    serializer_class = serializers.CitySerializer
    def get_queryset(self):
        s_id = self.kwargs["s_id"]
        return models.City.objects.filter(state_id__state_id=s_id)

#TwentyFourHoursDealsPorzotokView
class TwentyFourHoursDealsPorzotokViewSet(viewsets.ViewSet):
    def list(self, request):
        porzotok_deals = models.TwentyFourHoursDealsPorzotok.objects.all()
        serializer = serializers.TwentyFourHoursDealsPorzotokSerializer(porzotok_deals, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Porzotok Twenty Four Hours Deals List", "data": serializer.data}
        return Response(response_dict)
    def create(self, request):
        try:
            # save into image gallery details serializer
            image_gallery_details_serializer = serializers.ImageGalaryDetailsSerializer(data=request.data, context={"request":request})
            image_gallery_details_serializer.is_valid(raise_exception=True)
            image_gallery_details_serializer.save()
            image_galary_details_id = image_gallery_details_serializer.data['image_galary_details_id']
            # save Twenty Four Hours Deals Porzotok with image gallery details id into TwentyFourHoursDealsPorzotok table
            twenty_four_hours_deals_porzotok_list = []
            twenty_four_hours_deals_porzotok_detail = {}
            twenty_four_hours_deals_porzotok_detail["twenty_four_hours_deals_name"] = request.data["twenty_four_hours_deals_name"]
            twenty_four_hours_deals_porzotok_detail["image_galary_details_id"] = image_galary_details_id
            twenty_four_hours_deals_porzotok_detail["is_active"] = request.data["is_active"]
            twenty_four_hours_deals_porzotok_list.append(twenty_four_hours_deals_porzotok_detail)
            serializer = serializers.TwentyFourHoursDealsPorzotokSerializer(data=twenty_four_hours_deals_porzotok_list, many=True, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # save image into image table
            try:
                images = request.FILES.getlist('image')
                for image in list(images):
                    image_list = []
                    image_detail = {}
                    image_detail["Image"] = image
                    image_detail["image_galary_details_id"] = image_galary_details_id
                    image_list.append(image_detail)
                    serializer = serializers.ImageSerializer(data=image_list, many=True, context={"request": request})
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            except Exception as e:
                print(str(e))
            dict_response = {"error": False, "message": "Porzotok Twenty Four Hours Deals Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Porzotok Twenty Four Hours Deals Information Not Save."}
        return Response(dict_response)
    def retrieve(self, request, pk=None):
        queryset = models.TwentyFourHoursDealsPorzotok.objects.all()
        porzotok_deals = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TwentyFourHoursDealsPorzotokSerializer(porzotok_deals, context={"request": request})
        return Response({"error": False, "message": "Single Twenty Four Hours Deals Data", "data": serializer.data})
    def update(self, request, pk=None):
        try:
            queryset = models.TwentyFourHoursDealsPorzotok.objects.all()
            porzotok_deals = get_object_or_404(queryset, pk=pk)
            serializer = serializers.TwentyFourHoursDealsPorzotokSerializer(porzotok_deals, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Twenty Four Hours Deals Updated Successfully!"}
        except:
            dict_response = {"error": True, "message": "Twenty Four Hours Deals Not Updated"}
        return Response(dict_response)
    def destroy(self, request, pk=None):
        try:
            queryset = models.TwentyFourHoursDealsPorzotok.objects.all()
            porzotok_deals = get_object_or_404(queryset, pk=pk)
            porzotok_deals.delete()
            return Response({"error": False, "message": "Twenty Four Hours Deals deleted successfully!"})
        except:
            return Response({"error": True, "message": "Twenty Four Hours Deals Not Deleted!"})
#Hotel Twenty Four Hours Deals View
class TwentyFourHoursDealsViewSet(viewsets.ViewSet):
    def list(self, request):
        hotel_24_deals = models.TwentyFourHoursDeals.objects.all()
        serializer = serializers.TwentyFourHoursDealsSerializer(hotel_24_deals, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Hotel Twenty Four Hours Deals Data List", "data": serializer.data}
        return Response(response_dict)
    def create(self, request):
        try:
            twenty_four_hours_deals_details_list = []
            twenty_four_hours_deals_detail = {}
            twenty_four_hours_deals_detail["room_id"] = request.data["room_id"]
            twenty_four_hours_deals_detail["twenty_four_hours_deals_porzotok_id"] = request.data["twenty_four_hours_deals_porzotok_id"]
            twenty_four_hours_deals_detail["is_active"] = request.data["is_active"]
            twenty_four_hours_deals_details_list.append(twenty_four_hours_deals_detail)
            twenty_four_hours_deals_serializer = serializers.TwentyFourHoursDealsSerializer(data=twenty_four_hours_deals_details_list, many=True, context={"request": request})
            twenty_four_hours_deals_serializer.is_valid(raise_exception=True)
            twenty_four_hours_deals_serializer.save()
            dict_response = {"error": False, "message": "Hotel Twenty Four Hours Deals Information Save Successfully!"}
        except:
            dict_response = {"error": True, "message": "Hotel Twenty Four Hours Deals Information Not Save."}
        return Response(dict_response)
    def retrieve(self, request, pk=None):
        queryset = models.FacilitesGroup.objects.all()
        facilites_group = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FacilitesGroupSerializer(facilites_group, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "Data": serializer.data})
    def update(self, request, pk=None):
        queryset = models.FacilitesGroup.objects.all()
        facilites_group = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FacilitesGroupSerializer(facilites_group, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Hasbeen Updated"})
    def destroy(self, request, pk=None):
        try:
            queryset = models.FacilitesGroup.objects.all()
            facilites_group = get_object_or_404(queryset, pk=pk)
            facilites_group.delete()
            return Response({"error": False, "message": "Facilites Group deleted successfully!"})
        except:
            return Response({"error": True, "message": "Facilites Group Not Deleted!"})


# class TwentyFourHoursDealsRoomViewSet(viewsets.ViewSet):
#     def list(self, request):
#         room_24_deals = models.Room.objects.filter(is_deals=True)
#         serializer = serializers.RoomDealsSerializer(room_24_deals, many=True, context={"request": request})
#         response_dict = {"error": False, "message": "24 Hours Deals Room Data List", "data": serializer.data}
#         return Response(response_dict)

#Hotel By City View
class HotelByCityViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.GET.get('city_id'):
            city_id = request.GET.get('city_id')
            hotel_by_city = models.HotelDetails.objects.filter(city_id__city_id=int(city_id))
            serializer = serializers.HotelByCitySerializer(hotel_by_city, many=True, context={"request": request})
            return Response({"error": False, "message": "Hotel By City Data List", "data": serializer.data})
        else:
            return Response({"error": True, "message": "Hotel By City Data List"})
#Hotel By State View
class HotelByStateViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.GET.get('state_id'):
            state_id = request.GET.get('state_id')
            hotel_by_state = models.HotelDetails.objects.filter(city_id__state_id__state_id=int(state_id))
            serializer = serializers.HotelByStateSerializer(hotel_by_state, many=True, context={"request": request})
            return Response({"error": False, "message": "Hotel By State Data List", "data": serializer.data})
        else:
            return Response({"error": True, "message": "Hotel By State Data List"})


#CheckRoomAvailablityViewSet
class CheckRoomAvailablityViewSet(viewsets.ViewSet):

    def list(self, request):
        if request.GET.get('room_id'):
            room_id = request.GET.get('room_id')
            check_room = models.RoomCartDetails.objects.filter(room_id__room_id=room_id, room_status = '3')
            serializer = serializers.CheckRoomAvailabilitySerializer(check_room, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data})
        else:
            return Response({"error": True})

class SearchKeyWordViewSet(viewsets.ViewSet):
    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            results = models.RecentSearch.objects.filter(user_id__user_id=user_id).order_by('-created_at')[:5]
            serializer = serializers.SearchKeyWordSerializer(results, many=True, context={"request": request})
            return Response({"error": False, "data": serializer.data})

# check user active or deactive status view set
class CheckUserStatusViewSet(viewsets.ViewSet):

    def list(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
            user = models.User.objects.get(user_id=user_id)
            if user.is_active == True:
                return Response({"is_active": True})
            else:
                return Response({"is_active": False})

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

# update user profile photo for android
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


# update user profile photo for web
class ChangeUserProfilePhotoViewSet(viewsets.ViewSet):
    
    def update(self, request, pk=None):
        json_string = request.data['profile_image']
        format, imgstr = json_string.split(';base64,')
        extension = format.split('/')[-1]
        # generate random name for image
        random = str(uuid.uuid4())
        random = random.upper()
        random = random.replace("-", "")
        data = ContentFile(base64.b64decode(imgstr), name=random + '.' + extension)

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

# OTP viewset
class OTPViewSet(viewsets.ViewSet):

    # verify otp code
    def list(self, request):
        if 'user_id' in request.GET and 'code' in request.GET:
            user_id = request.GET.get('user_id')
            code = request.GET.get('code')
            result = models.OTPmodels.objects.get(user_id__user_id=int(user_id))
            is_auth = OTPverify(result.otp_key, code)
            return Response({"error": False, "data": is_auth})

    # create otp code
    def create(self, request):
        try:
            user_id = int(request.data["user_id"])
            code = OTP(user_id)
            dict_response = {"error": False, "data": code}
        except:
            dict_response = {"error": True}
        return Response(dict_response)


''' 
    * START
    * FRONTEND API View
    * Porzotok frontend API view start from here 
'''

#Single Hotel Details FrontEnd ViewSet
class SingleHotelDetailsFrontEndViewSet(viewsets.ViewSet):

    # retrieve all hotels with room 
    def retrieve(self, request, pk):
        queryset = models.HotelDetails.objects.all()
        single_hotel = get_object_or_404(queryset, slug_name=pk)
        serializer = serializers.HotelInfoFrontEndRoomSerializer(single_hotel, context={"request": request})
        return Response({"error": False, "message": "Single Hotel Details", "data": serializer.data})

# user cart details frontend viewset
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

# Search API 
class SearchModelViewSet(viewsets.ViewSet):

    def list(self, request):

        if 'q' in request.GET:
            key = request.GET.get('q')
            results = models.HotelDetails.objects.filter(hotel_name__contains=str(key))[:5]
            serializer = serializers.FrontEndSearchHotelDetailsSerializer(results, many=True, context={"request": request})
            cities = models.City.objects.filter(city_name__contains=str(key))[:5]
            city_serializer = serializers.FrontEndSearchCitySerializer(cities, many=True, context={"request": request})

            return Response({"error": False, "message": "Search results", "data": serializer.data, "cities": city_serializer.data})


# search details view
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

class ListOfHotelsModelViewSet(viewsets.ViewSet):

    def list(self, request):
        results = models.HotelDetails.objects.filter()
        serializer = serializers.SearchResultDetailsSerializer(results, many=True, context={"request": request})
        return Response({"error": False, "message": "Search results", "data": serializer.data})


# user 
class UserDetailsFrontEndModelViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = models.User.objects.filter(is_active=True)
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.UserDetailsCheckoutFrontEndSerializer(user, context={"request": request})
        return Response({"error": False, "message": "Single User Data", "data": serializer.data})

#Start Review ViewSet
class ReviewViewSet(viewsets.ViewSet):
    def list(self, request):
        if 'hotel_id' in request.GET:
            hotel_id = request.GET.get('hotel_id')
            queryset = models.Review.objects.filter(hotel_id__hotel_id=int(hotel_id))
            serializer = serializers.ReviewSerializer(queryset, many=True, context={"request": request})
        return Response({"error": False, "message": "User Review List.", "data": serializer.data})
    def create(self, request):
        try:
            review_detail = {}
            review_detail["rating"] = request.data["rating"]
            review_detail["review"] = request.data["review"]
            review_detail["hotel_id"] = request.data["hotel_id"]
            review_detail["user_id"] = request.data["user_id"]
            serializer = serializers.ReviewSerializer(data=review_detail, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            review_data = models.BookingReviewBool.objects.get(user_id__user_id=int(request.data["user_id"]),hotel_id__hotel_id=int(request.data["hotel_id"]))
            review_data.is_active=False
            review_data.save()
            dict_response = {"error": False, "message": "Review Completed Successfully!", "data": serializer.data}
        except Exception as e:
            dict_response = {"error": True, "message": "Review Failed. Please try again."}
        return Response(dict_response)
class ReviewReplayViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            if 'user_id' in request.GET and 'hotel_id' in request.GET:
                user_id = request.GET.get('user_id')
                hotel_id = request.GET.get('hotel_id')
                query = models.ReviewReplay.objects.filter(user_id__user_id=user_id, hotel_id__hotel_id=hotel_id)
                serializer = serializers.ReviewReplaySerializer(query, many=True, context={"request": request})
                response_dict = {"error": False,  "data": serializer.data}
            else:
                response_dict = {"error": True,  "data":[]}
        except Exception as e:
            response_dict = {"error": True, "data":[]}
        return Response(response_dict)

class BookingReviewBoolViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            if 'user_id' in request.GET and 'hotel_id' in request.GET:
                user_id = request.GET.get('user_id')
                hotel_id = request.GET.get('hotel_id')
                query = models.BookingReviewBool.objects.filter(user_id__user_id=user_id, hotel_id__hotel_id=hotel_id, is_active=True)
                serializer = serializers.BookingReviewBoolSerializer(query, many=True, context={"request": request})
                response_dict = {"error": False, "message": "Booking Review Bool List", "data": serializer.data}
            else:
                response_dict = {"error": True, "message": "Error in GET request", "data":[]}
        except Exception as e:
            response_dict = {"error": True, "message": "Error in Queryset", "data":[]}
        return Response(response_dict)


#Map ViewSet
class MapViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = models.HotelDetails.objects.all()
        hotel = get_object_or_404(queryset, hotel_id=pk)
        serializer = serializers.MapSerializer(hotel, context={"request": request})
        return Response({"error": False, "data": serializer.data})
     
''' 
    * END
    * FRONTEND API View
    * Porzotok frontend API view end 
'''
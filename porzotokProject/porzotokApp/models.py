from django.db import models
import PIL
from .password import PassWord

from django.db import OperationalError
import datetime
import django
import pyotp




class Country(models.Model):  

	country_id = models.AutoField(primary_key=True)
	country_name = models.CharField(max_length=75, unique=True)
	
	def __str__(self):
		return str(self.country_name)


class State(models.Model):
	 
	state_id = models.AutoField(primary_key=True)
	country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
	state_name = models.CharField(max_length=85,unique=True)

	def __str__(self):
		return str(self.state_name)


class City(models.Model):
	city_id = models.AutoField(primary_key=True)
	state_id = models.ForeignKey(State, on_delete=models.CASCADE)
	city_name = models.CharField(max_length=100, unique=True)
	is_popular = models.BooleanField(default=True)
	tag_line = models.CharField(max_length=100,null=True, blank=True)
	city_slug_name = models.CharField(max_length=100, unique=True,null=True, blank=True)
	city_image = models.ImageField(upload_to ='media/city/%Y/%d/%b', null=True, blank=True)

	def __str__(self):
		return str(self.city_name)

	def clean(self):
		self.city_slug_name = str(self.city_name).lower().replace(" ", "-").replace("'", "")


class Gendar(models.TextChoices):
	MALE = '1', 'Male'
	FEMALE = '2', 'Female'
	OTHER = '3', 'Other'


class User(models.Model):

	user_id = models.AutoField(primary_key=True)
	user_name = models.CharField(max_length=50)
	user_email = models.CharField(max_length=50, unique=True)
	user_phone = models.CharField(max_length=14, unique=True)
	gender = models.CharField(choices=Gendar.choices, max_length=20, null=True, blank=True)
	city_id = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
	user_password = models.CharField(max_length=64)
	user_national_id_card = models.CharField(max_length=25, null=True, blank=True)
	# nid_front_image = models.ImageField(upload_to='media/user/nid/%Y/%d/%b', null=True, blank=True)
	# nid_back_image = models.ImageField(upload_to='media/user/nid/%Y/%d/%b', null=True, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	user_short_address = models.CharField(max_length=200, null=True, blank=True)
	user_image = models.ImageField(upload_to ='media/user/%Y/%d/%b', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=False)
	block_status = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user_name)

class HotelUserType(models.Model):

	hotel_user_type_id = models.AutoField(primary_key=True)
	hotel_user_type_name = models.CharField(max_length=100)

	def __str__(self):
		return str(self.hotel_user_type_name)


class HotelUserOwner(models.Model):

	hotel_user_owner_id = models.AutoField(primary_key=True)
	hotel_name = models.CharField(max_length=100)
	hotel_owner_name = models.CharField(max_length=100)
	hotel_owner_national_id_card = models.CharField(max_length=20)
	hotel_user_email = models.CharField(max_length=75, unique=True)
	hotel_user_phone = models.CharField(max_length=14, unique=True)
	gendar = models.CharField(choices=Gendar.choices, max_length=20, null=True, blank=True)
	city_id = models.ForeignKey(City, on_delete=models.CASCADE)
	hotel_user_password = models.CharField(max_length=64)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	hotel_user_type_id = models.ForeignKey(HotelUserType, on_delete=models.CASCADE)


	def clean(self):

		if len(self.hotel_user_password) != 64:
			self.hotel_user_password = PassWord(self.hotel_user_password)

	def __str__(self):
		return str(self.hotel_owner_name)

class HotelUserPhoto(models.Model):
	photo_id = models.AutoField(primary_key=True)
	banner_photo = models.ImageField(upload_to ='banner/%Y/%d/%b', null=True, blank=True)
	logo_photo = models.ImageField(upload_to ='logo/%Y/%d/%b', null=True, blank=True)
	hotel_user_owner_id = models.ForeignKey(HotelUserOwner,on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.hotel_user_owner_id)

	def save(self, *args, **kwargs):
		super(HotelUserPhoto, self).save(*args, **kwargs)
		if self.banner_photo != None:
			img = PIL.Image.open(self.banner_photo.path)
			if img.height > 255 or img.width > 255:
				output_size=(255,255)
				img.thumbnail (output_size)
				img.save(self.banner_photo.path)
		if self.logo_photo != None:
			img_logo = PIL.Image.open(self.logo_photo.path)
			if img_logo.height > 90 or img_logo.width > 90:
				output_size=(90,90)
				img_logo.thumbnail (output_size)
				img_logo.save(self.logo_photo.path)


class AgentUser(models.Model):

	agent_user_id = models.AutoField(primary_key=True)
	agent_name = models.CharField(max_length=100)
	agent_national_id_card = models.CharField(max_length=20)
	agent_user_email = models.CharField(max_length=75, unique=True)
	agent_user_phone = models.CharField(max_length=14, unique=True)
	agent_photo = models.ImageField(upload_to ='agent/%Y/%d/%b', null=True, blank=True)
	gendar = models.CharField(choices=Gendar.choices, max_length=20, null=True, blank=True)
	city_id = models.ForeignKey(City, on_delete=models.CASCADE)
	agent_user_password = models.CharField(max_length=64)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def clean(self):

		if len(self.agent_user_password) != 64:
			self.agent_user_password = PassWord(self.agent_user_password)

	def __str__(self):
		return str(self.agent_name)



class GuideUser(models.Model):
	class GuideStatus(models.TextChoices):
		BOOK = '1', 'Book'
		AVAILABLE = '2', 'Available'

	guide_id = models.AutoField(primary_key=True)
	guide_name = models.CharField(max_length=100)
	guide_national_id_card = models.CharField(max_length=20)
	user_email = models.CharField(max_length=75, unique=True)
	user_phone = models.CharField(max_length=14, unique=True)
	guide_photo = models.ImageField(upload_to ='guide/%Y/%d/%b', null=True, blank=True)
	gendar = models.CharField(choices=Gendar.choices, max_length=20, null=True, blank=True)
	city_id = models.ForeignKey(City, on_delete=models.CASCADE)
	guide_password = models.CharField(max_length=64)
	guide_short_address = models.CharField(max_length=200, blank=True)
	guide_status = models.CharField(choices=GuideStatus.choices, max_length=20, null=True, blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def clean(self):

		if len(self.guide_password) != 64:
			self.guide_password = PassWord(self.guide_password)

	def __str__(self):
		return str(self.guide_name)


class DeffenseUser(models.Model):

	deffense_id = models.AutoField(primary_key=True)
	deffense_department_name = models.CharField(max_length=100)
	deffense_user_email = models.CharField(max_length=75, unique=True)
	deffense_user_phone = models.CharField(max_length=14, unique=True)
	gendar = models.CharField(choices=Gendar.choices, max_length=20, null=True, blank=True)
	deffense_photo = models.ImageField(upload_to ='deffense/%Y/%d/%b', null=True, blank=True)
	city_id = models.ForeignKey(City, on_delete=models.CASCADE)
	deffense_password = models.CharField(max_length=64)
	deffense_short_address = models.CharField(max_length=200, blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def clean(self):

		if len(self.deffense_password) != 64:
			self.deffense_password = PassWord(self.deffense_password)

	def __str__(self):
		return str(self.deffense_department_name)

class ImageGalaryDetails(models.Model):

	image_galary_details_id = models.AutoField(primary_key=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.image_galary_details_id)


class Image(models.Model):

	image_id = models.AutoField(primary_key=True)
	Image =  models.ImageField(upload_to='media/image/%Y/%d/%b')
	created_at = models.DateTimeField(auto_now_add=True)
	image_galary_details_id = models.ForeignKey(ImageGalaryDetails, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.image_galary_details_id)


class OfferType(models.Model):

	offer_type_id = models.AutoField(primary_key=True)
	offer_type_name = models.CharField(blank=True,max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.offer_type_name)


class OfferMaxAmount(models.Model):

	offer_max_amount_id = models.AutoField(primary_key=True)
	max_amount = models.DecimalField(max_digits=10, decimal_places=2)
	min_amount = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.max_amount)


class Offer(models.Model):

	offer_id = models.AutoField(primary_key=True)
	offer_name = models.CharField(blank=True,max_length=20)
	offer_type_id = models.ForeignKey(OfferType,on_delete=models.CASCADE)
	offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
	offer_image = models.ImageField(upload_to ='media/offer/%Y/%d/%b')
	offer_max_amount_id = models.ForeignKey(OfferMaxAmount,on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	offer_reason = models.CharField(blank=True,max_length=50)
	start_time_date = models.DateField()
	end_time_date = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	

	def __str__(self):
		return str(self.offer_type_id)		


class Cupon(models.Model):
	cupon_id = models.AutoField(primary_key=True)
	cupon_name = models.CharField(blank=True,max_length=100)
	cupon_code = models.CharField(max_length=50)
	start_date = models.DateField()
	end_date = models.DateField()
	offer_max_amount_id = models.ForeignKey(OfferMaxAmount,on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.cupon_code)


class GiftCard(models.Model):
	gift_card_id = models.AutoField(primary_key=True)
	gift_card_name = models.CharField(max_length=300)
	gift_card_number = models.CharField(max_length=100)
	gift_card_pin = models.CharField(max_length=100)
	gift_card_exp_date =  models.DateField()
	gift_card_amount = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.gift_card_name)


class TouristSpot(models.Model):

	tourist_spot_id = models.AutoField(primary_key=True)
	tourist_spot_name = models.CharField(max_length=100)
	slug_name = models.CharField(max_length=100, unique=True,null=True, blank=True)
	tag_line = models.CharField(max_length=100,null=True, blank=True)
	description = models.TextField()
	location = models.CharField(max_length=255,null=True, blank=True)
	map_address = models.CharField(max_length=200, blank=True)
	image_galary_details_id = models.ForeignKey(ImageGalaryDetails,on_delete=models.CASCADE)
	city_id = models.ForeignKey(City, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.tourist_spot_name)

	def clean(self):
		try:
			self.slug_name = str(self.tourist_spot_name).replace(' ','-').replace("'", "").lower()
		except:
			self.slug_name = str(self.tourist_spot_name).replace(' ','-').replace("'", "").lower() + str(self.tourist_spot_id)


class Price(models.Model):

	class PriceType(models.TextChoices):
		ROOM = '1', 'Room Price'
		FOOD = '2', 'Food Price'
		FACILITIES = '3', 'Facilites Price'
		PACKAGE = '4', 'Package Price'

	price_id = models.AutoField(primary_key=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	price_entry_date = models.DateField()
	offer_price = models.DecimalField(max_digits=10, decimal_places=2)
	price_type = models.CharField(choices=PriceType.choices, max_length=20, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.price)



class HotelDetails(models.Model):
	class HotelType(models.TextChoices):
		ONESTAR = '1', '1 STAR'
		TWOSTAR = '2', '2 STAR'
		THREETAR = '3', '3 STAR'
		FOURSTAR = '4', '4 STAR'
		FIVESTAR = '5', '5 STAR'
	hotel_id = models.AutoField(primary_key=True)
	hotel_name = models.CharField(max_length=100)
	slug_name = models.CharField(max_length=100, unique=True,null=True, blank=True)
	hotel_reg_no = models.CharField(max_length=100, unique=True)
	hotel_email = models.CharField(max_length=75, unique=True)
	hotel_phone = models.CharField(max_length=14, unique=True)
	latitude = models.CharField(max_length=50, null=True, blank=True, default="21.4285")
	longitude = models.CharField(max_length=50, null=True, blank=True, default="91.9702")
	short_address = models.CharField(max_length=200, blank=True)
	city_id = models.ForeignKey(City, on_delete=models.CASCADE)
	hotel_info = models.TextField()
	image_galary_details_id = models.ForeignKey(ImageGalaryDetails, on_delete=models.CASCADE)
	hotel_user_id = models.ForeignKey(HotelUserOwner,on_delete=models.CASCADE)
	spot = models.ForeignKey(TouristSpot,on_delete=models.CASCADE, null=True, blank=True)
	hotel_type = models.CharField(choices=HotelType.choices, max_length=20, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_recommended = models.BooleanField(default=False)
	def __str__(self):
		return str(self.hotel_name)
	def clean(self):
		try:
			self.slug_name = str(self.hotel_name).replace(' ','-').lower()
		except:
			self.slug_name = str(self.hotel_name).replace(' ','-').lower() + str(self.hotel_id)

class HotelDiscount(models.Model):
	hotel_discount_id = models.AutoField(primary_key=True)
	hotel_discount_name = models.CharField(max_length=100)
	start_time_date = models.DateField()
	end_time_date = models.DateField()
	offer_max_amount_id = models.ForeignKey(OfferMaxAmount,on_delete=models.CASCADE, null=True, blank=True)
	hotel_user_owner_id = models.ForeignKey(HotelUserOwner,on_delete=models.CASCADE, default=1)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.hotel_discount_name)





class Floor(models.Model):
	floor_id = models.AutoField(primary_key=True)
	floor_no = models.CharField(max_length=14, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.floor_no)


class Room(models.Model):

	class RoomStatus(models.TextChoices):
		BOOK = '1', 'Book'
		AVAILABLE = '2', 'Available'

	# AllowMaxPeople = [
	# 	('1', '1 Person'),
	# 	('2', '2 Person'),
	# 	('3', '3 Person'),
	# 	('4', '4 Person'),
	# 	('5', '5 Person'),
	# ]

	room_id = models.AutoField(primary_key=True)
	room_name = models.CharField(max_length=100)
	room_no = models.CharField(max_length=14)
	floor_id= models.ForeignKey(Floor, on_delete=models.CASCADE)
	hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
	room_status = models.CharField(choices=RoomStatus.choices, max_length=20, null=True, blank=True)
	price_id = models.ForeignKey(Price, on_delete=models.CASCADE)
	# number_of_people = models.CharField(choices=AllowMaxPeople, max_length=50)
	room_description = models.TextField()
	image_galary_details_id = models.ForeignKey(ImageGalaryDetails,on_delete=models.CASCADE)
	is_deals = models.BooleanField(default=False)
	deal_start_date = models.DateTimeField(blank=True, null=True)
	allow_offer_percent = models.CharField(blank=True, null=True, max_length=20)
	offer_discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	hotel_discount_id = models.ForeignKey(HotelDiscount, on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('hotel_id', 'room_no',)

	def __str__(self):
		return str(self.room_name)


class TwentyFourHoursDealsPorzotok(models.Model):
	twenty_four_hours_deals_porzotok_id = models.AutoField(primary_key=True)
	twenty_four_hours_deals_name = models.CharField(max_length=100)
	image_galary_details_id = models.ForeignKey(ImageGalaryDetails,on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.twenty_four_hours_deals_name)
		
class TwentyFourHoursDeals(models.Model):
	twenty_four_hours_deals_id = models.AutoField(primary_key=True)
	room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
	twenty_four_hours_deals_porzotok_id = models.ForeignKey(TwentyFourHoursDealsPorzotok, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.room_id)


class FoodMenu(models.Model):

	food_menu_id = models.AutoField(primary_key=True)
	food_name = models.CharField(max_length=100)
	hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
	price_id = models.ForeignKey(Price, on_delete=models.CASCADE)
	food_image = models.ImageField(upload_to ='media/food/%Y/%d/%b')
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.food_name)


	

class Facilites(models.Model):
	facilites_id = models.AutoField(primary_key=True)
	facilites_name = models.CharField(max_length=100)
#	facilites_icon = models.ImageField(upload_to ='media/facilites/%Y/%d/%b')
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.facilites_name)
		
class FacilitesGroup(models.Model):
	facilites_group_id = models.AutoField(primary_key=True)
	facilites_id = models.ForeignKey(Facilites, on_delete=models.CASCADE)
	room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.facilites_id)



class HotelFacilites(models.Model):

	hotel_facilites_id = models.AutoField(primary_key=True)
	facilites_id = models.ForeignKey(Facilites, on_delete=models.CASCADE)
	hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
	price_id = models.ForeignKey(Price, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.facilites_id)



class Package(models.Model):

	package_id = models.AutoField(primary_key=True)
	package_name = models.CharField(max_length=100)
	package_image = models.ImageField(upload_to ='media/package/%Y/%d/%b')
	price_id = models.ForeignKey(Price, on_delete=models.CASCADE)
	description = models.TextField()
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.package_name)

# room package
class RoomPackage(models.Model):

	room_package_id = models.AutoField(primary_key=True)
	package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
	room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.package_id)

# FoodMenuPackage
class FoodMenuPackage(models.Model):

	food_package_id = models.AutoField(primary_key=True)
	package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
	food_id = models.ForeignKey(FoodMenu, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.package_id)

# Facilities package
class FacilitesPackage(models.Model):

	facilities_package_id = models.AutoField(primary_key=True)
	package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
	facilities_id = models.ForeignKey(Facilites, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.package_id)

# Tourist Spot package
class TouristSpotPackage(models.Model):

	tourist_spot_package_id = models.AutoField(primary_key=True)
	package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
	tourist_spot_id = models.ForeignKey(TouristSpot, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.package_id)

# class PackageDetails(models.Model):

# 	package_details_id = models.AutoField(primary_key=True)
# 	package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
# 	price_id = models.ForeignKey(Price, on_delete=models.CASCADE)
# 	room_id = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
# 	food_menu_id = models.ForeignKey(FoodMenu, on_delete=models.CASCADE, blank=True, null=True)
# 	facilites_id = models.ForeignKey(Facilites, on_delete=models.CASCADE, blank=True, null=True)
# 	description = models.TextField()
# 	tourist_spot_id = models.ForeignKey(TouristSpot, on_delete=models.CASCADE)
# 	created_at = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return str(self.package_id)



class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
	event_name = models.CharField(max_length=100)
	start_date = models.DateField()
	end_date = models.DateField()
	event_date = models.DateField()
	event_end_date = models.DateField()
	no_of_people = models.CharField(max_length=20)
	minimum_people = models.CharField(max_length=20)
	price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField()
	event_image = models.ImageField(upload_to ='media/event/%Y/%d/%b')
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.event_name)



class EventDetails(models.Model):
	event_details_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	user_going_status = models.BooleanField(default=True) # True=going and False=interest
	total_member = models.CharField(max_length=20)
	total_cost = models.DecimalField(max_digits=10, decimal_places=2)
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.event_details_id)


class Payment(models.Model):

	payment_method_id = models.AutoField(primary_key=True)
	payment_method_name = models.CharField(max_length=100)
	payment_method_account_no = models.CharField(max_length=14, unique=True)
	payment_method_image = models.ImageField(upload_to ='media/payment/%Y/%d/%b', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.payment_method_name)


class Cart(models.Model):
	cart_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	session_id = models.CharField(max_length=50, unique=True)
	is_active = models.BooleanField(default=True) 
	updated = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.cart_id)


# room CartDetails
class RoomCartDetails(models.Model):
	class RoomStatus(models.TextChoices):
		CART = '1', 'Cart'
		HOLD = '2', 'Hold'
		PENDING = '3', 'Pending'
		COMPLETED = '4', 'Completed'

	room_cart_details_id = models.AutoField(primary_key=True)
	cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
	room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
	check_in_date = models.DateField(null=True, blank=True)
	check_out_date =  models.DateField(null=True, blank=True)
	total_day = models.IntegerField(default=0)
	static_regular_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	static_offer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	is_hold = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	room_status = models.CharField(choices=RoomStatus.choices, max_length=20, default='1')

	class Meta:
		unique_together = ('cart_id', 'room_id',)

	def __str__(self):
		return str(self.room_cart_details_id)

# FoodMenu CartDetails
class FoodMenuCartDetails(models.Model):

	food_cart_details_id = models.AutoField(primary_key=True)
	cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
	food_id = models.ForeignKey(FoodMenu, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('cart_id', 'food_id',)

	def __str__(self):
		return str(self.food_cart_details_id)

# Facilities CartDetails
class FacilitesCartDetails(models.Model):

	facilities_cart_details_id = models.AutoField(primary_key=True)
	cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
	hotel_facilites_id = models.ForeignKey(HotelFacilites, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('cart_id', 'hotel_facilites_id',)

	def __str__(self):
		return str(self.facilities_cart_details_id)

#Package CartDetails
class PackageCartDetails(models.Model):

	package_cart_details_id = models.AutoField(primary_key=True)
	package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
	cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('cart_id', 'package_id',)

	def __str__(self):
		return str(self.package_cart_details_id)


class Booking(models.Model):
	class BookingStatus(models.TextChoices):
		COMPLETED = '1', 'Completed'
		PENDING = '2', 'Pending'

	booking_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
	booking_status = models.CharField(choices=BookingStatus.choices, max_length=20)
	total_amount =  models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	payment_method_id = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
	offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
	cupon_id = models.ForeignKey(Cupon, on_delete=models.CASCADE, null=True, blank=True)
	hotel_discount_id = models.ForeignKey(HotelDiscount, on_delete=models.CASCADE, null=True, blank=True)
	gift_card_id = models.ForeignKey(GiftCard, on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('booking_id', 'cart_id')

	def __str__(self):
		return str(self.booking_id)


class ConfirmBooking(models.Model):
	class BookingStatus(models.TextChoices):
		COMPLETED = '1', 'Completed'
		PENDING = '2', 'Pending'

	confirm_booking_id = models.AutoField(primary_key=True)
	booking_id = models.IntegerField()
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
	booking_status = models.CharField(choices=BookingStatus.choices, max_length=20)
	total_amount =  models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	total_payable_amount =  models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	vat_amount =  models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	vat_percent =  models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	payment_method = models.CharField(max_length=30, null=True, blank=True)
	payment_account_number = models.CharField(max_length=30, null=True, blank=True)
	transaction_code = models.CharField(max_length=50, null=True, blank=True)
	offer_type = models.CharField(max_length=20, null=True, blank=True)
	offer_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	offer_max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	coupon_code = models.CharField(max_length=50, null=True, blank=True)
	coupon_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	coupon_max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	hotel_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	hotel_discount_max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	gift_card_number = models.CharField(max_length=30, null=True, blank=True)
	gift_card_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('booking_id', 'cart_id')

	def __str__(self):
		return str(self.confirm_booking_id)



class BilingAdress(models.Model):
	biling_address_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	address = models.TextField()
	post_code = models.CharField(max_length=64)
	country = models.CharField(max_length=64)
	phone = models.CharField(max_length=15, blank=True)
	email = models.EmailField()
	payment_method_id = models.ForeignKey(Payment, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name)

class TransactionDetails(models.Model):
	transaction_id = models.AutoField(primary_key=True)
	transaction_code = models.CharField(max_length=50)
	payment_account_number = models.CharField(max_length=20)
	transaction_status = models.BooleanField(default=True)
	transaction_time = models.DateTimeField(auto_now_add=True)
	amount = models.DecimalField(max_digits=16, decimal_places=2)
	payment_method_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.transaction_id)


class Invoice(models.Model):
	invoice_id = models.AutoField(primary_key=True)
	confirm_booking_id = models.ForeignKey(ConfirmBooking, on_delete=models.CASCADE)
	date_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.invoice_id)


class Review(models.Model):
	RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
	review_id = models.AutoField(primary_key=True)
	rating = models.IntegerField(choices=RATING_CHOICES)
	review = models.TextField()
	hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.review)

class BookingReviewBool(models.Model):
	booking_review_bool_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return str(self.booking_review_bool_id)

class FrontEndHotelLogo(models.Model):
	logo_id = models.AutoField(primary_key=True)
	logo_photo = models.ImageField(upload_to ='logo_f/%Y/%d/%b', null=True, blank=True)
	def __str__(self):
		return str(self.logo_photo)

class ReviewReplay(models.Model):
	review_replay_id = models.AutoField(primary_key=True)
	review_replay = models.TextField()
	review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
	hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
	logo_id = models.ForeignKey(FrontEndHotelLogo,on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.review_replay)


class ReportType(models.Model):

	report_type_id = models.AutoField(primary_key=True)
	report_type_name = models.CharField(max_length=100)

	def __str__(self):
		return str(self.report_type_name)

class Report(models.Model):

	report_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	report_type_id = models.ForeignKey(ReportType, on_delete=models.CASCADE)
	report = models.TextField()
	report_time = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.report_id)


class Affiliate(models.Model):
	af_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	af_link = models.CharField(max_length=75, unique=True)
	is_active = models.BooleanField(default=False)


	def __str__(self):
		return str(self.af_id)


class MembarshipCard(models.Model):

	class MembarshipStatus(models.TextChoices):
		VIP = '1', 'vip'
		GOLD = '2', 'gold'
		DIMOND = '3', 'dimond'
		PREMIUM = '4', 'premium'
		SILVER = '5', 'silver'
		

	membarship_card_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.CharField(choices=MembarshipStatus.choices, max_length=20, null=True, blank=True)
	booking_count = models.CharField(max_length=155)
	booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
	card_code = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.membarship_card_id)




class History(models.Model):
	history_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hotel_user_type_id = models.ForeignKey(HotelUserType, on_delete=models.CASCADE, null=True, blank=True)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.history_id)

class LoginActivity(models.Model):
	activity_id = models.AutoField(primary_key=True)
	session_id = models.CharField(max_length=100)
	time = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)
	user = models.CharField(max_length=30)
	def __str__(self):
		return str(self.user)

class RecentSearch(models.Model):
	recent_search_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	search_session_id = models.CharField(max_length=50, null=True, blank=True)
	keyword = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.keyword)

class HotelVisitor(models.Model):
	hotel_visitor_id = models.AutoField(primary_key=True)
	hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
	ip_address = models.CharField(max_length=50, unique=True)
	total_view = models.IntegerField()
	date = models.DateField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('hotel_id', 'ip_address')

	def __str__(self):
		return str(self.ip_address)

class OTPmodels(models.Model):
	otp_id = models.AutoField(primary_key=True)
	otp_key = models.CharField(max_length=255, default=pyotp.random_base32(), unique=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user_id)
from django import template
from django.utils.html import format_html

register = template.Library()
from porzotokApp import models
@register.filter(name='hotel_image')

def hotel_image(value):
	em = models.Image.objects.filter(image_galary_details_id__image_galary_details_id = int(value))
	if len(em) != 0:
		img = em[0].Image
	else:
		img = ""
	return img

@register.filter(name='hotel_name_slug')
def hotel_name_slug(value):
	name = str(value).replace(' ', '-')
	return name

@register.filter(name='space_remove')
def space_remove(value):
	name = str(value).replace(' ', '-').replace("'", "")
	return name


@register.filter(name='hotel_all_image')
def hotel_all_image(value):
	em = models.Image.objects.filter(image_galary_details_id__image_galary_details_id = int(value))
	return em

@register.filter(name='hotel_facilities')
def hotel_facilities(value):
	facilities = models.HotelFacilites.objects.filter(hotel_id__hotel_id = int(value))
	return facilities

@register.filter(name='hotel_min_price')
def hotel_min_price(value):
	try:
		room_price = min([each.price_id.offer_price for each in models.Room.objects.filter(hotel_id=value)])
	except:
		room_price = 0
	
	return room_price

@register.filter(name='GetRooms')
def GetRooms(cart_id):
	room_info = []
	try:
		room = models.RoomCartDetails.objects.get(cart_id__cart_id=int(cart_id))

	except:
		room = []

	return room
@register.filter(name='GetRoomNumber')
def GetRoomNumber(cart_id):
	room_info = []
	try:
		room = models.RoomCartDetails.objects.get(cart_id__cart_id=int(cart_id))
		room_no = room.room_id.room_no
	except:
		room_no = ""

	return room_no

# total review count
@register.filter(name='total_review_count')
def total_review_count(value):
	try:
		review_count = len([each.review for each in models.Review.objects.filter(hotel_id=value)])
	except:
		review_count = 0
	return review_count

# average rating count
@register.filter(name='average_rating_count')
def average_rating_count(value):
	try:
		rating = [each.rating for each in models.Review.objects.filter(hotel_id=value)]
		total_rating = 0
		for rate in rating:
			total_rating += rate
		avg_rating = round(total_rating / len(rating))
	except:
		avg_rating = 0
	return avg_rating

# start rating range display
@register.filter(name='range')
def filter_range(start, end):  
	return range(start, end)
import hashlib
from porzotokApp import models
import pandas as pd
from datetime import datetime
import pyotp


def PassWord(rawdata):
	Spass = hashlib.sha256(str(rawdata).encode("utf-8")).hexdigest()
	Mpass = hashlib.md5(str(Spass).encode("utf-8")).hexdigest()
	return Mpass

# save recent search history
def saveRecentSearchHistory(user_id, search_session_id, keyword):
	if user_id == '':
		new_user_id = None
		checkKeyword = models.RecentSearch.objects.filter(search_session_id=search_session_id, keyword=keyword)
		if(len(checkKeyword) == 0):

			recent_search = models.RecentSearch(
				user_id = new_user_id,
				search_session_id = search_session_id,
				keyword = keyword,
			)
			recent_search.save()
		else:
			checkKeyword.delete()
			recent_search = models.RecentSearch(
				user_id = new_user_id,
				search_session_id = search_session_id,
				keyword = keyword,
			)
			recent_search.save()
	else:
		try: 
			new_user_id = models.User.objects.get(user_id=user_id)
		except:
			new_user_id = None

		checkKeyword = models.RecentSearch.objects.filter(user_id=new_user_id, keyword=keyword)
		if(len(checkKeyword) == 0):

			recent_search = models.RecentSearch(
				user_id = new_user_id,
				search_session_id = search_session_id,
				keyword = keyword,
			)
			recent_search.save()
		else:
			checkKeyword.delete()
			recent_search = models.RecentSearch(
				user_id = new_user_id,
				search_session_id = search_session_id,
				keyword = keyword,
			)
			recent_search.save()

def CheckAvailable(new_start_date, new_end_date, room_id, cart = None):
	if cart == None:
		all_room_cart_details = models.RoomCartDetails.objects.filter(room_id__room_id = int(room_id), room_status="3")
	# else:
	# 	all_room_cart_details = models.RoomCartDetails.objects.filter(cart_id__cart_id = int(cart))
	total_days = []
	for each in all_room_cart_details:
		#old = pd.date_range(start=old_start_date,end=old_end_date)
		new = pd.date_range(start=each.check_in_date,end=each.check_out_date)
		total_days.append(new.values)
	new_range = pd.date_range(start=new_start_date, end=new_end_date)
	context = {}
	# print(new_range[0])
	# print(total_days)
	for each_i in total_days:
		for x in each_i:
			#print(f'{str(x).split("T")[0]} 00:00:00 and {[str(i) for i in new_range]}')
			if f'{str(x).split("T")[0]} 00:00:00' in [str(i) for i in new_range]:
				context['match'] = True
				context['msg'] = f"The {x} is Found"
				return context
			else:
				context = {}
				context['match'] = False
				context['msg'] = "Not Found"
	return context

# OTP
def OTP(userId):
	try:
		get_key = models.OTPmodels.objects.get(user_id__user_id=userId)
	except:
		get_key = models.OTPmodels.objects.create(otp_key=pyotp.random_base32(), user_id=models.User.objects.get(user_id=userId))
		get_key.save()
	otp_token = pyotp.TOTP(get_key.otp_key).now()
	return otp_token

def OTPverify(secret, code):
	otp_token = pyotp.TOTP(secret).verify(code)
	return otp_token
from porzotokApp.models import LoginActivity
from django.contrib.sessions.backends.db import SessionStore

def custom(session_id, username):
	li = LoginActivity(
			session_id = session_id,
			user = username,
		).save()
	return True
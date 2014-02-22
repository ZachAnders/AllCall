from flask import session, render_template
from functools import wraps

def is_valid_user(some_user, timestamp):
	"""Given a user, is this a valid user?"""
	if some_user == "admin":
		return True

def requires_session(some_route):
	@wraps(some_route)
	def protected(*args, **kwargs):
		if valid_session():
			return some_route(*args, **kwargs)
		else:
			return render_template("error.html")
	return protected

def valid_session():
	"""Returns True only if there is currently a valid username in the session"""
	#TODO: Add timestamp check
	if "username" in session:
		if is_valid_user(session["username"], 0):
			return True
	return False

def has_valid_credentials(user, passw):
	if user == "admin" and passw == "admin":
		return True
	return False

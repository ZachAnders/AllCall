from flask import Flask, render_template, request, session, redirect, url_for, flash
from AppAuth import has_valid_credentials, requires_session
from Powercode import DbSession
from PowercodeSchema import AccessPoint
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		user, pw = request.form["username"], request.form["password"]
		if has_valid_credentials(user, pw):
			#Set the username in the session. Apparently flask protects this from being tampered with
			session["username"] = user
			return redirect(url_for("allcall"))
		return render_template("login.html", error="Incorrect Username or Password! Please double check them and try again.")
	else:
		return render_template("login.html")

@requires_session
@app.route("/allcall")
def allcall():
	sess = DbSession()
	#aps = sess.get_APs()
#	aps = AccessPoint.get_all_equipment(sess.get_session())
#	for ap in aps:
	aps = sess.get_session().query(AccessPoint).all()
#		#Populate network location and address
#		ap.populate(sess.get_session())
	return render_template("allcall.html", access_points=aps, logged_in=True)

@app.route("/logout")
def logout():
	if "username" in session:
		del session["username"]
	flash("You have been logged out.")
	return redirect(url_for("login"))

app.secret_key = "?\xc1*\r\xa1\x89\xe6\xa1\xcc\xe7\x9ef\x97\x12\xd3Z)\x93\xd6u\x14y\x0b~Uw\x8a\x89k\xb5\xaejet\xe8\xb3L\xfc\xbez'\xe9\xd9^\xcb\x8fw\x1c\xcb\xab\xe0\xb0,\xc8\x8a\x86w\x8d\xf79\xdc;\x9c}"

if __name__ == "__main__":
	app.debug = True
	app.run()


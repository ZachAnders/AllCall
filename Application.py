import json, os
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

@app.route("/allcall")
@requires_session
def allcall():
	sess = DbSession()
	aps = sess.get_session().query(AccessPoint).all()
	sites = {}
	for ap in aps:
		nl_id = ap.equipment.equipment_ex.network_location.NetworkLocationID
		if nl_id not in sites:
			sites[nl_id] = []
		sites[nl_id].append(ap)

	default_order = sites.keys()
	default_order.sort(key=lambda x: sites[x][0].equipment.equipment_ex.network_location.Name)
	default_order = [(default_order[i], i%2) for i in range(len(default_order))]
	return render_template("allcall.html", sites=sites, site_order=default_order, logged_in=True, debug=app.debug)

@app.route("/select_aps", methods=['POST'])
@requires_session
def select_aps():
	aps = json.loads(request.form['selected_aps'])
	aps = [int(ap.replace("ap_",'')) for ap in aps]
	return str(aps)

@app.route("/logout")
def logout():
	if "username" in session:
		del session["username"]
	flash("You have been logged out.")
	return redirect(url_for("login"))

if __name__ == "__main__":
	app.secret_key = os.urandom(128)
	app.debug = True
	if app.debug:
		app.secret_key = 'U\xb3gP\x97\xd6\xd7\xe7\xce3<YO\xc4\x90\xfdp\xef4\xca\x13x\xd5\x83aq\x99rP/0Z'
	app.run()


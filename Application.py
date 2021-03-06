#!/usr/bin/env python
import json, os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from AppAuth import has_valid_credentials, requires_session
from DbSession import DbSession
from PowercodeSchema import AccessPoint, Equipment, Customer
app = Flask(__name__)

#Root, redirect to login
@app.route("/")
def hello():
	return render_template("login.html")

#Simple login page
@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		user, pw = request.form["username"], request.form["password"]
		if has_valid_credentials(user, pw):
			#Set the username in the session. Apparently flask protects this from being tampered with
			#via crypto sig
			session["username"] = user
			return redirect(url_for("allcall"))
		return render_template("login.html", error="Incorrect Username or Password! Please double check them and try again.")
	else:
		return render_template("login.html")

# Main page for selecting AlLCall APs
@app.route("/allcall")
@requires_session
def allcall():
	sess = DbSession().get_session()
	aps = sess.query(AccessPoint).all()
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

#Select APs, determines appropriate customer list
@app.route("/select_aps", methods=['POST'])
@requires_session
def select_aps():
	aps = json.loads(request.form['selected_aps'])
	message = request.form['selected_message']
	aps = [int(ap.replace("ap_", '')) for ap in aps]
	sess = DbSession().get_session()
	ap_equips = sess.query(Equipment).filter(Equipment.ID.in_(aps)).all()
	num_customers = sum([len(ap.get_children()) for ap in ap_equips])
	return render_template("customer_select.html", num_customers=num_customers, aps=ap_equips, message=message, logged_in=True, debug=app.debug)

@app.route("/exec_allcall", methods=['POST'])
@requires_session
def exec_allcall():
	sess = DbSession().get_session()
	message = request.form['selected_message']
	customers = json.loads(request.form['selected_custs'])
	customers = [int(customer.replace("cust_", '')) for customer in customers]
	customers = sess.query(Customer).filter(Customer.CustomerID.in_(customers)).all()
	
	phone_numbers = [customer.get_first_number() for customer in customers if customer.get_first_number()]

	def cust_iter():
		for number in phone_numbers:
			yield str(number)

	outs = "Message: %s, To call: <br>" % message
	print(outs + ",".join(cust_iter()))

	return render_template("completed.html", logged_in=True, debug=app.debug)

#Logout.
@app.route("/logout")
def logout():
	if "username" in session:
		del session["username"]
	flash("You have been logged out.")
	return redirect(url_for("login"))

if __name__ == "__main__":
	app.debug = True
	#This makes debugging a lot easier. Otherwise the current session gets invalidated every time flask restarts
	if app.debug:
		app.secret_key = 'U\xb3gP\x97\xd6\xd7\xe7\xce3<YO\xc4\x90\xfdp\xef4\xca\x13x\xd5\x83aq\x99rP/0Z'
	else:
		#Note to self: Figure out if this has any other repercussions.
		#Pros: crypto key can't get leaked from source
		#Cons: Restarting the web server invalidates old sessions. (Inconvenient?)
		app.secret_key = os.urandom(128)
	app.run()


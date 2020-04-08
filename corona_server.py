from flask import Flask, render_template, request, make_response, redirect, url_for, session
from utils import data_db, handle_customer as customer, graph
import datetime
import os

# TODO: (on country change -> javascript visible available dates -> get info through javascript with background
#  python api); design adminpanel (watch out for mobile design); design sign up page
#  for new user; fix server issues
#
#

server = Flask(__name__)
server.secret_key = 'G\xc1*_Ad\xb0EI\xc9\x108\x7f]\x07\x1f\xfb\x1a\xeb\x84\xb1\xd7\xbc;'

info_db_path = os.path.join("database", "corona_info.db")
customer_db_path = os.path.join("database", "customer.db")

data_db.setup(info_db_path)
customer.setup(customer_db_path)
graph.setup(info_db_path)


@server.route("/", methods=["POST", "GET"])
def index():
    username = session["username"] if "username" in session else None
    if "country" in request.args:
        country = request.args.get("country")
        requested_timestamp = request.args.get("date")
        if requested_timestamp is not None:
            requested_timestamp = int(requested_timestamp)
        update_timestamp, confirmed, deaths, reco = data_db.get_db_info(country, requested_timestamp)
        available_timestamps = data_db.get_available_timestamps(country)
        resp = make_response(
            render_template("display_info.html", country=country, confirmed=confirmed, deaths=deaths, reco=reco,
                            last_info_update=update_timestamp, datetime=datetime.datetime,
                            available_timestamps=available_timestamps, requested_timestamp=requested_timestamp,
                            username=username)
        )
        resp.set_cookie("country", country)
        return resp

    countries = data_db.beatify_country_list(data_db.get_countries())
    country = request.cookies.get("country")
    return render_template("index.html", countries=countries, country=country, username=username)


@server.route("/graphs")
def graphs():
    username = session["username"] if "username" in session else None
    countries = data_db.beatify_country_list(data_db.get_countries())
    if "country" in request.args:
        country = request.args["country"]
        graph.save_graph(country, path=f"static/img/graphs/{country}.png")
        return render_template("display_graph.html", username=username, country=country, countries=countries)

    return render_template("graphs.html", username=username, countries=countries)


@server.route("/login", methods=["GET", "POST"])
def login():
    if request.args.get("error") is None:
        return render_template("login.html", error=False)
    return render_template("login.html", error=True)


@server.route("/login/validate", methods=["POST"])
def validate_login():
    username = request.form.get("username")
    pwd = request.form.get("password")
    case = customer.login(username, pwd)
    if case:
        session["username"] = username
        if username == "admin":
            return redirect("/adminpage")
        return redirect("/")
    else:
        return redirect(url_for("login", error=True))


@server.route("/adminpage")
def adminpage():
    if "username" in session and session["username"] == "admin":
        return render_template("adminpage.html", username="admin")
    return redirect("/")


@server.route("/signup")
def signup():
    if request.args.get("error") is None:
        return render_template("signup.html", error=False)
    return render_template("signup.html", error=True)


@server.route("/signup/validate", methods=["POST"])
def validate_signup():
    username = request.form.get("username")
    pwd = request.form.get("password")
    name = request.form.get("name")
    if customer.user_exists(username):
        return redirect(url_for("signup", error=True))
    customer.signup(username, name, pwd)
    session["username"] = username
    return redirect("/")


@server.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@server.errorhandler(404)
def page_not_found(e):
    username = session["username"] if "username" in session else None
    return render_template("page_not_found.html", username=username)


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=80, debug=True, threaded=True)

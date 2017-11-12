"""I control everything."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, jsonify
# from flask_migrate import Migrate
from model import db, connect_to_db, User, Chart, Star


app = Flask(__name__)

app.debug = True

app.secret_key = "shhhhhhhhhhh!!! don't tell!"

#keep jinja from failing silently because of undefined variables
app.jinja_env.undefined = StrictUndefined

#make the database and migrations work
connect_to_db(app)
# migrate = Migrate(app, db)


@app.route("/")
def show_homepage():
    """Show the landing page"""

    return render_template("home.html")


@app.route("/register.json", methods=["POST"])
def do_registration():
    """Process registration"""

    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")

    #we shouldn't ever get to this route with an email that's taken, but check
    #just in case, and return an error if so
    user = User.query.filter(User.email == email).first()
    if user:
        return jsonify({"status": "email taken"})

    #if we get here, the email is new to us, so register a new user and return
    #a success status
    new_user = User(email=email, password=password,
                    firstname=first_name, lastname=last_name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "successfully registered"})



@app.route("/check-email.json", methods=["GET"])
def check_email():
    """Return true if email belongs to a registered user, false otherwise"""

    email = request.args.get("email")

    #look up email in database
    user = User.query.filter(User.email == email).first()

    #return a result
    if user:
        return jsonify({"email in database": True})
    else:
        return jsonify({"email in database": False})



@app.route("/login.json", methods=["POST"])
def do_login():
    """Process login"""

    email = request.form.get("email")
    password = request.form.get("password")

    #look up user in database
    user = User.query.filter(User.email == email).first()

    #if the user was found and their password is correct, log them in and
    #redirect them to their dashboard
    if user and user.password == password:
        session["user_id"] = user.user_id
        return jsonify({"status": "logged in"})
    #return an error status otherwise
    else:
        return jsonify({"status": "error"})




if __name__ == "__main__":
    app.run()

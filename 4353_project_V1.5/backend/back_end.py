from flask_sqlalchemy import SQLAlchemy #added
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #added
db = SQLAlchemy(app) #added

class User(db.Model): #added
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class FuelQuote(db.Model): #added
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gallons_requested = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    price_per_gallon = db.Column(db.Float, nullable=False)
    total_amount_due = db.Column(db.Float, nullable=False)

    user = db.relationship("User", backref=db.backref("fuel_quotes", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<FuelQuote {self.id}>"

    def __repr__(self):
        return '<User %r>' % self.username

@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"]) #added
def login():
    if request.method == "POST":
        session.permanent = True
        user_identifier = request.form["nm"]
        found_user = User.query.filter((User.username == user_identifier) | (User.email == user_identifier)).first()
        if found_user:
            session["user"] = found_user.username
            flash(f"Login Successful!")
            return redirect(url_for("user"))
        else:
            flash(f"Invalid credentials. Please try again.")
            return render_template("login.html")
    else:
        if "user" in session:
            flash(f"Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")
#This updated implementation uses SQLAlchemy's filter and first methods to query the database for a user 
# with the submitted username or email. If the user is found, they are logged in; otherwise, an error message is displayed.
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        session.permanent = True
        session["user"] = username
        flash(f"Sign Up Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"Already Logged In!")
            return redirect(url_for("user"))
        return render_template("register.html")
    
@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash(f"You are not logged in!")
        return redirect(url_for("login"))

    
@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/fquote", methods=["POST", "GET"]) #added
def fquote():
    if "user" in session:
        user = session["user"]
        found_user = User.query.filter_by(username=user).first()

        if request.method == "POST":
            gallons_requested = float(request.form["gallons_requested"])
            delivery_address = request.form["delivery_address"]
            delivery_date = datetime.strptime(request.form["delivery_date"], '%Y-%m-%d')
            price_per_gallon = 1.50  # Calculate price per gallon based on your pricing module
            total_amount_due = gallons_requested * price_per_gallon

            new_quote = FuelQuote(user_id=found_user.id, gallons_requested=gallons_requested,
                                  delivery_address=delivery_address, delivery_date=delivery_date,
                                  price_per_gallon=price_per_gallon, total_amount_due=total_amount_due)

            db.session.add(new_quote)
            db.session.commit()

            flash("Fuel quote created successfully!")
            return render_template("fquote.html")
        else:
            return render_template("fquote.html")
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


@app.route("/hquote", methods=["POST", "GET"]) #added
def hquote():
    if "user" in session:
        user = session["user"]
        found_user = User.query.filter_by(username=user).first()
        quotes = FuelQuote.query.filter_by(user_id=found_user.id).all()
        return render_template("hquote.html", quotes=quotes)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/view", methods=["POST", "GET"])
def view():
    return render_template("view.html")

@app.route("/delete", methods=["POST"]) #added
def delete():
    if "user" in session:
        user = session["user"]
        found_user = User.query.filter_by(username=user).first()
        if found_user:
            db.session.delete(found_user)
            db.session.commit()
            session.pop("user", None)
            flash(f"Your account has been deleted!", "info")
        else:
            flash(f"Error: Unable to delete your account.", "error")
    else:
        flash(f"You are not logged in!", "warning")
    return redirect(url_for("home"))
#    Check if the user is logged in.
#    If the user is logged in, delete their account from the database.
#   Remove their session data and log them out.
#   Redirect them to the home page with a flash message indicating that their account has been deleted.

if __name__ == "__main__":
    with app.app_context(): #added
        db.create_all() # added
    app.run(debug=True)

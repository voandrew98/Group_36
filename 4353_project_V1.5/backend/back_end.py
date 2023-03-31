from flask_sqlalchemy import SQLAlchemy #added
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #added
db = SQLAlchemy(app) #added

class User(db.Model): #added
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

#need to define secret key to USE session

@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash(f"Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")
    
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"] #nm data form
        session["user"] = user #session stores data
        flash(f"Sign Up Successful!")
        return redirect(url_for("user")) #submit button will redirect us to users name @app.route(usr)
    else: #if "get" request
        if "user" in session:
            flash(f"Already Logged In!")
            return redirect(url_for("user"))
        return render_template("register.html") ##this html creates a form 

@app.route("/user")
def user():
    if "user" in session: #check if user in session
        user = session["user"]
        return render_template("user.html",user = user)
    else:
        flash(f"You are not logged in!")
        return redirect(url_for("login"))

    
@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None) #remove user data
    return redirect(url_for("login"))

@app.route("/fquote", methods=["POST", "GET"])
def fquote():
    return render_template("fquote.html") ##this html creates a form 

@app.route("/hquote", methods=["POST", "GET"])
def hquote():
    return render_template("hquote.html")

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
    app.run(debug=True) #dont have to rerun server everytime we make change
    



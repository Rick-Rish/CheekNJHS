from flask import Flask, render_template, flash, redirect, request, url_for, session
import re
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = '2a421c841097eadac4554d06abdc6751'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cheeknjhs.db'
"""

"""
oauth = OAuth(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user (user_id):
   return User.query.get(int(user_id))
"""
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
""" # MAKE SURE THIS GETS BACK TO NORMAL
class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self): 
       return f"User('{self.username}', '{self.email}')"
    
    signups = db.relationship("Signup", backref="User", lazy=True)
    
class Event(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    signups = db.relationship("Signup", backref="Event", lazy=True)

class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))

all_events = [
    {
       "id": 1,
       "name" : "Induction Ceremony",
       "date" : "March 24, 2026",
       "time" : "3:00 to 8:00PM Slots",
       "description" : "Our NJHS Induction Ceremony welcomes all new 7th and 8th graders who have been invited to the NJHS Committee. They have accepted this opportunity, and have agreed to volunteer to make the community better. Come for this annual event, so you can be on stage, backstage, or simply set the event up!",
       "img" : "Screenshot 2026-02-08 at 20.38.53.png"
    },
]

@app.route("/")
def home():
    return render_template('index.html', title="Home", user=session.get('user'))

@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get('name', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    conpassword = request.form.get('con-password', '')

    if request.method == "POST":
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conpassword = request.form['con-password']
    
    errors = []

    if len(username) < 2 or len(username) > 20:
       errors.append("Username must be between 2-20 character")
    
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        errors.append("Invalid email format")
    
    if conpassword != password:
        errors.append("Retype your password.")

    if errors:
        for e in errors:
            flash(e, "danger")
        return render_template("logsign.html")
    else: 
     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
     user = User(username=username, email=email, password=hashed_password)
     db.session.add(user)
     db.session.commit()
     username = request.form['name']
     session['user'] = username
     return redirect(url_for("user"))
    
@app.route("/login", methods=["GET", "POST"])
def login():
 if request.method == "POST":
   user = request.form.get('name', '')
   email = request.form.get('email', '')
   password = request.form.get('password', '')
   rememberme = request.form.get('rememberme', '')

   errors = []
   if len(user) < 2 or len(user) > 20:
       errors.append("Username must be between 2-20 character")
    
   pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

   if not re.match(pattern, email):
        errors.append("Invalid email format")

   if request.method == "POST":
     username = request.form['name']
     rememberme = True if request.form.get('remember-me') == 'on' else False
     user = User.query.filter_by(email=email).first() 

   if user and bcrypt.check_password_hash(user.password, password):
    login_user(user, remember=rememberme)
    session['user'] = username
    return redirect(url_for("user"))
   else: 
     flash('Login Unsuccessful. Please check your name, email, and password and resubmit', 'danger')
 return render_template("logsign.html")
   
@app.route("/user")
def user():
   if "user" not in session:
     return render_template("logsign.html")
   
   upcoming = []
   current_user = User.query.filter_by(username=session["user"]).first()
   user_signups = Signup.query.filter_by(user_id=current_user.id).all()

   for signup in user_signups:
        event = Event.query.get(signup.event_id)
        if event:
            upcoming.append(event)
   return render_template("profile.html", username=session["user"], upcoming=upcoming, user=current_user)
"""
@app.route("/google_login")
def google_login():
    return google.authorize_redirect(url_for('callback', _external=True))

@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token, nonce=None)

    email = user_info['email']
    username = user_info.get('name', email.split("@")[0])

    user = User.query.filter_by(email=email).first()

    if not user:
     user = User(username=username, email=email, password='')
     db.session.add(user)
     db.session.commit()

    login_user(user)
    session['user'] = username
    flash("Logged in successfully with Google", "success")
    return redirect(url_for("user"))
""" # MAKE SURE THIS GOES BACK TO NORMAL
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/volunteer")
def volunteer():
 eventsdb = Event.query.all()
 with app.app_context():
    if Event.query.count() == 0:
        event = Event(
            name="Induction Ceremony",
            date="March 24, 2026",
            time="3:00 to 8:00PM Slots",
            description="Our NJHS Induction Ceremony welcomes all new members..."
        )
        db.session.add(event)
        db.session.commit()
 print(eventsdb)

 if 'user' not in session:
    flash("Please log in to access volunteering", "warning")
    return redirect(url_for("login"))
 return render_template("volunteering.html", all_events=eventsdb, user=session.get('user'))

@app.route("/signup_event/<int:event_id>", methods=["GET", "POST"]) 
def signup_event(event_id) :
   
   if 'user' not in session:
    flash("Please log in to access volunteering", "warning")
    return redirect(url_for("login"))

   if "upcoming_events" not in session:
    session["upcoming_events"] = []

   user = User.query.filter_by(username=session["user"]).first()
   signup = Signup(user_id=user.id, event_id=event_id)
   exsisting_signup = Signup.query.filter_by(user_id=user.id, event_id=event_id).first()

   if exsisting_signup:
      flash("You have already signed up for this event.", "info")

   else:
      session["upcoming_events"].append(event_id)
      session.modified = True
      db.session.add(signup)
      db.session.commit()
      flash("You signed up for the event!", "success")

   return redirect(url_for("volunteer"))

@app.route("/cancel_signup/<int:event_id>", methods=["GET", "POST"])
def cancel_signup(event_id):
   if "user" not in session: 
     return redirect(url_for("login"))

   user = User.query.filter_by(username=session["user"]).first()
   signup = Signup.query.filter_by(user_id=user.id, event_id=event_id).first()

   if signup: 
     db.session.delete(signup)
     db.session.commit()

   if "upcoming_events" in session and event_id in session["upcoming_events"]:
        session["upcoming_events"].remove(event_id)
        session.modified = True
        flash("You have sucessfully cancelled your signup. Please signup again if you are going to be there.")
        
   return redirect(url_for("user"))

@app.route("/aboutus")
def about_us():
    return render_template("aboutus.html")

@app.route("/hours")
def hours():
    return render_template("hours.html")

@app.route("/requirement")
def req():
    return render_template("requirements.html")

@app.route("/pictures")
def pictures():
    return render_template("pictures.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
app.run(host="0.0.0.0", port=5000, debug=True)

# if __name__ == "__main__":
 # app.run(debug=True)
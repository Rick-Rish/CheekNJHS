from flask import Flask, render_template, flash, redirect, request, url_for, session
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = '2a421c841097eadac4554d06abdc6751'

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
event_signups = {
   1: ["Rishon", "Random Dude", "Random Dude2"]
}
print(event_signups)

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
     username = request.form['name']
     session['user'] = username
     return redirect(url_for("user"))
    
@app.route("/login", methods=["GET", "POST"])
def login():
   user = request.form.get('name', '')
   email = request.form.get('email', '')
   password = request.form.get('password', '')

   errors = []
   if len(user) < 2 or len(user) > 20:
       errors.append("Username must be between 2-20 character")
    
   pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

   if not re.match(pattern, email):
        errors.append("Invalid email format")

   if request.method == "POST":
     username = request.form['name']
     session['user'] = username
     return redirect(url_for("user"))
   else: 
     return render_template("logsign.html")

@app.route("/user")
def user():
   if "user" not in session:
     return render_template("logsign.html")
   else:
       user = session["user"]
       upcoming_ids = session.get("upcoming_events", [])
       upcoming = [e for e in all_events if e["id"] in upcoming_ids]
       return render_template("profile.html", username=session["user"], upcoming=upcoming, user=user, event_signups = event_signups)
   
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/volunteer")
def volunteer():
 if 'user' not in session:
    flash("Please log in to access volunteering", "warning")
    return redirect(url_for("login"))
 
 return render_template("volunteering.html", all_events=all_events, event_signups = event_signups, user=session.get('user'))

@app.route("/signup_event/<int:event_id>", methods=["GET", "POST"]) 
def signup_event(event_id) :
   if 'user' not in session:
    flash("Please log in to access volunteering", "warning")
    return redirect(url_for("login"))
   
   if "upcoming_events" not in session:
    session["upcoming_events"] = []

    if event_id not in event_signups:
       event_signups(event_id) == []

   if event_id not in session["upcoming_events"]:
      session["upcoming_events"].append(event_id)
      session.modified = True
      flash("You signed up for the event!", "success")
   else:
      flash("You're already signed up for this event.", "info")

   return redirect(url_for("volunteer"))

@app.route("/aboutus")
def about_us():
    return render_template("aboutus.html")

@app.route("/hours")
def hours():
    return render_template("hours.html")

@app.route("/requirement")
def req():
    return render_template("requirements.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
 app.run(debug=True)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
   username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])

   email = StringField('Email', validators=[DataRequired(), Email()])

   password = PasswordField('Password', validators=[DataRequired()])

   confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

   submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
 name = StringField('Username', validators = [DataRequired()])
 email = StringField('Email', validators=[DataRequired(), Email()])

 password = PasswordField('Password', validators=[DataRequired()])
 remember = BooleanField('Remember Me')
 submit = SubmitField('Log In')
@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', title='Home Page')

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Validation
        if len(username) < 2 or len(username) > 20:
            flash("Username must be 2-20 characters long", "danger")
            return redirect(url_for("register"))
        if "@" not in email:
            flash("Invalid email address", "danger")
            return redirect(url_for("register"))

        flash("Registration successful!", "success")
        return redirect(url_for("home"))

    return render_template("logsign.html", title="Register")

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    print(email)
    print(password)

    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)

    @app.route("/login", methods=["GET", "POST"])
def login():
   username = request.form.get('name', '')
   email = request.form.get('email', '')

   from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///mydatabase.db', echo=True)
conn = engine.connect()
conn.execute(text("CREATE TABLE IF NOT EXSISTS people(name str, people int)"))
conn.commit()

from sqlalchemy.orm import Session
session = Session(engine)
session.execute(text('INSERT INTO people(name, age) VALUES("Mike", 30)'))
session.commit()

from app import db, login_manager

with app.app_context():
    event = Event(
        name="Something",
        date="March 24, 2026",
        time="3:00 to 8:00PM Slots",
        description="Our NJHS Induction Ceremony welcomes all new 7th and 8th graders..."
    )

    db.session.add(event)
    db.session.commit()


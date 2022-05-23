from flask import Flask, flash, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf.form import FlaskForm
from wtforms import StringField , PasswordField



app = Flask(__name__ , template_folder="templates" , static_folder="static")
app.secret_key = "this is password pls don't steal 4269"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sheet.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


##MODELS
class User(db.Model , UserMixin):

    _id =      db.Column( db.Integer , primary_key = True)
    username = db.Column(db.String(100) , unique= True , nullable = False)
    password = db.Column(db.String(1000)  , nullable = False)
    html_bio = db.Column(db.Text , nullable = True)


    def __init__(self, username : str , password : str , html_bio = None):
        self.username = username
        self.password = password
        self.html_bio = html_bio

    def __repr__(self):
        return self.username
        


####FORMS

class SignupForm(FlaskForm):
    
    username =  StringField("username")
    password =  PasswordField("password")



###VIEWS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup")
def signup():
    
    if request.method == "POST":
        username = request.form.get("username" , False)
        password = request.form.get("password" , False)
        if username:
            if username >= 100:
                flash("یوزرنیم باید کمتر از 100 کاراکتر باشد جناپ")
            else:
                pass

            
        else:
            flash("اقای محرتم یوزرنیم خالی نباشه وگرنه")

    
        if password:
            pass
    

    if request.method == "GET":
        form = SignupForm()
        return render_template("signup.html" , form=form)



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)




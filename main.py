from flask import Flask, flash, jsonify, render_template , request , redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin , login_user  , LoginManager , current_user
from flask_wtf.form import FlaskForm
from wtforms import StringField , PasswordField
from passlib.hash import sha256_crypt




app = Flask(__name__ , template_folder="templates" , static_folder="static")
app.secret_key = "this is password pls don't steal 4269"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sheet.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


##MODELS
class User(db.Model , UserMixin):

    _id         = db.Column( db.Integer , primary_key = True)
    username    = db.Column(db.String(100) , unique= True , nullable = False)
    password    = db.Column(db.String(1000)  , nullable = False)
    html_bio    = db.Column(db.Text , nullable = True)
    name        = db.Column(db.String(100) , nullable = True)
    last_name   = db.Column(db.String(100) , nullable = True)


    def __init__(self, username : str , password  , html_bio = None , name = None , last_name = None):
        self.username = username
        self.password = password
        self.html_bio = html_bio
        self.name = name
        self.last_name = last_name

    def __repr__(self):
        return self.username
    
    def get_id(self):
        return self._id


####FORMS

class SignupForm(FlaskForm):
    
    username =  StringField("username" )
    password =  PasswordField("password")
    name   = StringField("name")
    last_name = StringField("last_name")




@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(_id = user_id).first()

###VIEWS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup" , methods =["GET" , "POST"] )
def signup():
    
    if request.method == "POST":
        username = request.form.get("username" , False)
        password = request.form.get("password" , False)
        name = request.form.get("name" , False)
        last_name = request.form.get("last_name" , False)
        if username:
            if len(username) >= 100:
                flash("یوزرنیم باید کمتر از 100 کاراکتر باشد جناپ")
            else:
                if  User.query.filter_by(username=username).first() != None:
                    flash("یوزرنیم تکراری است اقای محترم")
                else:
                    if password == False:
                        password = ""
                    password = sha256_crypt.encrypt(password)
                    user = User(username=username , password=password , name=name , last_name=last_name)
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect("/")
        
        else:
            flash("اقای محرتم یوزرنیم خالی نباشه وگرنه")
        return redirect(url_for("signup"))


    if request.method == "GET":
        form = SignupForm()
        return render_template("signup.html" , form=form)



@app.route("/has_logged_in")
def has_logged_in():
    return jsonify({
        "is_authenticated" : current_user.is_authenticated
    })
    


@app.route("/validation123" , methods = ["POST"])
def validation_endpoint():
    print(request)
    



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)



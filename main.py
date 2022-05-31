from datetime import datetime
from flask import Flask, flash, jsonify, render_template , request , redirect, url_for , abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin , login_user  , LoginManager , current_user
from passlib.hash import sha256_crypt
from flask_wtf.csrf import CSRFProtect
import os
from flask import send_from_directory





app = Flask(__name__ , template_folder="templates" , static_folder="static")
app.secret_key = "this is password pls don't steal 4269"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sheet.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)
csrf.init_app(app)


##MODELS
class User(db.Model , UserMixin):

    _id         = db.Column( db.Integer , primary_key = True)
    username    = db.Column(db.String(100) , unique= True , nullable = False)
    slug        = db.Column(db.String(100))
    password    = db.Column(db.String(1000)  , nullable = False)
    html_bio    = db.Column(db.Text , nullable = True)
    name        = db.Column(db.String(100) , nullable = True)
    last_name   = db.Column(db.String(100) , nullable = True)
    date_joinde = db.Column(db.DateTime , default= datetime.utcnow)


    def __init__(self, username : str , password  , html_bio = None , name = None , last_name = None):
        self.username = username
        self.password = password
        self.html_bio = html_bio
        self.name = name
        self.last_name = last_name
        
        self.slug = slugify(username)

    def __repr__(self):
        return self.username
    
    def get_id(self):
        return self._id




@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(_id = user_id).first()


def slugify(text : str):

    valid = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="
    new = ""
    for i in text:
        if i in valid:
            new += i
    return new


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
            elif " " in username:
                flash ("آقای محترم اسپیس نذارید توی نام کاربری")
            
            else:

                for l in username:
                    if ord(l) < 33 or ord(l) > 126:
                        flash("یوزرنیم فارسی اقای محرتم")
                        break
                else:

                    if  User.query.filter_by(username=username).first() != None:
                        flash("یوزرنیم تکراری است اقای محترم")
                    else:
                        if not password == False and len(password) >= 8:
                            
                            password = sha256_crypt.encrypt(password)
                            user = User(username=username , password=password , name=name , last_name=last_name)
                            db.session.add(user)
                            db.session.commit()
                            login_user(user)
                            return redirect("/") 
                        
                        if password == False:
                            flash ("آقای محترم رمز خالی نباشه وگرنه")
                        
                        elif len(password) <= 8:
                            flash("آقای محترم رمزتون باید بیشتر از 8 کارکتر باشه")
        else:
            flash("اقای محرتم یوزرنیم خالی نباشه وگرنه")
                    
        return redirect(url_for("signup"))


    if request.method == "GET":
        return render_template("signup.html")


@app.route("/login" , methods= ["GET" , "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first() != None:
            user = User.query.filter_by(username = username).first()
            if sha256_crypt.verify(password, user.password):
                login_user(user)
                return redirect("/")
            flash("اقای محترم پسسورد شما دارای ایراد است")
            return redirect(url_for("login"))

        flash("یوزرنیم در پایگاه داده یافت نشد")
        return redirect(url_for("login"))
            



    if request.method == "GET":
        return render_template("login.html")



@app.route("/has_logged_in")
def has_logged_in():
    return jsonify({
        "is_authenticated" : current_user.is_authenticated
    })
    

@app.route("/validation123" , methods = ["POST"])
def validation_endpoint():
    username = request.form.get("username")
    password = request.form.get("password")
    error = ""
    password_error = ""
    if username == "":
        error = "اقای محترم چرا خالی؟"
    elif len(username) > 100:
        error = "زیادی بلنده اسکل"

    elif " " in username:
        error = "اسپیس نذارید. جدی می باشم.😤 "


    if User.query.filter_by(username = username).first() != None:
        error = "تکراریه اقای مترحم"

    if len(password) < 8:
        password_error = "اقای محترم چرا پسسورد کوتاه؟"

    return jsonify({
        "username_error" : error,
        "password_error" : password_error
    })



@app.route("/<int:pk>/<slug>")
def profile_view(pk , slug):
    if User.query.filter_by(_id = pk).filter_by(slug = slug).first() != None:
        user = User.query.filter_by(_id = pk).first()
        return render_template("profile.html" , user = user)
    abort(404)




#errors ??
@app.errorhandler(404)
def page_not_found (e):
    return render_template("404.html"), 404
    
    
@app.errorhandler(405)
def page_not_found (e):
    return render_template("405.html"), 405
    

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


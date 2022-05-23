from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


app = Flask(__name__ , template_folder="templates" , static_folder="static")
app.secret_key = "this is password pls don't steal 4269"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sheet.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

################
class User(db.Model , UserMixin):

    _id =      db.Column( db.Integer , primary_key = True)
    username = db.Column(db.String(100) , unique= True , nullable = False)
    password = db.Column(db.String(1000)  , nullable = False)
    html_bio = db.Column(db.String())



    def __init__(self, username : str , password : str):
        self.username = username
        self.password = password
        


#################


@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


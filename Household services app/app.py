from flask import Flask,render_template,request,redirect,url_for,session,flash
from extension import db
app = Flask(__name__)
from dotenv import load_dotenv
from models import *
from cust import cust
from professional import prof
from admin import adminbp
from api_controller import api_controller
import os
load_dotenv()

FLASK_DEBUG = os.getenv('FLASK_DEBUG')
app.config["FLASK_APP"] = os.getenv('FLASK_APP')
app.secret_key = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)
app.app_context().push()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        user1=request.form['username']
        passw=request.form['password']
        user = User.query.filter_by(email=user1).first()
        if user and user.check_password(passw):
            session['user']=user.email
            if user.role=='household':
                return redirect(url_for('cust.dashboard1'))
            elif user.role=='service_professional':
                return redirect(url_for('prof.dashboard'))
            else:
                return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid Credentials')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin/admin_layout.html')
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))
@app.route('/update_profile_pic',methods=['GET','POST'])
def update_profile_pic():
    if 'user' not in session:
        return redirect(url_for("login"))
    if request.method=='POST':
        file = request.files['image']
        user = User.query.filter_by(email=session['user']).first()
        user.profile_picture_name =  file.filename
        user.profile_picture = file.read()
        db.session.commit()
    return render_template('cust/profile.html',user=user)

app.register_blueprint(prof,url_prefix="/prof")
app.register_blueprint(cust,url_prefix="/cust")
app.register_blueprint(adminbp,url_prefix="/admin")
app.register_blueprint(api_controller,url_prefix="/api")

if __name__ =='__main__':
    app.run(debug=True)
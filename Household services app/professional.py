from flask import request,render_template,flash,redirect,url_for,Blueprint,session
import matplotlib.pyplot as plt
import base64
from models import*
from sqlalchemy import and_
prof = Blueprint("prof",__name__)

@prof.route('/profesional_register',methods=['GET','POST'])
def professional_register():
    service = Service.query.filter_by().all()
    if request.method=="POST":
        existing_username = User.query.filter_by(email=request.form['email']).first()
        if existing_username:
            flash('Email already exists','error')
            return render_template('professional/professionals_registration.html')
        password= request.form['password']
        email =request.form['email']
        role= "service_professional"
        profile_pic =request.files['image']
        new_user =User(email=email,role=role,profile_picture_name = profile_pic.filename,profile_picture = profile_pic.read())
        new_user.set_password(password=password)
        db.session.add(new_user)
        db.session.commit()
        
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        state = request.form['state']
        city = request.form['city']
        pincode = request.form['pincode']
        address = request.form['address']
        experience = request.form['experience']
        rate = request.form['rate']
        age  = request.form['age']
        about = request.form['about']
        document = request.files['document']
        ser_id = request.form.get('service','')
        new_professional = ServiceProfessional(first_name = fname,
                                               last_name = lname,
                                               phone_number = phone,
                                               state= state,
                                               about = about,
                                               city=city,
                                               pin_code = pincode,
                                               address = address,
                                               experience = experience,
                                               price = rate,
                                               age = age,
                                               document_name = document.filename,
                                               document = document.read(),
                                               ser_id = ser_id)
        db.session.add(new_professional)
        db.session.commit()
        flash('User registered successfully!')
        return redirect(url_for('professional_register'))
    return render_template('professional/professionals_registration.html',services = service)

@prof.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('login'))
    professional = ServiceProfessional.query.filter_by(s_id=user.u_id).first()
    
    if not professional:
        flash("Professional profile not found.")
        return redirect(url_for('prof.professional_register'))  # Or other redirect to register profile
    professional_id = professional.s_id

    if not professional_id:
        flash("Invalid professional data.")
        return redirect(url_for('login'))
    return render_template('professional/service_professional.html', professional=professional)
@prof.route('/update_request')
def update_request():
    request_id = request.form.get('request_id')
    action = request.form.get('action')
    service_request = Request.query.filter_by(req_id=request_id).first()
    if service_request:
        service_request.status = 'Accepted' if action == 'accept' else 'Rejected'
        db.session.commit()
        flash(f"Request {action.capitalize()} successfully!")
    else:
        flash("Request not found.")

    return redirect(url_for('prof.professional_home'))

@prof.route('/search', methods=['GET', 'POST'])
def search():
    results = None  
    if request.method == 'POST':
        search_option = request.form.get('search_option')
        date_str = request.form.get('date')
        address = request.form.get('address')
        pin_code = request.form.get('pincode')
        customer_name = request.form.get('customer_name')
        search_text = request.form.get('search_text')
        filters = []
        if search_option == 'date' and date_str:
            try:
                search_date = datetime.strptime(date_str, "%Y-%m-%d")
                filters.append(Request.date_req == search_date)
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.")
                return redirect(url_for('prof.search'))
        if search_option == 'address' and address:
            filters.append(ServiceProfessional.address.like(f"%{address}%"))
        if search_option == 'pincode' and pin_code:
            filters.append(ServiceProfessional.pin_code.like(f"%{pin_code}%"))
        if search_option == 'customer_name' and customer_name:
            filters.append(ServiceProfessional.first_name.like(f"%{customer_name}%"))
        if search_option == 'search_text' and search_text:
            filters.append(Request.comments.like(f"%{search_text}%"))

        query = db.session.query(Request).join(
            ServiceProfessional, ServiceProfessional.s_id == Request.s_id
        ).filter(*filters)
        results = query.all()

    return render_template('professional/search.html', results=results)

@prof.route('/update-profile-pic', methods=['POST'])
def update_profile_pic():
    if 'user' not in session:
        return redirect(url_for('login'))  
    user = User.query.filter_by(email=session['user']).first()
    professional = ServiceProfessional.query.filter_by(user_id=user.u_id).first()
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:  
            filename = file.filename
            professional.profile_image = file.read()  #
            db.session.commit()  
    return redirect(url_for('professional_profile'))

@prof.route('/professional-profile')
def professional_profile():
    if 'user' not in session:
        return redirect(url_for('login'))  
    
    user = User.query.filter_by(email=session['user']).first()
    professional = ServiceProfessional.query.filter_by(user_id=user.u_id).first()

    if professional:
        if professional.profile_image:
            user_image = base64.b64encode(professional.profile_image).decode('utf-8')
        else:
            user_image = None

        return render_template('professional/professional_profile.html', 
                               professional=professional, 
                               user=user,
                               user_image=user_image)
    
@prof.route('/professional_summary/<int:s_id>')
def professional_summary(s_id):
    professional = ServiceProfessional.query.get_or_404(s_id)
    requests = Request.query.filter_by(s_id=s_id).all()
    accepted_requests = len([r for r in requests if r.status == 'accepted'])
    rejected_requests = len([r for r in requests if r.status == 'rejected'])
    pending_requests = len([r for r in requests if r.status == 'pending'])
    rating = professional.rating  
    
    return render_template('professional/summary.html', 
                           professional=professional,
                           accepted_requests=accepted_requests,
                           rejected_requests=rejected_requests,
                           pending_requests=pending_requests,
                           rating=rating)
from flask import request,render_template,flash,redirect,url_for,Blueprint,session
import base64
from models import*
from sqlalchemy import and_,or_
cust = Blueprint("cust",__name__)

@cust.route('/cust_registration',methods=['GET','POST'])
def cust_register():
    if request.method=="POST":
        existing_username = User.query.filter_by(email=request.form['email']).first()
        if existing_username:
            flash('Email already exists','error')
            return render_template('cust/customer_registration.html')
        password= request.form['password']
        email =request.form['email']
        role= "household"
        profile_pic =request.files['image']
        new_user =User(email=email,role=role,profile_picture_name = profile_pic.filename,profile_picture=profile_pic.read())
        new_user.set_password(password=password)
        db.session.add(new_user)
        db.session.commit()
        
        first_name =request.form['first_name']
        last_name= request.form['last_name']
        phone_number =request.form['phone']
        state= request.form['state']
        city =request.form['city']
        pin_code =request.form['pincode']
        address= request.form['address'] 
        new_household = Household(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            state=state,
            city=city,
            pin_code=pin_code,
            address=address
            )     
        db.session.add(new_household)
        db.session.commit()
        flash('User registered successfully!')
        return redirect(url_for('cust.cust_register'))
    return render_template('cust/customer_registration.html')

@cust.route('/cust_dashboard')
def dashboard1():
    if 'user' not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(email=session['user']).first()
    household = Household.query.filter_by(h_id = user.u_id).first()
    services = Service.query.all()
    return render_template('cust/cust_dashboard.html',customer_name=household.first_name,services = services)

@cust.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(email=session['user']).first()
    household = Household.query.filter_by(h_id = user.u_id).first()
    if user.profile_picture:
        user_image = base64.b64encode(user.profile_picture).decode('utf-8')
    else:
        user_image =None
    return render_template('cust/profile.html',household=household,user_image=user_image,user=user)


@cust.route('/best_deals/<int:service_id>')
def best_deals(service_id):
    service = Service.query.get_or_404(service_id)
    
    professionals = (ServiceProfessional.query
                     .filter_by(service_id=service_id)
                     .order_by(ServiceProfessional.rating.desc(), ServiceProfessional.price.asc())
                     .all())
    
    return render_template(
        'cust/best_deals.html',
        service=service,
        professionals=professionals
    )
    
@cust.route('/book/<int:professional_id>', methods=['POST'])
def book_service(professional_id):
    if 'user' not in session:
        flash("You need to log in to book a service.", "danger")
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['user']).first()
    professional = ServiceProfessional.query.get_or_404(professional_id)
    service_request = Request(
        customer_id=user.u_id,  
        service_id=professional.service_id,
        professional_id=professional_id,
        status="Pending",
        date_req=db.func.now()  
    )
    db.session.add(service_request)
    db.session.commit()

    flash(f"Service booked with {professional.first_name} successfully!", "success")
    return redirect(url_for('custbp.dashboard')) 
  
@cust.route('/close_service/<int:request_id>', methods=['GET', 'POST'])
def close_service(request_id):
    if 'user' not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(email=session['user']).first()

    request = Request.query.filter_by(req_id=request_id, s_id=user.u_id).first()
    if not request:
        flash("Request not found or access denied.", "error")
        return redirect(url_for("cust.dashboard"))

    if request.method == "POST":
        rating = int(request.form.get("rating"))
        remarks = request.form.get("remarks")
        request.status = "closed"
        request.rating = rating
        request.remarks = remarks

        if request.professional:
            professional = request.professional
            all_ratings = [req.rating for req in professional.requests if req.rating is not None]
            if all_ratings:
                professional.rating = sum(all_ratings) / len(all_ratings)

        db.session.commit()

        flash("Service closed and rating submitted successfully.", "success")
        return redirect(url_for("cust.dashboard"))

    return render_template("cust/close_service.html", service=request.service, request=request)

@cust.route('/search', methods=['GET', 'POST'])
def search():
    if 'user' not in session:
        return redirect(url_for("login"))

    category = request.args.get('category')
    query = request.args.get('query', '')

    results = []

    if category == 'service':
        services = Service.query.filter(Service.name.ilike(f"%{query}%")).all()
        for service in services:
            professionals = service.professionals
            results.extend(professionals)
    elif category == 'professional':
        results = ServiceProfessional.query.filter(
            ServiceProfessional.first_name.ilike(f"%{query}%") |
            ServiceProfessional.last_name.ilike(f"%{query}%") |
            ServiceProfessional.city.ilike(f"%{query}%")
        ).all()

    return render_template('cust/search.html', results=results)

@cust.route('/customer-summary')
def customer_summary():
    if 'user' not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(email=session['user']).first()
    accepted_requests = Request.query.filter_by(status='accepted', h_id=user.u_id).count()
    rejected_requests = Request.query.filter_by(status='rejected', h_id=user.u_id).count()
    pending_requests = Request.query.filter_by(status='pending', h_id=user.u_id).count()
    return render_template('cust/summary.html',
                           accepted_requests=accepted_requests,
                           rejected_requests=rejected_requests,
                           pending_requests=pending_requests)

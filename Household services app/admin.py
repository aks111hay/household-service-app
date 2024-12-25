from flask import request,render_template,flash,redirect,url_for,Blueprint,session
import matplotlib.pyplot as plt
import base64
from models import*
from sqlalchemy import and_
adminbp = Blueprint("adminbp",__name__)

@adminbp.route('/dashboard')
def dashboard():
    return render_template('admin/admin_layout.html')

@adminbp.route('/search', methods=['POST'])
def search():
    search_category = request.form.get('search_category')
    search_text = request.form.get('search_text')
    results = []
    if search_category == 'services':
        results = Service.query.filter(Service.name.ilike(f"%{search_text}%")).all()
    elif search_category == 'customers':
        results = Household.query.join(User, User.u_id == Household.h_id).filter(
            (Household.first_name.ilike(f"%{search_text}%")) | 
            (Household.last_name.ilike(f"%{search_text}%"))
        ).all()
    elif search_category == 'professionals':
        results = ServiceProfessional.query.filter(
            (ServiceProfessional.first_name.ilike(f"%{search_text}%")) | 
            (ServiceProfessional.last_name.ilike(f"%{search_text}%"))
        ).all()

    return render_template('admin_search.html', results=results, search_text=search_text, search_category=search_category)
@adminbp.route('/manageservices',methods=['GET'])
def manageservices():
    services = Service.query.all()
    professionals = ServiceProfessional.query.all()
    requests = Request.query.all()
    return render_template('admin/manage.html', services=services, professionals=professionals, requests=requests)

@adminbp.route('/new_service')
def new_service():
    return render_template('admin/new_service.html')

@adminbp.route('/add_new_service',methods=['GET','POST'])
def add_new_service():
    if request.method=='POST':
        name = request.form['name']
        desc = request.form['desc']
        base_price = request.form['price']
        
        service = Service(name=name,desc = desc,base_price=base_price)
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('adminbp.new_service'))

@adminbp.route('/admin/edit-service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        service.name = request.form.get('service_name')
        service.description = request.form.get('description')
        service.base_price = request.form.get('base_price')
        db.session.commit()
        return redirect('admin/dashboard')  
    return render_template('edit_service.html', service=service)

@adminbp.route('/admin/delete-service/<int:service_id>', methods=['GET', 'POST'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        db.session.delete(service)
        db.session.commit()
        return redirect('/admin-dashboard')  
    return render_template('delete_service_confirm.html', service=service)

@adminbp.route('/admin/delete-user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)  
    if user.role == 'household':
        household = Household.query.filter_by(h_id=user.u_id).first()
        if household:
            requests = Request.query.filter((Request.s_id == user.u_id) | (Request.c_id == user.u_id)).all()
            for request in requests:
                db.session.delete(request)
            db.session.delete(household)
            db.session.commit()
    elif user.role == 'service_professional':
        service_professional = ServiceProfessional.query.filter_by(s_id=user.u_id).first()
        if service_professional:
            requests = Request.query.filter(Request.s_id == user.u_id).all()
            for request in requests:
                db.session.delete(request)
            db.session.delete(service_professional)
            db.session.commit()
    db.session.delete(user)
    db.session.commit()
    flash('User and associated data have been deleted successfully.', 'success')
    return redirect(url_for('adminbp.admin_dashboard'))

@adminbp.route('/professional-detail/<int:id>')
def detail(id):
    user = User.query.filter_by(u_id=id).first()
    professional = ServiceProfessional.query.filter_by(s_id=user.u_id).first()
    if professional.profile_picture:
        user_image = base64.b64encode(professional.document).decode('utf-8')
    else:
        user_image = None
    return render_template('admin/professional_detail.html', professional=professional, user_image=user_image, user=user) 
@adminbp.route('/service-request-details/<int:req_id>', methods=['GET'])
def service_request_details(req_id):
    service_request = Request.query.filter_by(req_id=req_id).first()
    
    if not service_request:
        return "Request not found", 404
    
    service = service_request.service
    customer = Household.query.filter_by(h_id=service_request.h_id).first()
    professional = service.professional if service.professional else None

    return render_template(
        'service_details.html', 
        request=service_request,
        service=service,
        customer=customer,
        professional=professional
    )    
@adminbp.route('/summary')
def summary():
    # Query the data you need, for example:
    
    # Get the number of requests with different statuses (Accepted, Rejected, Pending)
    accepted_requests = db.session.query(Request).filter(Request.status == 'Accepted').count()
    rejected_requests = db.session.query(Request).filter(Request.status == 'Rejected').count()
    pending_requests = db.session.query(Request).filter(Request.status == 'Pending').count()

    # Get the number of ratings for customers
    customer_ratings = [
        db.session.query(Request).filter(Request.rating == 1).count(),
        db.session.query(Request).filter(Request.rating == 2).count(),
        db.session.query(Request).filter(Request.rating == 3).count(),
        db.session.query(Request).filter(Request.rating == 4).count(),
        db.session.query(Request).filter(Request.rating == 5).count()
    ]
    
    # Pass the data to the template
    return render_template('admin/summary.html', 
                           accepted_requests=accepted_requests, 
                           rejected_requests=rejected_requests,
                           pending_requests=pending_requests,
                           customer_ratings=customer_ratings)
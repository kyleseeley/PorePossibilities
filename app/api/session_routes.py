from flask import Blueprint, request
from app.forms import SignUpForm, AppointmentForm
from flask_login import login_required, current_user
from app.models import User, Appointment, Company, Employee, Cart, db
from .auth_routes import validation_errors_to_error_messages
from datetime import datetime


session_routes = Blueprint('current', __name__)


@session_routes.route('')
@login_required
def get_current_user():
    if current_user.is_authenticated:
        if isinstance(current_user, User):
            return current_user.to_dict()
        elif isinstance(current_user, Employee):
            return current_user.to_dict()
    else:
        return {'error': 'User not found'}, 404


@session_routes.route("/reviews")
@login_required
def get_current_user_reviews():
    user = User.query.get(current_user.id)
    if user:
        return user.get_reviews()
    else:
        return {'error': 'User not found'}, 404


@session_routes.route('/cart')
@login_required
def get_current_user_cart():
    user = User.query.get(current_user.id)
    if user:
        return user.get_cart()
    else:
        return {'error': 'User has no cart'}, 404


@session_routes.route('/appointments')
@login_required
def get_current_user_appointments():
    user = User.query.get(current_user.id)
    if user:
        return user.get_appointments()
    else:
        return {'error': 'User not found'}, 404


@session_routes.route('/user', methods=['PUT'])
@login_required
def updateUserInfo():
    user = User.query.get(current_user.id)

    form = SignUpForm(obj=user)
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user.firstname = form.data['firstname']
        user.lastname = form.data['lastname']
        user.email = form.data['email']
        user.phone = form.data['phone']
        user.username = form.data['username']
        user.address = form.data['address']
        user.city = form.data['city']
        user.state = form.data['state']
        user.password = form.data['password']
        db.session.commit()
        return user.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@session_routes.route('/user', methods=['DELETE'])
@login_required
def deleteUser():
    user = User.query.get(current_user.id)
    if not user:
        return {'error': 'User not found'}, 404
    db.session.delete(user)
    db.session.commit()
    return {'message': 'Deleted successfully'}


@session_routes.route('<int:companyId>/appointments', methods=['POST'])
@login_required
def create_new_appointment(companyId):
    user = User.query.get(current_user.id)
    if not user:
        return {'error': 'User not found'}, 404

    company = Company.query.get(companyId)
    if not company:
        return {'error': 'Company does not exist'}, 404

    if not isinstance(current_user, User):
        return {'error': 'Only users can create appointments'}, 403

    form = AppointmentForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        data = form.data

        cart_services = current_user.cart.services if current_user.cart else []

        if not cart_services:
            return {'error': 'Cart is empty. Please add services to the cart before creating an appointment.'}, 400

        new_appointment = Appointment(
            userId=user.id,
            employeeId=data['employeeId'],
            companyId=companyId,
            appointmentDate=data['appointmentDate'],
            appointmentTime=data['appointmentTime'],
        )
        new_appointment.services = cart_services

        db.session.add(new_appointment)
        db.session.commit()
        return new_appointment.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401

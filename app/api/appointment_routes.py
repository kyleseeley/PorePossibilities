from flask import Blueprint, jsonify, request
from app.models import Appointment, Staff, User, Cart, Company, Service, db
from app.forms import CompanyForm, ReviewForm, ServiceForm, AppointmentForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


appointment_routes = Blueprint('appointments', __name__)


@appointment_routes.route('/')
@login_required
def all_appointments():
    appointments = Appointment.query.all()
    return {'appointments': [appointment.to_dict() for appointment in appointments]}


@appointment_routes.route('/<int:appointmentId>')
@login_required
def get_one_appointment(appointmentId):
    appointment = Appointment.query.filter(
        Appointment.id == appointmentId).first()
    if not appointment:
        return {'error': 'Company not found'}, 404

    return appointment.to_dict()


@appointment_routes.route('/<int:userId')
@login_required
def get_user_appointments(userId):
    user = User.query.get(userId)

    if not user:
        return {'error': 'User not found'}

    appointments = Appointment.query.filter(Appointment.userId == userId).all()

    return {'user_appointments': [appointment.to_dict() for appointment in appointments]}


@appointment_routes.route('/<int:staffId')
@login_required
def get_staff_appointments(staffId):
    staff = Staff.query.get(staffId)

    if not staff:
        return {'error': 'Staff not found'}

    appointments = Appointment.query.filter(
        Appointment.staffId == staffId).all()

    return {'staff_appointments': [appointment.to_dict() for appointment in appointments]}


@appointment_routes.route('/', methods=['POST'])
@login_required
def create_new_appointment():
    form = AppointmentForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form. validate_on_submit():
        data = form.data

        if current_user.id != data['userId']:
            return {'error': 'You are not authorized to create an appointment for this user'}, 403

        new_appointment = Appointment(
            userId=data['userId'],
            serviceId=data['serviceId'],
            staffId=data['staffId'],
            appointmentDate=data['appointmentDate'],
            appointmentTime=data['appointmentTime'],
            status=data['status']
        )

        db.session.add(new_appointment)
        db.session.commit()
        return new_appointment.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401

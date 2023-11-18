from flask import Blueprint, jsonify, request
from app.models import Appointment, Employee, User, db
from app.forms import AppointmentForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages
from datetime import datetime


appointment_routes = Blueprint('appointments', __name__)


@appointment_routes.route('')
@login_required
def all_appointments():
    appointments = Appointment.query.all()
    if not appointments:
        return {'error': 'No appointments found'}, 404
    
    return {'appointments': [appointment.to_dict() for appointment in appointments]}

@appointment_routes.route('/<int:appointmentId>')
@login_required
def get_one_appointment(appointmentId):
    appointment = Appointment.query.filter(
        Appointment.id == appointmentId).first()
    if not appointment:
        return {'error': 'Appointment not found'}, 404

    return appointment.to_dict()


@appointment_routes.route('/', methods=['POST'])
@login_required
def create_appointment():
    form = AppointmentForm()

    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        data = form.data
        new_appointment = Appointment(
            userId=data['userId'],
            companyId=data['companyId'],
            employeeId=data['employeeId'],
            appointmentDate=data['appointmentDate'],
            appointmentTime=datetime.strptime(data['appointmentTime'], '%I:%M %p').time()
        )

        db.session.add(new_appointment)
        db.session.commit()

        return new_appointment.to_dict(), 201
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@appointment_routes.route('/<int:appointmentId>', methods=['PUT'])
@login_required
def update_appointment(appointmentId):
    appointment = Appointment.query.get(appointmentId)
    if not appointment:
        return {'error': 'Appointment not found'}

    form = AppointmentForm(obj=appointment)
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        data = form.data
        appointment.userId = data.get('userId', appointment.userId)
        appointment.companyId = data.get('companyId', appointment.companyId)
        appointment.employeeId = data.get('employeeId', appointment.employeeId)
        appointment.appointmentDate = data.get(
            'appointmentDate', appointment.appointmentDate)
        appointment.appointmentTime = datetime.strptime(
            data.get('appointmentTime', appointment.appointmentTime.strftime('%I:%M %p')), "%I:%M %p").time()

        db.session.commit()

        return appointment.to_dict()
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@appointment_routes.route("/<int:appointmentId>", methods=['DELETE'])
@login_required
def delete_appointment(appointmentId):
    appointment = Appointment.query.filter(
        Appointment.id == appointmentId).first()
    if not appointment:
        return {'error': 'Appointment not found'}, 404
    if appointment.userId != current_user.id:
        return {'error': 'Unauthorized'}, 403
    db.session.delete(appointment)
    db.session.commit()
    return {'message': 'Appointment successfully deleted'}

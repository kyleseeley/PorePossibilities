from flask import Blueprint, jsonify, request
from app.models import Appointment, Employee, User, db
from app.forms import AppointmentForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


appointment_routes = Blueprint('appointments', __name__)


@appointment_routes.route('/<int:appointmentId>')
@login_required
def get_one_appointment(appointmentId):
    appointment = Appointment.query.filter(
        Appointment.id == appointmentId).first()
    if not appointment:
        return {'error': 'Appointment not found'}, 404

    return appointment.to_dict()


@appointment_routes.route('/<int:appointmentId>', methods=['PUT'])
@login_required
def update_appointment(appointmentId):
    appointment = Appointment.query.filter(
        Appointment.id == appointmentId).first()
    if not appointment:
        return {'error': 'Appointment not found'}

    form = AppointmentForm(obj=appointment)
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        data = form.data
        appointment.userId = data['userId']
        appointment.serviceId = data['serviceId']
        appointment.employeeId = data['employeeId']
        appointment.appointmentDate = data['appointmentDate']
        appointment.appointmentTime = data['appointmentTime']

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

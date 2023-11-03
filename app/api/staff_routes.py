from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.models import Staff, Appointment, db
from app.forms import StaffForm
from .auth_routes import validation_errors_to_error_messages

staff_routes = Blueprint('staffs', __name__)


@staff_routes.route('/')
def all_staff():
    staffs = Staff.query.all()
    if not staffs:
        return {'error': 'No staff members found'}
    return {'staffs': [staff.to_dict() for staff in staffs]}


@staff_routes.route('/<int:staffId>')
@login_required
def get_one_staff_member(staffId):
    staff = Staff.query.get(staffId)
    if not staff:
        return {'error': 'Staff member does not exist'}
    return staff.to_dict()


@staff_routes.route('/<int:staffId>/appointments')
@login_required
def get_appointments_by_staff_member(staffId):
    staff = Staff.query.get(staffId)
    if not staff:
        return {'error': 'Staff member not found'}
    appointments = Appointment.query.filter(
        Appointment.staffId == staffId).all()
    if not appointments:
        return {'error': 'Staff member does not have appointments'}
    
    return {'staff_appointments': [appointment.to_dict() for appointment in appointments]}


@staff_routes.route('/', methods=['POST'])
@login_required
def create_staff():
    if not current_user.is_owner:
        return {'error': 'Only the owner can create a new staff member'}, 403

    form = StaffForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        new_staff = Staff(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            authorized=data['authorized'],
            availability=data['availability'],
            password=data['password'],
        )

        db.session.add(new_staff)
        db.session.commit()
        return new_staff.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401
    

@staff_routes.route('/', methods=['PUT'])
@login_required
def edit_staff(staffId):
    staff = Staff.query.filter(Staff.id == staffId).first()
    if not staff:
        return {'error': 'Staff member does not exist'}
    if not current_user.is_owner:
        return {'error': 'Only the owner can edit a staff member'}, 403

    form = StaffForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        data.firstname=data['firstname'],
        data.lastname=data['lastname'],
        data.email=data['email'],
        data.authorized=data['authorized'],
        data.availability=data['availability'],
        data.password=data['password'],

        db.session.commit()
        return staff.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401
    

@staff_routes.route('/<int:staffId>', methods=['DELETE'])
@login_required
def delete_staff(staffId):
    staff = Staff.query.filter(Staff.id == staffId).first()
    if not staff:
        return {'error': 'Staff member not found'}, 404
    if not current_user.is_owner:
        return {'error': 'Only the owner can delete a staff member'}, 403

    db.session.delete(staff)
    return {'message': 'Staff member successfully deleted'}

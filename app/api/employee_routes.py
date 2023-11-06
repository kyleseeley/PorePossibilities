from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.models import Employee, Appointment, db
from app.forms import EmployeeForm
from .auth_routes import validation_errors_to_error_messages
from datetime import datetime

employee_routes = Blueprint('employees', __name__)


@employee_routes.route('')
def all_employees():
    employees = Employee.query.all()
    if not employees:
        return {'error': 'No employees found'}, 404
    return {'employees': [employee.to_dict() for employee in employees]}


@employee_routes.route('/<int:employeeId>')
@login_required
def get_one_employee(employeeId):
    employee = Employee.query.get(employeeId)
    if not employee:
        return {'error': 'Employee does not exist'}
    return employee.to_dict()


@employee_routes.route('/<int:employeeId>/appointments')
@login_required
def get_appointments_by_employee(employeeId):
    employee = Employee.query.get(employeeId)
    if not employee:
        return {'error': 'Employee not found'}
    appointments = Appointment.query.filter(
        Appointment.id == employeeId).all()
    if not appointments:
        return {'error': 'Employee does not have appointments'}

    return {'employee_appointments': [appointment.to_dict() for appointment in appointments]}


@employee_routes.route('', methods=['POST'])
@login_required
def create_employee():
    if not current_user.is_owner:
        return {'error': 'Only the owner can create a new employee'}, 403

    form = EmployeeForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data

        new_employee = Employee(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            authorized=data['authorized'],
            monday_start=datetime.strptime(
                data['monday_start'], '%I:%M %p').time() if data['monday_start'] else None,
            monday_end=datetime.strptime(
                data['monday_end'], '%I:%M %p').time() if data['monday_end'] else None,
            tuesday_start=datetime.strptime(
                data['tuesday_start'], '%I:%M %p').time() if data['tuesday_start'] else None,
            tuesday_end=datetime.strptime(
                data['tuesday_end'], '%I:%M %p').time() if data['tuesday_end'] else None,
            wednesday_start=datetime.strptime(
                data['wednesday_start'], '%I:%M %p').time() if data['wednesday_start'] else None,
            wednesday_end=datetime.strptime(
                data['wednesday_end'], '%I:%M %p').time() if data['wednesday_end'] else None,
            thursday_start=datetime.strptime(
                data['thursday_start'], '%I:%M %p').time() if data['thursday_start'] else None,
            thursday_end=datetime.strptime(
                data['thursday_end'], '%I:%M %p').time() if data['thursday_end'] else None,
            friday_start=datetime.strptime(
                data['friday_start'], '%I:%M %p').time() if data['friday_start'] else None,
            friday_end=datetime.strptime(
                data['friday_end'], '%I:%M %p').time() if data['friday_end'] else None,
            saturday_start=datetime.strptime(
                data['saturday_start'], '%I:%M %p').time() if data['saturday_start'] else None,
            saturday_end=datetime.strptime(
                data['saturday_end'], '%I:%M %p').time() if data['saturday_end'] else None,
            sunday_start=datetime.strptime(
                data['sunday_start'], '%I:%M %p').time() if data['sunday_start'] else None,
            sunday_end=datetime.strptime(
                data['sunday_end'], '%I:%M %p').time() if data['sunday_end'] else None,
            password=data['password'],
        )

        db.session.add(new_employee)
        db.session.commit()
        return new_employee.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@employee_routes.route('/<int:employeeId>', methods=['PUT'])
@login_required
def edit_employee(employeeId):
    employee = Employee.query.filter(Employee.id == employeeId).first()
    if not employee:
        return {'error': 'Employee does not exist'}
    if not current_user.is_owner:
        return {'error': 'Only the owner can edit an employee'}, 403

    form = EmployeeForm(obj=employee)
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        data.firstname = data['firstname'],
        data.lastname = data['lastname'],
        data.email = data['email'],
        data.authorized = data['authorized'],
        employee.monday_start = datetime.strptime(
            data['monday_start'], '%I:%M %p').time() if data['monday_start'] else None
        employee.monday_end = datetime.strptime(
            data['monday_end'], '%I:%M %p').time() if data['monday_end'] else None
        employee.tuesday_start = datetime.strptime(
            data['tuesday_start'], '%I:%M %p').time() if data['tuesday_start'] else None
        employee.tuesday_end = datetime.strptime(
            data['tuesday_end'], '%I:%M %p').time() if data['tuesday_end'] else None
        employee.wednesday_start = datetime.strptime(
            data['wednesday_start'], '%I:%M %p').time() if data['wednesday_start'] else None
        employee.wednesday_end = datetime.strptime(
            data['wednesday_end'], '%I:%M %p').time() if data['wednesday_end'] else None
        employee.thursday_start = datetime.strptime(
            data['thursday_start'], '%I:%M %p').time() if data['thursday_start'] else None
        employee.thursday_end = datetime.strptime(
            data['thursday_end'], '%I:%M %p').time() if data['thursday_end'] else None
        employee.friday_start = datetime.strptime(
            data['friday_start'], '%I:%M %p').time() if data['friday_start'] else None
        employee.friday_end = datetime.strptime(
            data['friday_end'], '%I:%M %p').time() if data['friday_end'] else None
        employee.saturday_start = datetime.strptime(
            data['saturday_start'], '%I:%M %p').time() if data['saturday_start'] else None
        employee.saturday_end = datetime.strptime(
            data['saturday_end'], '%I:%M %p').time() if data['saturday_end'] else None
        employee.sunday_start = datetime.strptime(
            data['sunday_start'], '%I:%M %p').time() if data['sunday_start'] else None
        employee.sunday_end = datetime.strptime(
            data['sunday_end'], '%I:%M %p').time() if data['sunday_end'] else None
        data.password = data['password'],

        db.session.commit()
        return employee.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@employee_routes.route('/<int:employeeId>', methods=['DELETE'])
@login_required
def delete_employee(employeeId):
    employee = Employee.query.filter(Employee.id == employeeId).first()
    if not employee:
        return {'error': 'Employee not found'}, 404
    if not current_user.is_owner:
        return {'error': 'Only the owner can delete an employee'}, 403

    db.session.delete(employee)
    db.session.commit()
    return {'message': 'Employee successfully deleted'}

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.models import Employee, Appointment, db
from app.forms import EmployeeForm
from .auth_routes import validation_errors_to_error_messages

employee_routes = Blueprint('employees', __name__)


@employee_routes.route('/')
def all_employees():
    employees = Employee.query.all()
    if not employees:
        return {'error': 'No employees found'}
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


@employee_routes.route('/', methods=['POST'])
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
            availability=data['availability'],
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

    form = EmployeeForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        data.firstname = data['firstname'],
        data.lastname = data['lastname'],
        data.email = data['email'],
        data.authorized = data['authorized'],
        data.availability = data['availability'],
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
    return {'message': 'Employee successfully deleted'}

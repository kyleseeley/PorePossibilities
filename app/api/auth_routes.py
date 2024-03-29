from flask import Blueprint, jsonify, session, request
from app.models import User, Employee, db
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required

auth_routes = Blueprint('auth', __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


# @auth_routes.route('')
# def authenticate():
#     print("Current user in authenticate:", current_user.to_dict())
#     if current_user.is_authenticated:
#         if isinstance(current_user, User):
#             return current_user.to_dict()
#         elif isinstance(current_user, Employee):
#             return current_user.to_dict()
#     return {'errors': ['Unauthorized']}, 403
@auth_routes.route('')
def authenticate():
    print("Current user in authenticate:", current_user.to_dict())
    if current_user.is_authenticated:
        user_type = session.get('user_type')
        if user_type == 'user':
            return {'user': current_user.to_dict(), 'user_type': 'user'}
        elif user_type == 'employee':
            return {'employee': current_user.to_dict(), 'user_type': 'employee'}
    return {'errors': ['Unauthorized']}, 403


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data['email']).first()
        employee = Employee.query.filter(
            Employee.email == form.data['email']).first()

        if user:
            session['user_type'] = 'user'
            login_user(user)
            return {'user': user.to_dict(), 'user_type': 'user'}

        if employee:
            session['user_type'] = 'employee'
            login_user(employee)
            return {'employee': employee.to_dict(), 'user_type': 'employee'}

    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    session.clear()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        user = User(
            firstname=form.data['firstname'],
            lastname=form.data['lastname'],
            email=form.data['email'],
            phone=form.data['phone'],
            username=form.data['username'],
            address=form.data['address'],
            city=form.data['city'],
            state=form.data['state'],
            password=form.data['password']
        )
        db.session.add(user)
        db.session.commit()
        session['user_type'] = 'user'
        login_user(user)
        return user.to_dict()
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/unauthorized')
def unauthorized():
    return {'errors': ['Unauthorized']}, 401

from flask import Blueprint, jsonify, request
from app.models import Service, db
from app.forms import ServiceForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


service_routes = Blueprint('services', __name__)


@service_routes.route('')
def all_services():
    services = Service.query.all()
    if not services:
        return {'error': 'No services found'}, 404
    return {'services': [service.to_dict() for service in services]}


@service_routes.route('/<int:serviceId>')
def get_one_service(serviceId):
    service = Service.query.filter(Service.id == serviceId).first()
    if not service:
        return {'error': 'Service not found'}, 404

    return service.to_dict()


@service_routes.route('/', methods=['POST'])
@login_required
def create_new_service():
    if not current_user.is_owner:
        return {'error': 'Only the owner can create a new service'}, 403

    form = ServiceForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        new_service = Service(
            type=data['type'],
            name=data['name'],
            price=data['price'],
            description=data['description']
        )

        db.session.add(new_service)
        db.session.commit()
        return new_service.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@service_routes.route('/<int:serviceId>', methods=['PUT'])
@login_required
def edit_service(serviceId):
    service = Service.query.filter(Service.id == serviceId).first()
    if not service:
        return {'error': 'Service not found'}, 404
    if not current_user.is_owner:
        return {'error': 'Only the owner can edit a service'}, 403

    form = ServiceForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        service.type = data['type']
        service.name = data['name']
        service.price = data['price']
        service.description = data['description']

        db.session.commit()
        return service.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@service_routes.route('/<int:serviceId>', methods=['DELETE'])
@login_required
def delete_service(serviceId):
    service = Service.query.filter(Service.id == serviceId).first()
    if not service:
        return {'error': 'Service not found'}, 404
    if not current_user.is_owner:
        return {'error': 'Only the owner can delete a service'}, 403

    db.session.delete(service)
    return {'message': 'Service successfully deleted'}

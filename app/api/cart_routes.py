from flask import Blueprint, jsonify, request
from app.models import Employee, User, Cart, Company, Service, db
from app.forms import CartForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


cart_routes = Blueprint('carts', __name__)


@cart_routes.route('/<int:userId>')
@login_required
def get_user_cart(userId):
    cart_items = Cart.query.filter(Cart.userId == userId).all()
    if not cart_items:
        return {'message': 'User has no items in the cart'}, 404
    return {'cart_items': [cart_item.to_dict() for cart_item in cart_items]}


@cart_routes.route('/<int:userId>/update', methods=['POST'])
@login_required
def update_cart(userId):
    cart = Cart.query.filter(Cart.userId == userId).first()
    if not cart:
        return {'error': 'No cart associated with this user'}

    form = CartForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        data = form.data
        serviceId = data['serviceId']
        quantity = data['quantity']

        service = Service.query.get(serviceId)
        if not service:
            return {'error': 'Service not found'}, 404

        cart_item = Cart.query.filter(
            Cart.userId == userId, Cart.serviceId == serviceId).first()

        if cart_item:
            cart_item.quantity += quantity
            cart_item.serviceTotal = service.price * cart_item.quantity
        else:
            cart_item = Cart(
                userId=userId,
                companyId=service.companyId,
                serviceId=serviceId,
                quantity=quantity,
                serviceTotal=service.price * quantity,
            )

        db.session.add(cart_item)
        db.session.commit()

        cart_items = Cart.query.filter(Cart.userId == userId).all()
        total = sum(cart_item.serviceTotal for cart_item in cart_items)
        cart.cartTotal = total

        db.session.commit()

        return cart_item.to_dict()
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@cart_routes.route('/<int:userId>/remove', methods=['DELETE'])
@login_required
def remove_from_cart(userId):
    cart = Cart.query.filter(Cart.userId == userId).first()
    if not cart:
        return {'error': 'No cart associated with this user'}

    form = CartForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        data = form.data
        serviceId = data['serviceId']

        cart_item = Cart.query.filter(
            Cart.userId == userId, Cart.serviceId == serviceId).first()

        if not cart_item:
            return {'error': 'Item not found in the cart'}, 404

        cart.cartTotal -= cart_item.serviceTotal

        db.session.delete(cart_item)
        db.session.commit()

        return {'message': 'Item removed from the cart'}

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 400

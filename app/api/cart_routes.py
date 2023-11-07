from flask import Blueprint, jsonify, request
from app.models import Employee, User, Cart, CartItem, Company, Service, db
from app.forms import CartItemForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


cart_routes = Blueprint('carts', __name__)


@cart_routes.route("/<int:cartId>", methods=["DELETE"])
@login_required
def delete_shoppingCart(cartId):
    cart = Cart.query.get(cartId)
    if not cart:
        return {'error': 'Cart does not exist'}, 404
    if cart.userId != current_user.id:
        return {'error': 'Unauthorized'}, 401
    db.session.delete(cart)
    db.session.commit()

    return jsonify({"message": "Cart deleted successfully"})


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

    form = Cart()
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

    form = CartItemForm()
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


@cart_routes.route('/<int:userId>/add', methods=['POST'])
@login_required
def add_to_cart(userId):
    user = User.query.get(userId)
    if not user:
        return {'error': 'User does not exist'}, 404

    data = request.get_json()

    if 'serviceId' not in data or 'quantity' not in data:
        return {'error': 'Please provide both serviceId and quantity'}, 400

    serviceId = data['serviceId']
    service = Service.query.get(serviceId)
    if service is None:
        return {'error': 'Service not found'}, 404

    quantity = data['quantity']
    if quantity <= 0:
        return {'error': 'Quantity must be greater than 0'}, 400

    service_price = service.price
    service_total = service_price * quantity

    cart = Cart.query.filter_by(userId=current_user.id).first()
    if cart is None:
        cart = Cart(userId=current_user.id)
        db.session.add(cart)

    # Add the service to the cart
    cart_item = CartItem(
        cart=cart,
        service=service,
        quantity=quantity,
        serviceTotal=service_total
    )

    db.session.add(cart_item)
    db.session.commit()

    return {'message': 'Service added to cart successfully'}

from flask import Blueprint, jsonify, request
from app.models import Employee, User, Cart, CartItem, Company, Service, db
from app.forms import CartItemForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


cart_routes = Blueprint('carts', __name__)


@cart_routes.route('/<int:companyId>/<int:userId>', methods=['DELETE'])
@login_required
def delete_cart(companyId, userId):
    active_cart = Cart.query.filter(
        Cart.companyId == companyId,
        Cart.userId == userId,
        Cart.checkedOut == False
    ).first()
    if not active_cart:
        return {'error': 'No active cart found for deletion'}, 404

    if active_cart.userId != current_user.id or active_cart.companyId != companyId:
        return {'error': 'Unauthorized'}, 401

    db.session.delete(active_cart)
    db.session.commit()

    return jsonify({"message": "Cart deleted successfully"})


@cart_routes.route('/<int:companyId>/<int:userId>')
@login_required
def get_user_cart(companyId, userId):
    active_cart = Cart.query.filter(
        Cart.companyId == companyId,
        Cart.userId == userId,
        Cart.checkedOut == False
    ).first()

    if not active_cart:
        active_cart = Cart(companyId=companyId, userId=userId)
        db.session.add(active_cart)
        db.session.commit()

    cart_items = active_cart.cart_items
    cart_items_data = []

    for cart_item in cart_items:
        service_data = cart_item.service.to_dict()
        cart_item_data = cart_item.to_dict()
        cart_item_data['service'] = service_data
        cart_items_data.append(cart_item_data)

    cart_total = active_cart.calculate_cart_total()
        
    return {'cart': active_cart.to_dict(), 'cart_items': cart_items_data, 'cartTotal': cart_total}


@cart_routes.route('/<int:companyId>/<int:userId>/update', methods=['POST'])
@login_required
def update_cart(companyId, userId):
    cart = Cart.query.filter(Cart.companyId == companyId,
                             Cart.userId == userId).first()

    if not cart:
        cart = Cart(companyId=companyId, userId=userId)
        db.session.add(cart)
        db.session.commit()

    data = request.get_json()
    if 'serviceId' not in data or 'quantity' not in data:
        return {'error': 'Please provide both serviceId and quantity'}, 400

    serviceId = data['serviceId']
    quantity = int(data['quantity'])

    if not isinstance(quantity, int) or quantity <= 0:
        return {'error': 'Invalid quantity provided'}, 400

    service = Service.query.get(serviceId)
    if not service:
        return {'error': 'Service not found'}, 404
    
    print(f"serviceId: {serviceId}, quantity: {quantity}")

    cart_item = CartItem.query.filter(
        CartItem.cartId == cart.id, CartItem.serviceId == serviceId).first()

    if cart_item:
        if quantity == 0:
            db.session.delete(cart_item)
        else:
            cart_item.quantity = quantity
            cart_item.serviceTotal = service.price * quantity
    else:
        if quantity != 0:
            cart_item = CartItem(
                cartId=cart.id,
                serviceId=serviceId,
                quantity=quantity,
                price=service.price,
                serviceTotal=service.price * quantity,
            )
        db.session.add(cart_item)

    db.session.add(cart_item)

    cart.cartTotal = cart.calculate_cart_total()

    db.session.commit()

    return cart.to_dict()


@cart_routes.route('/<int:companyId>/<int:userId>/remove/<int:serviceId>', methods=['DELETE'])
@login_required
def remove_from_cart(companyId, userId, serviceId):
    cart = Cart.query.filter(Cart.companyId == companyId,
                             Cart.userId == userId).first()
    if not cart:
        return {'error': 'No cart associated with this user'}, 404

    cart_item = CartItem.query.filter(
        CartItem.cartId == cart.id, CartItem.serviceId == serviceId).first()

    if not cart_item:
        return {'error': 'Item not found in the cart'}, 404

    cart.cartTotal -= cart_item.serviceTotal

    db.session.delete(cart_item)

    if not cart.cart_items:
        db.session.delete(cart)

    db.session.commit()

    return {'message': 'Item removed from the cart'}


@cart_routes.route('/<int:companyId>/<int:userId>/add', methods=['POST'])
@login_required
def add_to_cart(companyId, userId):
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
        company = Company.query.get(companyId)
        if company:
            cart = Cart(companyId=company.id,
                        userId=current_user.id, cartTotal=0)
            db.session.add(cart)
        else:
            return {'error': 'Company not found for the service'}, 404

    # Check if the service is already in the cart
    cart_item = CartItem.query.filter(
        CartItem.cartId == cart.id, CartItem.serviceId == serviceId).first()

    if cart_item:
        cart_item.quantity += quantity
        cart_item.serviceTotal = service_price * cart_item.quantity
    else:
        cart_item = CartItem(
            cartId=cart.id,
            serviceId=serviceId,
            quantity=quantity,
            price=service_price,
            serviceTotal=service_total,
        )

    db.session.add(cart_item)
    db.session.commit()

    cart.cartTotal = cart.calculate_cart_total()
    db.session.commit()

    return {'message': 'Service added to cart successfully'}

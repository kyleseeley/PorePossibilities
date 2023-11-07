from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import CartItem, Cart, db
from app.forms import CartItemForm
from .auth_routes import validation_errors_to_error_messages


cartItem_routes = Blueprint('cartItem', __name__)


@cartItem_routes.route('/<int:shoppingCartItemId>', methods=["PUT"])
@login_required
def update_cartItem(cartItemId):
    if not current_user:
        return {'error': 'Unauthorized: User is not logged in'}, 401
    cartItem = CartItem.query.get(cartItemId)
    if not cartItem:
        return {'error': 'Cart item not found'}, 404
    form = CartItemForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():

        cart = Cart.query.get(cartItem.cartId)
        itemDetails = cartItem.to_dict()
        cart.total += itemDetails['price'] * \
            (form.data['quantity'] - cartItem.quantity)

        cartItem.quantity = form.data["quantity"]
        db.session.commit()
        return cartItem.to_dict(), 200
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@cartItem_routes.route('/<int:cartItemId>', methods=["DELETE"])
@login_required
def delete_cartItem(cartItemId):
    if not current_user:
        return {'error': 'Unauthorized: User is not logged in'}, 401
    cartItem = CartItem.query.filter(CartItem.id == cartItemId).first()
    if not cartItem:
        return {'error': 'Cart item not found'}, 404
    cart = Cart.query.get(cartItem.cartId)
    cart_dict = current_user.get_cart(cart.companyId)

    if len(cart_dict['items']) == 1:
        db.session.delete(cart)
    else:

        itemDetails = cartItem.to_dict()
        cart.total -= itemDetails['price'] * cartItem.quantity

    db.session.delete(cartItem)
    db.session.commit()

    return {"message": "Successfully deleted"}

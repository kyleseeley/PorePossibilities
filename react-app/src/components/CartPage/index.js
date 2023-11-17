import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  getCartThunk,
  updateCartThunk,
  removeItemFromCartThunk,
} from "../../store/cart";
import "./CartPage.css";

const CartPage = () => {
  const user = useSelector((state) => state.session.user);
  const cart = useSelector((state) => state.cart);
  const dispatch = useDispatch();
  console.log("cart", cart);

  useEffect(() => {
    if (user) {
      dispatch(getCartThunk(1, user.id));
    }
  }, [dispatch, user]);

  const cartItemsArray = Object.values(cart.cartItems);

  const handleQuantityChange = (serviceId, quantity) => {
    dispatch(updateCartThunk(1, user.id, serviceId, quantity));
  };

  const handleDeleteItem = (serviceId) => {
    dispatch(removeItemFromCartThunk(1, serviceId, user.id));
  };

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="cart-container">
        <h2 className="cart-title">Your Cart</h2>
        <ul className="cart-items-container">
          {cartItemsArray.map((item) => (
            <li key={item.id} className="cart-items">
              <p className="cart-service">{item.service.name}</p>
              <label htmlFor={`quantity-${item.id}`}>Quantity:</label>
              <select
                value={item.quantity}
                className="cart-quantity"
                onChange={(e) => handleQuantityChange(item.id, e.target.value)}
              >
                {[1, 2, 3, 4, 5].map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
              <p className="cart-price">Price: ${item.price}</p>
              <div className="cart-item-actions">
                <button onClick={() => handleDeleteItem(item.id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
        <p className="cart-total">Total: ${cart.cartTotal}</p>
      </div>
    </div>
  );
};

export default CartPage;

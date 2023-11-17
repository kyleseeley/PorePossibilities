import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { getCartThunk } from "../../store/cart";

const CartPage = () => {
  const user = useSelector((state) => state.session.user);
  const cart = useSelector((state) => state.cart);
  const dispatch = useDispatch();

  useEffect(() => {
    if (user) {
      dispatch(getCartThunk(1, user.id));
    }
  }, [dispatch, user]);

  const cartItemsArray = Object.values(cart.cartItems);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <h2 className="cart-title">Your Cart</h2>
      <p>Total: {cart.cartTotal}</p>
      <ul>
        {cartItemsArray.map((item) => (
          <li key={item.id}>
            <p>Service: {item.service.name}</p>
            <p>Quantity: {item.quantity}</p>
            <p>Price: {item.price}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CartPage;

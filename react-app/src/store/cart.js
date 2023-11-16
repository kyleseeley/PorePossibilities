import { csrfFetch } from "./csrf";

const GET_CART = "session/GET_CART";
const UPDATE_CART = "session/UPDATE_CART";
const REMOVE_ITEM_FROM_CART = "session/REMOVE_ITEM_FROM_CART";
const DELETE_CART = "session/REMOVE_CART";

export const getCart = (cart) => ({
  type: GET_CART,
  cart,
});

export const updateCart = (serviceId) => ({
  type: UPDATE_CART,
  serviceId,
});

export const removeItemFromCart = (serviceId) => ({
  type: REMOVE_ITEM_FROM_CART,
  serviceId,
});

export const deleteCart = () => ({
  type: DELETE_CART,
});

export const getCartThunk = (companyId, userId) => async (dispatch) => {
  const response = await csrfFetch(`/api/carts/${companyId}/${userId}`);
  if (!response.ok) {
    throw new Error("Error fetching user's cart");
  }

  const data = await response.json();
  dispatch(getCart(data.cart_items));
};

export const updateCartThunk =
  (companyId, userId, serviceId, quantity) => async (dispatch) => {
    const response = await csrfFetch(
      `/api/carts/${companyId}/${userId}/update`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ serviceId, quantity }),
      }
    );

    if (!response.ok) {
      throw new Error("Error updating user's cart");
    }

    const updatedCartItem = await response.json();
    dispatch(updateCart(updatedCartItem));
  };

export const removeItemFromCartThunk =
  (companyId, userId, serviceId) => async (dispatch) => {
    const response = await csrfFetch(
      `/api/carts/${companyId}/${userId}/remove/${serviceId}`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      throw new Error("Error removing item from user's cart");
    }

    dispatch(removeItemFromCart(serviceId));
  };

export const deleteCartThunk = (companyId, userId) => async (dispatch) => {
  const response = await csrfFetch(`/api/carts/${companyId}/${userId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Error deleting user's cart");
  }

  dispatch(deleteCart());
};

const initialState = {};

const cartReducer = (state = initialState, action) => {
  switch (action.type) {
    case GET_CART:
      return action.cart;
    case UPDATE_CART:
      return {
        ...state,
        [action.cartItem.serviceId]: action.cartItem,
      };
    case REMOVE_ITEM_FROM_CART:
      const newState = { ...state };
      delete newState[action.serviceId];
      return newState;
    case DELETE_CART:
      return initialState;
    default:
      return state;
  }
};

export default cartReducer;

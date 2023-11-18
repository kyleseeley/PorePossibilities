import { csrfFetch } from "./csrf";

const GET_CART = "session/GET_CART";
const UPDATE_CART = "session/UPDATE_CART";
const REMOVE_ITEM_FROM_CART = "session/REMOVE_ITEM_FROM_CART";
const DELETE_CART = "session/REMOVE_CART";

export const getCart = (cartItems, cartTotal) => ({
  type: GET_CART,
  payload: { cartItems, cartTotal },
});

export const updateCart = (cartItem) => ({
  type: UPDATE_CART,
  cartItem,
});

export const removeItemFromCart = (serviceId) => ({
  type: REMOVE_ITEM_FROM_CART,
  serviceId,
});

export const deleteCart = (cartId) => ({
  type: DELETE_CART,
  cartId,
});

export const getCartThunk = (companyId, userId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/cart/${companyId}/${userId}`);
    if (!response.ok) {
      throw new Error(`Error fetching user's cart. Status: ${response.status}`);
    }

    const responseData = await response.json();

    dispatch(getCart(responseData.cart_items, responseData.cartTotal));
  } catch (error) {
    console.error("Error in getCartThunk:", error);
  }
};

export const updateCartThunk =
  (companyId, userId, serviceId, quantity) => async (dispatch) => {
    const response = await csrfFetch(
      `/api/cart/${companyId}/${userId}/update`,
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
      `/api/cart/${companyId}/${userId}/remove/${serviceId}`,
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
  const response = await csrfFetch(`/api/cart/${companyId}/${userId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Error deleting user's cart");
  }

  dispatch(deleteCart());
};

const initialState = {
  cartItems: {},
};

const cartReducer = (state = initialState, action) => {
  switch (action.type) {
    case GET_CART:
      return {
        ...state,
        cartItems: action.payload.cartItems,
        cartTotal: action.payload.cartTotal,
      };
    case UPDATE_CART:
      return {
        ...state,
        cartItems: {
          ...state.cartItems,
          [action.cartItem.id]: action.cartItem,
        },
      };
    case REMOVE_ITEM_FROM_CART:
      const newCartItems = { ...state.cartItems };
      delete newCartItems[action.serviceId];
      return {
        ...state,
        cartItems: newCartItems,
      };

    case DELETE_CART:
      const newState = { ...state };
      delete newState[action.cartId];
      return newState;
    default:
      return state;
  }
};

export default cartReducer;

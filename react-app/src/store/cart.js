import { csrfFetch } from "./csrf";

const GET_CART = "session/GET_CART";
const UPDATE_CART = "session/UPDATE_CART";
const REMOVE_ITEM_FROM_CART = "session/REMOVE_ITEM_FROM_CART";
const DELETE_CART = "session/REMOVE_CART";
// const CLEAR_CART = "session/CLEAR_CART";

export const getCart = (cartId, cartItems, cartTotal) => ({
  type: GET_CART,
  payload: { cartId, cartItems, cartTotal },
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

// export const clearCart = () => ({
//   type: CLEAR_CART,
// });

export const getCartThunk = (companyId, userId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/cart/${companyId}/${userId}`);
    if (!response.ok) {
      throw new Error(`Error fetching user's cart. Status: ${response.status}`);
    }

    const responseData = await response.json();

    dispatch(getCart(responseData.cartId, responseData.cart_items, responseData.cartTotal));
  } catch (error) {
    console.error("Error in getCartThunk:", error);
  }
};

export const updateCartThunk =
  (cartId, companyId, userId, serviceId, quantity) => async (dispatch) => {
    const response = await csrfFetch(
      `/api/cart/${cartId}/${companyId}/${userId}/update`,
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
  (cartId, companyId, userId, serviceId) => async (dispatch) => {
    const response = await csrfFetch(
      `/api/cart/${cartId}/${companyId}/${userId}/remove/${serviceId}`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      throw new Error("Error removing item from user's cart");
    }

    dispatch(removeItemFromCart(serviceId));
  };

export const deleteCartThunk = (cartId, companyId, userId) => async (dispatch) => {
  const response = await csrfFetch(`/api/cart/${cartId}/${companyId}/${userId}`, {
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
        cartId: action.payload.cartId,
        cartItems: action.payload.cartItems,
        cartTotal: action.payload.cartTotal,
      };
    case UPDATE_CART:
      console.log("updating cart");
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
    // case CLEAR_CART:
    //   console.log("clearing cart");
    //   return {
    //     ...state,
    //     cartItems: {},
    //   };
    default:
      return state;
  }
};

export default cartReducer;

import { csrfFetch } from "./csrf";

const SET_USER = "session/SET_USER";
const REMOVE_USER = "session/REMOVE_USER";

const setUser = (user) => ({
  type: SET_USER,
  payload: user,
});

const removeUser = () => ({
  type: REMOVE_USER,
});

export const authenticate = () => async (dispatch) => {
  const response = await fetch("/api/auth", {
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (response.ok) {
    const data = await response.json();
    if (data.errors) {
      return;
    }

    dispatch(setUser(data));
  }
};

export const login = (email, password) => async (dispatch) => {
  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(setUser(data));
      return null;
    } else if (response.status < 500) {
      const data = await response.json();
      if (data.errors) {
        return data.errors;
      }
    } else {
      return ["An error occurred. Please try again."];
    }
  } catch (error) {
    return ["An error occurred. Please try again."];
  }
};

export const logout = () => async (dispatch) => {
  const response = await fetch("/api/auth/logout", {
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.ok) {
    dispatch(removeUser());
  }
};

export const signUp =
  (
    firstname,
    lastname,
    email,
    phone,
    username,
    address,
    city,
    state,
    password
  ) =>
  async (dispatch) => {
    const response = await fetch("/api/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        firstname,
        lastname,
        email,
        phone,
        username,
        address,
        city,
        state,
        password,
      }),
    });
    const data = await response.json();
    if (response.ok) {
      dispatch(setUser(data));
    } else {
      if (data.errors) {
        throw data.errors;
      }
    }
  };

export const restoreUserThunk = () => async (dispatch) => {
  const response = await csrfFetch("/api/session");
  const data = await response.json();
  dispatch(setUser(data));
  return response;
};

export const editUserThunk = (user) => async (dispatch) => {
  const response = await csrfFetch("/api/session/userInfo", {
    method: "PUT",
    body: JSON.stringify(user),
  });

  const data = await response.json();
  dispatch(setUser(data));
  return response;
};

export const deleteUserThunk = () => async (dispatch) => {
  const response = await csrfFetch("/api/session/userInfo", {
    method: "DELETE",
  });

  if (response.ok) {
    dispatch(removeUser());
  }
  return response;
};

const initialState = { user: null };

export default function sessionReducer(state = initialState, action) {
  switch (action.type) {
    case SET_USER:
      return { user: action.payload };
    case REMOVE_USER:
      return { user: null };
    default:
      return state;
  }
}

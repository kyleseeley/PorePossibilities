import { csrfFetch } from "./csrf";

const FETCH_ALL_APPOINTMENTS = "session/GET_ALL_APPOINTMENTS";
const FETCH_ONE_APPOINTMENT = "session/GET_ONE_APPOINTMENT";
const CREATE_APPOINTMENT = "session/CREATE_APPOINTMENT";
const UPDATE_APPOINTMENT = "session/UPDATE_APPOINTMENT";
const DELETE_APPOINTMENT = "session/DELETE_APPOINTMENT";

const fetchAllAppointments = (appointments) => ({
  type: FETCH_ALL_APPOINTMENTS,
  appointments,
});

const fetchOneAppointment = (appointmentId) => ({
  type: FETCH_ONE_APPOINTMENT,
  appointmentId,
});

const createAppointment = (appointment) => ({
  type: CREATE_APPOINTMENT,
  appointment,
});

const updateAppointment = (appointmentId, updatedAppointmentData) => ({
  type: UPDATE_APPOINTMENT,
  appointmentId,
  updatedAppointmentData,
});

const deleteAppointment = (appointmentId) => ({
  type: DELETE_APPOINTMENT,
  appointmentId,
});

export const fetchAllAppointmentsThunk = () => async (dispatch) => {
  const response = await csrfFetch("/api/appointments");
  if (!response.ok) {
    throw new Error("Error fetching appointments");
  }

  const responseData = await response.json();

  dispatch(fetchAllAppointments(responseData));
};

export const fetchOneAppointmentThunk = (appointmentId) => async (dispatch) => {
  const response = await csrfFetch(`/api/appointments/${appointmentId}`);
  if (!response.ok) {
    throw new Error("Error fetching appointment");
  }

  const responseData = await response.json();

  dispatch(fetchOneAppointment(responseData));
};

export const createAppointmentThunk =
  (userId, companyId, employeeId, appointmentDate, appointmentTime) =>
  async (dispatch) => {
    const response = await csrfFetch(`/api/appointments/${companyId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userId,
        companyId,
        employeeId,
        appointmentDate,
        appointmentTime,
      }),
    });
    if (!response.ok) {
      throw new Error("Error creating appointment");
    }
    const responseData = await response.json();
    dispatch(createAppointment(responseData));
  };

export const updateAppointmentThunk =
  (appointmentId, updatedAppointmentData) => async (dispatch) => {
    const response = await csrfFetch(`/api/appointments/${appointmentId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedAppointmentData),
    });
    if (!response.ok) {
      throw new Error("Error updating appointment");
    }
    console.log("response", response);
    const responseData = await response.json();
    console.log("responseData", responseData);
    dispatch(updateAppointment(appointmentId, responseData));
    dispatch(fetchAllAppointmentsThunk());
  };

export const deleteAppointmentThunk = (appointmentId) => async (dispatch) => {
  const response = await csrfFetch(`/api/appointments/${appointmentId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Error deleting appointment");
  }

  dispatch(deleteAppointment(appointmentId));
  dispatch(fetchAllAppointmentsThunk());
};

const initialState = {};

const appointmentReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_ALL_APPOINTMENTS:
      return { ...state, ...action.appointments };
    case FETCH_ONE_APPOINTMENT:
      return {
        ...state,
        [action.appointment.id]: action.appointment,
      };
    case CREATE_APPOINTMENT:
      return {
        ...state,
        [action.appointment.id]: action.appointment,
      };
    case UPDATE_APPOINTMENT:
      return {
        ...state,
        [action.appointmentId]: {
          ...state[action.appointmentId],
          ...action.updatedAppointmentData,
        },
      };
    // return {
    //   ...state,
    //   [action.appointment.id]: action.appointment,
    // };
    case DELETE_APPOINTMENT:
      const newState = { ...state };
      delete newState[action.appointmentId];
      return newState;
    default:
      return state;
  }
};

export default appointmentReducer;

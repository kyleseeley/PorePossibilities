import { csrfFetch } from "./csrf";

export const FETCH_ALL_SERVICES = "services/FETCH_ALL_SERVICES";
export const FETCH_ONE_SERVICE = "services/FETCH_ONE_SERVICE";
export const CREATE_NEW_SERVICE = "services/CREATE_NEW_SERVICE";
export const UPDATE_SERVICE = "services/UPDATE_SERVICE";
export const DELETE_SERVICE = "services/DELETE_SERVICE";

export const fetchAllServices = (services) => ({
  type: FETCH_ALL_SERVICES,
  services,
});

export const fetchOneService = (serviceId) => ({
  type: FETCH_ONE_SERVICE,
  serviceId,
});

export const createNewService = (serviceInfo) => ({
  type: CREATE_NEW_SERVICE,
  serviceInfo,
});

export const updateService = (serviceId) => ({
  type: UPDATE_SERVICE,
  serviceId,
});

export const deleteService = (serviceId) => ({
  type: DELETE_SERVICE,
  serviceId,
});

export const fetchAllServicesThunk = () => async (dispatch) => {
  const response = await csrfFetch("/api/services");
  if (!response.ok) {
    throw new Error("Error fetching services");
  }

  const responseData = await response.json();
  const services = responseData.services;

  dispatch(fetchAllServices(services));
};

export const fetchOneServiceThunk = (serviceId) => async (dispatch) => {
  const response = await csrfFetch(`/api/services/${serviceId}`);
  if (!response.ok) {
    throw new Error("Error fetching service");
  }

  const responseData = await response.json();
  const service = responseData.Services;

  dispatch(fetchOneService(service));
};

export const createNewServiceThunk =
  (type, name, price, description, duration) => async (dispatch) => {
    const response = await csrfFetch("/api/services", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type,
        name,
        price,
        description,
        duration,
      }),
    });
    if (!response.ok) {
      throw new Error("Error creating service");
    }

    const data = await response.json();
    dispatch(createNewService(data));
    dispatch(fetchAllServices());
  };

export const updateServiceThunk =
  (serviceId, updatedServiceData) => async (dispatch) => {
    const response = await csrfFetch(`/api/services/${serviceId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedServiceData),
    });
    if (!response.ok) {
      throw new Error("Error updating service");
    }

    const updatedService = await response.json();
    dispatch(updateService(updatedService));

    return updatedService;
  };

export const deleteServiceThunk = (serviceId) => async (dispatch) => {
  const response = await csrfFetch(`/api/services/${serviceId}`, {
    method: "DELETE",
  });

  await response.json();

  dispatch(deleteService(serviceId));
};

const initialState = {};

const serviceReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_ALL_SERVICES:
      return { ...state, ...action.services };
    case FETCH_ONE_SERVICE:
      return {
        ...state,
        [action.service.id]: action.service,
      };
    case CREATE_NEW_SERVICE:
      return {
        ...state,
        [action.service.id]: action.service,
      };
    case UPDATE_SERVICE:
      return {
        ...state,
        [action.service.id]: action.service,
      };
    case DELETE_SERVICE:
      const newState = { ...state };
      delete newState[action.serviceId];
      return newState;
    default:
      return state;
  }
};

export default serviceReducer;

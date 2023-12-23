import { csrfFetch } from "./csrf";

const FETCH_ALL_COMPANIES = "session/FETCH_ALL_COMPANIES";
const FETCH_ONE_COMPANY = "session/FETCH_ONE_COMPANY";
const CREATE_COMPANY = "session/CREATE_COMPANY";
const UPDATE_COMPANY = "session/UPDATE_COMPANY";
const DELETE_COMPANY = "session/DELETE_COMPANY";

const fetchAllCompanies = (companies) => ({
  type: FETCH_ALL_COMPANIES,
  companies,
});

const fetchOneCompany = (companyId) => ({
  type: FETCH_ONE_COMPANY,
  companyId,
});

const createCompany = (company) => ({
  type: CREATE_COMPANY,
  company,
});

const updateCompany = (companyId) => ({
  type: UPDATE_COMPANY,
  companyId,
});

const deleteCompany = (companyId) => ({
  type: DELETE_COMPANY,
  companyId,
});

export const fetchAllCompaniesThunk = () => async (dispatch) => {
  const response = await csrfFetch("/api/companies");
  if (!response.ok) {
    throw new Error("Error fetching companies");
  }

  const resonseData = await response.json();

  dispatch(fetchAllCompanies(resonseData));
};

export const fetchOneCompanyThunk = (companyId) => async (dispatch) => {
  const response = await csrfFetch(`/api/companies/${companyId}`);
  if (!response.ok) {
    throw new Error("Error fetching company");
  }

  const resonseData = await response.json();

  dispatch(fetchOneCompany(resonseData));
};

export const createCompanyThunk =
  (
    name,
    email,
    phone,
    address,
    city,
    state,
    zip_code,
    monday_open,
    monday_close,
    tuesday_open,
    tuesday_close,
    wednesday_open,
    wednesday_close,
    thursday_open,
    thursday_close,
    friday_open,
    friday_close,
    saturday_open,
    saturday_close,
    sunday_open,
    sunday_close
  ) =>
  async (dispatch) => {
    const response = await csrfFetch("/api/companies", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        email,
        phone,
        address,
        city,
        state,
        zip_code,
        monday_open,
        monday_close,
        tuesday_open,
        tuesday_close,
        wednesday_open,
        wednesday_close,
        thursday_open,
        thursday_close,
        friday_open,
        friday_close,
        saturday_open,
        saturday_close,
        sunday_open,
        sunday_close,
      }),
    });
    if (!response.ok) {
      throw new Error("Error creating company");
    }

    const responseData = await response.json();
    dispatch(createCompany(responseData));
  };

export const updateCompanyThunk =
  (companyId, updatedCompanyData) => async (dispatch) => {
    const response = await csrfFetch(`/api/companies/${companyId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedCompanyData),
    });
    if (!response.ok) {
      throw new Error("Error updating company");
    }

    const responseData = await response.json();
    dispatch(updateCompany(responseData));
  };

export const deleteCompanyThunk = (companyId) => async (dispatch) => {
  const response = await csrfFetch(`/api/companies/${companyId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Error deleting company");
  }

  dispatch(deleteCompany(companyId));
};

const initialState = {};

const companyReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_ALL_COMPANIES:
      return { ...state, ...action.companies };
    case FETCH_ONE_COMPANY:
    case CREATE_COMPANY:
    case UPDATE_COMPANY:
      return {
        ...state,
        [action.company.id]: action.company,
      };
    case DELETE_COMPANY:
      const newState = { ...state };
      delete newState[action.companyId];
      return newState;
    default:
      return state;
  }
};

export default companyReducer;

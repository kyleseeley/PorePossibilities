import { csrfFetch } from "./csrf";

const FETCH_ALL_EMPLOYEES = "session/GET_ALL_EMPLOYEES";
const FETCH_ONE_EMPLOYEE = "session/GET_ONE_EMPLOYEE";
const CREATE_EMPLOYEE = "session/CREATE_EMPLOYEE";
const UPDATE_EMPLOYEE = "session/UPDATE_EMPLOYEE";
const DELETE_EMPLOYEE = "session/DELETE_EMPLOYEE";

const fetchAllEmployees = (employees) => ({
  type: FETCH_ALL_EMPLOYEES,
  employees,
});

const fetchOneEmployee = (employeeId) => ({
  type: FETCH_ONE_EMPLOYEE,
  employeeId,
});

const createEmployee = (employee) => ({
  type: CREATE_EMPLOYEE,
  employee,
});

const updateEmployee = (employeeId) => ({
  type: UPDATE_EMPLOYEE,
  employeeId,
});

const deleteEmployee = (employeeId) => ({
  type: DELETE_EMPLOYEE,
  employeeId,
});

export const fetchAllEmployeesThunk = () => async (dispatch) => {
  const response = await csrfFetch("/api/employees");
  if (!response.ok) {
    throw new Error("Error fetching employees");
  }

  const responseData = await response.json();

  dispatch(fetchAllEmployees(responseData));
};

export const fetchOneEmployeeThunk = (employeeId) => async (dispatch) => {
  const response = await csrfFetch(`/api/employees/${employeeId}`);
  if (!response.ok) {
    throw new Error("Error fetching employee");
  }

  const responseData = await response.json();

  dispatch(fetchOneEmployee(responseData));
};

export const createEmployeeThunk =
  (
    firstname,
    lastname,
    email,
    authorized,
    monday_start,
    monday_end,
    tuesday_start,
    tuesday_end,
    wednesday_start,
    wednesday_end,
    thursday_start,
    thursday_end,
    friday_start,
    friday_end,
    saturday_start,
    saturday_end,
    sunday_start,
    sunday_end,
    password
  ) =>
  async (dispatch) => {
    const response = await csrfFetch("/api/employees", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        firstname,
        lastname,
        email,
        authorized,
        monday_start,
        monday_end,
        tuesday_start,
        tuesday_end,
        wednesday_start,
        wednesday_end,
        thursday_start,
        thursday_end,
        friday_start,
        friday_end,
        saturday_start,
        saturday_end,
        sunday_start,
        sunday_end,
        password,
      }),
    });
    if (!response.ok) {
      throw new Error("Error creating employee");
    }

    const responseData = await response.json();
    dispatch(createEmployee(responseData));
  };

export const updateEmployeeThunk =
  (employeeId, updatedEmployeeData) => async (dispatch) => {
    const response = await csrfFetch(`/api/employees/${employeeId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedEmployeeData),
    });
    if (!response.ok) {
      throw new Error("Error updating employee");
    }

    const responseData = await response.json();
    dispatch(updateEmployee(responseData));
  };

export const deleteEmployeeThunk = (employeeId) => async (dispatch) => {
  const response = await csrfFetch(`/api/employees/${employeeId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Error deleting employee");
  }

  dispatch(deleteEmployee(employeeId));
};

const initialState = {};

const employeeReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_ALL_EMPLOYEES:
      return { ...state, ...action.employees };
    case FETCH_ONE_EMPLOYEE:
    case CREATE_EMPLOYEE:
    case UPDATE_EMPLOYEE:
      return {
        ...state,
        [action.employee.id]: action.employee,
      };
    case DELETE_EMPLOYEE:
      const newState = { ...state };
      delete newState[action.employeeId];
      return newState;
    default:
      return state;
  }
};

export default employeeReducer;

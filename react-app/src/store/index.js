import { createStore, combineReducers, applyMiddleware, compose } from "redux";
import thunk from "redux-thunk";
import sessionReducer from "./session";
import reviewReducer from "./reviews";
import imageReducer from "./images";
import serviceReducer from "./services";
import cartReducer from "./cart";
import appointmentReducer from "./appointments";
import employeeReducer from "./employees";

const rootReducer = combineReducers({
  session: sessionReducer,
  reviews: reviewReducer,
  images: imageReducer,
  services: serviceReducer,
  cart: cartReducer,
  appointments: appointmentReducer,
  employees: employeeReducer,
});

let enhancer;

if (process.env.NODE_ENV === "production") {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = require("redux-logger").default;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState) => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;

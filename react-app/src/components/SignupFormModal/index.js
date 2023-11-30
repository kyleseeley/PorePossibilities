import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Redirect } from "react-router-dom";
import { useModal } from "../../context/Modal";
import { signUp, login } from "../../store/session";
import "./SignupForm.css";

const states = [
  "Alabama",
  "Alaska",
  "Arizona",
  "Arkansas",
  "California",
  "Colorado",
  "Connecticut",
  "Delaware",
  "Florida",
  "Georgia",
  "Hawaii",
  "Idaho",
  "Illinois",
  "Indiana",
  "Iowa",
  "Kansas",
  "Kentucky",
  "Louisiana",
  "Maine",
  "Maryland",
  "Massachusetts",
  "Michigan",
  "Minnesota",
  "Mississippi",
  "Missouri",
  "Montana",
  "Nebraska",
  "Nevada",
  "New Hampshire",
  "New Jersey",
  "New Mexico",
  "New York",
  "North Carolina",
  "North Dakota",
  "Ohio",
  "Oklahoma",
  "Oregon",
  "Pennsylvania",
  "Rhode Island",
  "South Carolina",
  "South Dakota",
  "Tennessee",
  "Texas",
  "Utah",
  "Vermont",
  "Virginia",
  "Washington",
  "West Virginia",
  "Wisconsin",
  "Wyoming",
];

function SignupFormModal() {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.session.user);
  const [firstname, setFirstName] = useState("");
  const [lastname, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [username, setUsername] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState({});
  const { closeModal } = useModal();

  const isButtonDisabled =
    !firstname ||
    !lastname ||
    !email ||
    !phone ||
    !username ||
    !address ||
    !city ||
    !state ||
    !password ||
    !confirmPassword ||
    username.length < 4;

  if (user) return <Redirect to="/" />;

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setErrors({
        confirmPassword: "Password and Confirm Password must match",
      });
      return;
    }

    if (password === confirmPassword) {
      try {
        const data = await dispatch(
          signUp(
            firstname,
            lastname,
            email,
            phone,
            username,
            address,
            city,
            state,
            password
          )
        );
        if (!data || Object.keys(data).length === 0) {
          closeModal();
        }
      } catch (error) {
        setErrors({ error: error || { _error: "An unknown error occurred." } });
      }
    }
  };

  return (
    <div className="signup-container">
      <h1 className="signup-title">Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <div className="input-container">
          <div className="column1">
            <label className="signup-input-label">
              First Name
              <input
                className="signup-input"
                type="text"
                value={firstname}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "firstname") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
            <label className="signup-input-label">
              Last Name
              <input
                className="signup-input"
                type="text"
                value={lastname}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "lastname") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
            <label className="signup-input-label">
              Email
              <input
                className="signup-input"
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "email") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
            <label className="signup-input-label">
              Phone Number
              <input
                className="signup-input"
                type="tel"
                value={phone}
                inputMode="numeric"
                pattern="[0-9]*"
                onChange={(e) => setPhone(e.target.value)}
                onKeyPress={(e) => {
                  if (!/[0-9]/.test(e.key)) {
                    e.preventDefault();
                  }
                }}
                required
              />
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "phone") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
            <label className="signup-input-label">
              Username
              <input
                className="signup-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "username") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
          </div>
          <div className="column2">
            <label className="signup-input-label">
              Address
              <input
                className="signup-input"
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                required
              />
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "address") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
            <label className="signup-input-label">
              City
              <input
                className="signup-input"
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                required
              />
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "city") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
            <label className="signup-input-label">
              State
              <select
                className="signup-input"
                defaultValue=""
                onChange={(e) => {
                  setState(e.target.value);
                }}
                required
              >
                <option value="" disabled>
                  Please select an option...
                </option>
                {states.map((state) => (
                  <option key={state} value={state}>
                    {state}
                  </option>
                ))}
              </select>
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "state") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
            <label className="signup-input-label">
              Password
              <input
                className="signup-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            {errors?.error &&
              errors.error.map((error, index) => {
                const [fieldName, errorMessage] = error.split(" : ");
                if (fieldName === "password") {
                  return (
                    <p key={index} className="error-message">
                      {errorMessage}
                    </p>
                  );
                }
                return null;
              })}
            <label className="signup-input-label">
              Confirm Password
              <input
                className="signup-input"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </label>
            {errors?.confirmPassword && (
              <p className="error-message">{errors.confirmPassword}</p>
            )}
          </div>
        </div>
        <button
          type="submit"
          className="submit-button"
          // disabled={isButtonDisabled}
        >
          Sign Up
        </button>
      </form>
    </div>
  );
}

export default SignupFormModal;

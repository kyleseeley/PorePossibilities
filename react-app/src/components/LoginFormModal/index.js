import React, { useState } from "react";
import { login } from "../../store/session";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import "./LoginForm.css";

function LoginFormModal() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState([]);
  const { closeModal } = useModal();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await dispatch(login(email, password));
    if (data) {
      setErrors(data);
    } else {
      closeModal();
    }
  };

  const handleDemoUserLogIn = (e) => {
    e.preventDefault();

    dispatch(login("demo@aa.io", "password"))
      .then(closeModal)
      .catch(async (res) => {
        const data = await res.json();
        if (data && data.errors) setErrors(data.errors);
      });
  };

  const isButtonDisabled = email.length < 4 || password.length < 6;

  console.log("Errors:", errors);

  return (
    <div className="login-container">
      <h1 className="login-title">Log In</h1>
      <form onSubmit={handleSubmit}>
        <div className="email-input-container">
          <label className="email-input-label">
            Email
            <input
              className="login-input"
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
        </div>
        <div className="password-input-container">
          <label className="password-input-label">
            Password
            <input
              className="login-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
        </div>
        <div className="login-error-container">
          {errors.length > 0 && (
            <ul className="login-error-message">
              {errors.map((error, idx) => (
                <li key={idx}>{error}</li>
              ))}
            </ul>
          )}
        </div>
        <button
          className="submit-button"
          type="submit"
          disabled={isButtonDisabled}
        >
          Log In
        </button>
        <div>
          <div className="demo-link-container" onClick={handleDemoUserLogIn}>
            <span className="demo-link">Demo User</span>
          </div>
        </div>
      </form>
    </div>
  );
}

export default LoginFormModal;

// import React, { useState } from "react";
// import { login } from "../../store/session";
// import { useDispatch, useSelector } from "react-redux";
// import { Redirect } from "react-router-dom";
// import "./LoginForm.css";

// function LoginFormPage() {
//   const dispatch = useDispatch();
//   const sessionUser = useSelector((state) => state.session.user);
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [errors, setErrors] = useState([]);

//   if (sessionUser) return <Redirect to="/" />;

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     const data = await dispatch(login(email, password));
//     if (data) {
//       setErrors(data);
//     }
//   };

//   const handleDemoUserLogIn = (e) => {
//     e.preventDefault();

//     dispatch(login("demo@aa.io", "password")).catch(async (res) => {
//       const data = await res.json();
//       if (data && data.errors) setErrors(data.errors);
//     });
//   };

//   return (
//     <div className="login-container">
//       <h1 className="login-title">Log In</h1>
//       <form onSubmit={handleSubmit}>
//         <ul className="login-errors">
//           {errors.map((error, idx) => (
//             <li key={idx}>{error}</li>
//           ))}
//         </ul>
//         <div className="email-input-container">
//           <label className="email-input-label">
//             Email
//             <input
//               className="login-input"
//               type="text"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               required
//             />
//           </label>
//         </div>
//         <div className="password-input-container">
//           <label className="password-input-label">
//             Password
//             <input
//               className="login-input"
//               type="password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               required
//             />
//           </label>
//         </div>
//         <button type="submit">Log In</button>
//         <div>
//           <button
//             className="login-button"
//             type="submit"
//             onClick={handleDemoUserLogIn}
//           >
//             Demo User Log In
//           </button>
//         </div>
//       </form>
//     </div>
//   );
// }

// export default LoginFormPage;

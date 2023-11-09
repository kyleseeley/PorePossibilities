import React from "react";
import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";

function Navigation({ isLoaded }) {
  const sessionUser = useSelector((state) => state.session.user);

  return (
    <ul className="navigation-menu">
      <NavLink exact to="/" className="navigation-home">
        <i class="fa-solid fa-house-tsunami"></i>
        {"  "}
        Pore Possibilities
      </NavLink>
      <li className="profile-button-container">
        <ProfileButton user={sessionUser} />
      </li>
    </ul>
  );
}

export default Navigation;

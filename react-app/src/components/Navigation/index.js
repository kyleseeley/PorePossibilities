import React, { useEffect, useState } from "react";
import { NavLink, Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import ProfileButton from "./ProfileButton";
import SearchBar from "../SearchBar";
import { getCartThunk } from "../../store/cart";
import "./Navigation.css";

function Navigation({ isLoaded }) {
  const dispatch = useDispatch();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const user = useSelector((state) => state.session.user);
  const regularUser = user && user.user;
  const employee = user && user.employee;
  const cart = useSelector((state) => state.cart);

  useEffect(() => {
    if (user && user.user && user.user.id && regularUser) {
      dispatch(getCartThunk(1, user.user.id));
    }
  }, [dispatch, user, cart.cartItems.length, cart.cartId, regularUser]);

  const handleSearch = async () => {
    try {
      // Show a loading indicator while the search is in progress
      setLoading(true);

      // Send a request to your server to perform the search
      const response = await fetch(`/api/search?q=${searchQuery}`);
      if (response.ok) {
        const data = await response.json();
        setSearchResults(data.results);
      } else {
        // Handle errors here
      }
    } finally {
      // Hide the loading indicator
      setLoading(false);
    }
  };

  const serviceOptions = [
    "Skincare Treatments",
    "Advanced Skincare Treatments",
    "Signature Skin Therapies",
    "Injectable Treatments",
  ];

  const aboutOptions = ["Our Story", "Meet the Team"];

  return (
    <div>
      {/* Top section */}
      <ul className="navigation-menu">
        <NavLink exact to="/" className="navigation-home">
          <i className="fa-solid fa-spa"></i>
          {"  "}
          Pore Possibilities
        </NavLink>
        <li className="search-bar-container">
          <SearchBar />
        </li>
        {regularUser && (
          <li className="ml-auto cart-icon-container">
            <NavLink to="/cart" className="cart-icon-link">
              <i className="fa-solid fa-cart-shopping">
                {cart.cartItems.length > 0 && (
                  <span className="cart-item-count">
                    {cart.cartItems.length}
                  </span>
                )}
                {cart.cartItems.length === 0 && (
                  <span className="cart-item-count">0</span>
                )}
              </i>
            </NavLink>
          </li>
        )}
        <li className="profile-button-container">
          <ProfileButton user={regularUser || employee} />
        </li>
      </ul>

      {/* Bottom section */}
      <ul className="site-navigation">
        <li className="about-dropdown">
          <NavLink to="#" className="about-dropdown-link">
            About
          </NavLink>
          <div className="about-dropdown-content">
            {aboutOptions.map((option) => (
              <NavLink
                key={option}
                to={`/about/${option.toLowerCase().replace(/\s/g, "-")}`}
                className="dropdown-option"
              >
                {option}
              </NavLink>
            ))}
          </div>
        </li>
        <li className="services-dropdown">
          <NavLink to="#" className="services-dropdown-link">
            Services
          </NavLink>
          <div className="services-dropdown-content">
            {serviceOptions.map((option) => (
              <NavLink
                key={option}
                to={`/services/${option.toLowerCase().replace(/\s/g, "-")}`}
                className="dropdown-option"
              >
                {option}
              </NavLink>
            ))}
          </div>
        </li>
      </ul>
    </div>
  );
}

export default Navigation;

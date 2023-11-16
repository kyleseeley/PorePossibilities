import React, { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import SearchBar from "../SearchBar";
import "./Navigation.css";

function Navigation({ isLoaded }) {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const sessionUser = useSelector((state) => state.session.user);

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
        <li className="profile-button-container">
          <ProfileButton user={sessionUser} />
        </li>
      </ul>

      {/* Bottom section */}
      <ul className="site-navigation">
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

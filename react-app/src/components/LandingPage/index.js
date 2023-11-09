import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { authenticate } from "../../store/session";
import "./LandingPage.css";

const LandingPage = () => {
  const dispatch = useDispatch();

  // useEffect(() => {
  //   dispatch(authenticate());
  // }, [dispatch]);

  return (
    <div>
      <h1>Landing Page</h1>
    </div>
  );
};

export default LandingPage;

import React, { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { Route, Switch } from "react-router-dom";
// import SignupFormPage from "./components/SignupFormPage";
// import LoginFormPage from "./components/LoginFormPage";
import { authenticate } from "./store/session";
import Navigation from "./components/Navigation";
import LandingPage from "./components/LandingPage";
import CartPage from "./components/CartPage";
import AdvancedSkincareTreatments from "./components/Services/AdvancedSkincareTreatments";
import SkincareTreatments from "./components/Services/SkincareTreatments";
import SignatureSkinTherapies from "./components/Services/SignatureSkinTherapies";
import InjectableTreatments from "./components/Services/InjectableTreatments";
import Appointments from "./components/Appointments";
import OurStory from "./components/OurStory";
import MeetTheTeam from "./components/MeetTheTeam";

function App() {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false);
  useEffect(() => {
    dispatch(authenticate()).then(() => setIsLoaded(true));
    // dispatch(authenticate());
  }, [dispatch]);

  return (
    <>
      <Navigation isLoaded={isLoaded} />
      <Switch>
        <Route exact path="/">
          <LandingPage />
        </Route>
        <Route expact path="/services/advanced-skincare-treatments">
          <AdvancedSkincareTreatments />
        </Route>
        <Route expact path="/services/skincare-treatments">
          <SkincareTreatments />
        </Route>
        <Route expact path="/services/signature-skin-therapies">
          <SignatureSkinTherapies />
        </Route>
        <Route expact path="/services/injectable-treatments">
          <InjectableTreatments />
        </Route>
        <Route expact path="/appointments">
          <Appointments />
        </Route>
        <Route exact path="/cart">
          <CartPage />
        </Route>
        <Route exact path="/about/our-story">
          <OurStory />
        </Route>
        <Route exact path="/about/meet-the-team">
          <MeetTheTeam />
        </Route>
      </Switch>
    </>
  );
}

export default App;

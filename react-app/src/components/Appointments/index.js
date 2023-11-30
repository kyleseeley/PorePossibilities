import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllAppointmentsThunk } from "../../store/appointments";
import "./Appointments.css";

const Appointments = () => {
  const dispatch = useDispatch();
  const appointments = useSelector((state) => state.appointments);

  useEffect(() => {
    dispatch(fetchAllAppointmentsThunk());
  }, [dispatch]);

  // Render logic for displaying appointments

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div>
        <h2>Your Appointments</h2>
        {/* Render upcoming and past appointments here */}
      </div>
    </div>
  );
};

export default Appointments;

import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchAllAppointmentsThunk,
  deleteAppointmentThunk,
  updateAppointmentThunk,
} from "../../store/appointments";
import "./Appointments.css";
import UpdateAppointmentModal from "../UpdateAppointmentModal";
import { useModal } from "../../context/Modal";
import OpenModalButton from "../OpenModalButton";

const Appointments = () => {
  const dispatch = useDispatch();
  const appointments = useSelector((state) => state.appointments.appointments);
  console.log("appointments", appointments);

  const user = useSelector((state) => state.session.user);
  const regularUser = user && user.user;
  const employee = user && user.employee;
  const [showForm, setShowForm] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const { setModalContent, closeModal } = useModal();

  const upcomingAppointments = [];
  const pastAppointments = [];

  // for (const appointmentId in appointments) {
  //   const appointment = appointments[appointmentId];

  //   const isUpcoming = new Date(appointment.appointmentDate) > new Date();

  //   if (isUpcoming) {
  //     upcomingAppointments.push(appointment);
  //   } else {
  //     pastAppointments.push(appointment);
  //   }
  // }

  for (const appointment of Object.values(appointments || {})) {
    const isUpcoming = new Date(appointment.appointmentDate) > new Date();

    if (isUpcoming) {
      upcomingAppointments.push(appointment);
    } else {
      pastAppointments.push(appointment);
    }
  }

  useEffect(() => {
    dispatch(fetchAllAppointmentsThunk());
  }, [dispatch]);

  const handleCancelAppointment = async (appointmentId) => {
    try {
      await dispatch(deleteAppointmentThunk(appointmentId));
    } catch (error) {
      console.error("Error canceling appointment", error);
    }
  };

  const handleUpdateAppointment = (appointmentId) => {
    const appointmentToUpdate = appointments.find(
      (appointment) => appointment.id === appointmentId
    );
    setSelectedAppointment(appointmentToUpdate);
    setModalContent(
      <UpdateAppointmentModal
        appointment={appointmentToUpdate}
        onClose={() => {
          setSelectedAppointment(null);
          closeModal();
        }}
      />
    );
  };

  console.log("upcoming appointments", upcomingAppointments);
  console.log("past appointments", pastAppointments);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="appointments-container">
        <h2 className="appointments-title">Your Appointments</h2>
        <div className="upcoming-appointments">
          <h3>Upcoming Appointments</h3>
          {upcomingAppointments.length === 0 ? (
            <p className="no-appointments">No upcoming appointments</p>
          ) : (
            upcomingAppointments.map(
              (appointment) =>
                ((regularUser && appointment.userId === regularUser.id) ||
                  (employee && appointment.employeeId === employee.id)) && (
                  <div key={appointment.id} className="appointment-info">
                    {/* Render individual appointment details */}
                    <p>Date: {appointment.appointmentDate}</p>
                    <p>Time: {appointment.appointmentTime}</p>
                    <p>
                      With: {appointment.employee.firstname}{" "}
                      {appointment.employee.lastname[0]}.
                    </p>
                    <p>
                      Service(s):{" "}
                      {appointment.services.length > 0
                        ? appointment.services
                            .map((service) => service.name)
                            .join(", ")
                        : "No services"}
                    </p>
                    <button
                      onClick={() => handleUpdateAppointment(appointment.id)}
                      className="update-appointment-button"
                    >
                      Update Appointment
                    </button>
                    <button
                      onClick={() => handleCancelAppointment(appointment.id)}
                      className="cancel-appointment-button"
                    >
                      Cancel Appointment
                    </button>
                  </div>
                )
            )
          )}
        </div>

        <div className="past-appointments">
          <h3>Past Appointments</h3>
          {pastAppointments.length === 0 ? (
            <p className="no-appointments">No past appointments</p>
          ) : (
            pastAppointments.map(
              (appointment) =>
                ((regularUser && appointment.userId === regularUser.id) ||
                  (employee && appointment.employeeId === employee.id)) && (
                  <div key={appointment.id} className="appointment-info">
                    {/* Render individual appointment details */}
                    <p>Date: {appointment.appointmentDate}</p>
                    <p>Time: {appointment.appointmentTime}</p>
                    <p>
                      With: {appointment.employee.firstname}{" "}
                      {appointment.employee.lastname[0]}.
                    </p>
                    <p>
                      Service(s):{" "}
                      {appointment.services.length > 0
                        ? appointment.services
                            .map((service) => service.name)
                            .join(", ")
                        : "No services"}
                    </p>
                  </div>
                )
            )
          )}
        </div>
      </div>
      {showModal && (
        <OpenModalButton modalComponent={<UpdateAppointmentModal />} />
      )}
      <div className="my-info">
        <div>
          <div>Kyle Seeley</div>
          <a href="https://github.com/kyleseeley">
            <i className="fa-brands fa-github" />
          </a>
          <a href="https://www.linkedin.com/in/kyle-seeley-6a856539/">
            <i className="fa-brands fa-linkedin" />
          </a>
        </div>
      </div>
    </div>
  );
};

export default Appointments;

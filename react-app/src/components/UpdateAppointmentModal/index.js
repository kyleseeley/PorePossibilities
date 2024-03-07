import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { updateAppointmentThunk } from "../../store/appointments";
import { fetchAllEmployeesThunk } from "../../store/employees";
import { useModal } from "../../context/Modal";
import "./UpdateAppointmentModal.css";

const timeSlots = [
  "9:00 AM",
  "9:15 AM",
  "9:30 AM",
  "9:45 AM",
  "10:00 AM",
  "10:15 AM",
  "10:30 AM",
  "10:45 AM",
  "11:00 AM",
  "11:15 AM",
  "11:30 AM",
  "11:45 AM",
  "12:00 PM",
  "12:15 PM",
  "12:30 PM",
  "12:45 PM",
  "1:00 PM",
  "1:15 PM",
  "1:30 PM",
  "1:45 PM",
  "2:00 PM",
  "2:15 PM",
  "2:30 PM",
  "2:45 PM",
  "3:00 PM",
  "3:15 PM",
  "3:30 PM",
  "3:45 PM",
  "4:00 PM",
  "4:15 PM",
  "4:30 PM",
  "4:45 PM",
  "5:00 PM",
  "5:15 PM",
  "5:30 PM",
];

const UpdateAppointmentModal = ({ appointment, setShowModal }) => {
  const dispatch = useDispatch();
  const employees = useSelector((state) => state.employees);
  const employeesArray = Object.values(employees?.employees || {});
  const user = useSelector((state) => state.session.user);
  const appointments = useSelector((state) => state.appointments.appointments);
  const companyId = 1;
  const [errors, setErrors] = useState({});
  const { closeModal, setModalContent } = useModal();
  const [dataLoaded, setDataLoaded] = useState(false);

  const formatDate = (date) => {
    if (!date || !(date instanceof Date) || isNaN(date.getTime())) {
      // Handle the case where the date is not valid
      return "";
    }

    const year = date.getUTCFullYear();
    const month = `${date.getUTCMonth() + 1}`.padStart(2, "0");
    const day = `${date.getUTCDate()}`.padStart(2, "0");

    // If the date format is 'Nov 29, 2023', convert it to '2023-11-29'
    if (date.toString().includes(",")) {
      const monthNames = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ];
      const [monthStr, dayStr, yearStr] = date.toDateString().split(" ");
      const monthNum = monthNames.indexOf(monthStr) + 1;
      return `${yearStr}-${monthNum
        .toString()
        .padStart(2, "0")}-${dayStr.padStart(2, "0")}`;
    }

    // If the date format is already '2023-11-29', return it as is
    return `${year}-${month}-${day}`;
  };

  const [formData, setFormData] = useState({
    employeeId: appointment?.employeeId,
    appointmentDate: formatDate(new Date(appointment?.appointmentDate)),
    appointmentTime: appointment?.appointmentTime,
  });

  useEffect(() => {
    dispatch(fetchAllEmployeesThunk());
  }, [dispatch]);

  const getInitialDate = () => {
    const now = new Date();
    const oneHourLater = new Date(now.getTime() + 60 * 60 * 1000);

    // Check if the current time is before the last time slot
    const lastTimeSlot = timeSlots[timeSlots.length - 1];
    const lastTimeSlotDate = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate(),
      parseInt(lastTimeSlot.split(":")[0]),
      parseInt(lastTimeSlot.split(":")[1]),
      0
    );

    const timeDifference = lastTimeSlotDate.getTime() - now.getTime();
    const timeThreshold = 59 * 60 * 1000; // 59 minutes threshold

    // If the current time is after the last time slot, set the initial date to tomorrow
    if (timeDifference < timeThreshold) {
      return formatDate(new Date(now.setDate(now.getDate() + 1)));
    }

    // Otherwise, set the initial date to one hour later
    return formatDate(oneHourLater);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleUpdate = async () => {
    try {
      await dispatch(
        updateAppointmentThunk(appointment.id, {
          ...formData,
        })
      );
      closeModal();
    } catch (error) {
      console.error("Error updating appointment", error);
    }
  };

  const getBookedTimeSlots = (employeeId, appointmentDate) => {
    const bookedTimeSlots = [];

    const employeeAppointments = appointments?.filter((appointment) => {
      const formattedAppointmentDate = formatDate(
        new Date(appointment.appointmentDate)
      );
      const formattedInputDate = formatDate(new Date(appointmentDate));

      return (
        String(appointment.employeeId) === String(employeeId) &&
        formattedAppointmentDate === formattedInputDate
      );
    });

    employeeAppointments?.forEach((appointment) => {
      // Calculate the total duration across all services
      const totalDuration = appointment.services.reduce(
        (acc, service) => acc + service.duration,
        0
      );

      const startTime = appointment.appointmentTime;
      const endTimeIndex =
        timeSlots.indexOf(startTime) + Math.ceil(totalDuration / 15);

      // Add the entire duration to the booked time slots
      for (let i = timeSlots.indexOf(startTime); i < endTimeIndex; i++) {
        bookedTimeSlots.push(timeSlots[i]);
      }
    });

    return bookedTimeSlots;
  };

  const employeeId = formData.employeeId;
  const appointmentDate = formData.appointmentDate;

  const bookedTimeSlots = getBookedTimeSlots(employeeId, appointmentDate);

  const availableTimeSlots = timeSlots.filter(
    (timeSlot) => !bookedTimeSlots.includes(timeSlot)
  );

  return (
    <div className="update-appointment-modal">
      <h2 className="update-modal-heading">Update Appointment</h2>
      <label htmlFor="employeeId" className="update-appointment-label">
        Select Employee:{" "}
      </label>
      <select
        name="employeeId"
        value={formData.employeeId}
        onChange={handleInputChange}
        className="update-appointment-input"
        required
      >
        <option value="">-- Select Employee --</option>
        {employeesArray.map((employee) => (
          <option key={employee.id} value={employee.id}>
            {employee?.firstname} {employee?.lastname[0]}.
          </option>
        ))}
      </select>
      <label htmlFor="appointmentDate" className="update-appointment-label">
        Select Date:
      </label>
      <input
        type="date"
        name="appointmentDate"
        value={formData.appointmentDate}
        min={getInitialDate()}
        className="update-appointment-input"
        onChange={handleInputChange}
        required
      />
      <label htmlFor="appointmentTime" className="update-appointment-label">
        Select Time:
      </label>
      <select
        name="appointmentTime"
        value={formData.appointmentTime}
        className="update-appointment-input"
        onChange={handleInputChange}
        required
      >
        <option value="">-- Select Time --</option>
        {availableTimeSlots.map((time) => (
          <option key={time} value={time}>
            {time}
          </option>
        ))}
      </select>

      {/* Buttons for updating and canceling */}
      <button onClick={handleUpdate} className="update-button">
        Update
      </button>
      <button onClick={closeModal} className="cancel-button">
        Cancel
      </button>
    </div>
  );
};

export default UpdateAppointmentModal;

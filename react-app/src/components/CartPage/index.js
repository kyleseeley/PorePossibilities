import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import {
  getCartThunk,
  updateCartThunk,
  removeItemFromCartThunk,
  deleteCartThunk,
} from "../../store/cart";
import {
  createAppointmentThunk,
  fetchAllAppointmentsThunk,
} from "../../store/appointments";
import { fetchAllEmployeesThunk } from "../../store/employees";
import "./CartPage.css";

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

const CartPage = () => {
  const user = useSelector((state) => state.session.user);
  const cart = useSelector((state) => state.cart);
  const employees = useSelector((state) => state.employees);
  console.log("employees", employees);
  const appointments = useSelector((state) => state.appointments.appointments);
  const companyId = 1;
  const dispatch = useDispatch();
  const history = useHistory();
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    employeeId: "",
    appointmentDate: "",
    appointmentTime: "",
  });

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

  const formatDate = (date) => {
    const year = date.getUTCFullYear();
    const month = `${date.getUTCMonth() + 1}`.padStart(2, "0");
    const day = `${date.getUTCDate()}`.padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // const getBookedTimeSlots = (employeeId, appointmentDate) => {
  //   const bookedTimeSlots = [];

  //   const employeeAppointments = appointments?.filter((appointment) => {
  //     const formattedAppointmentDate = formatDate(
  //       new Date(appointment.appointmentDate)
  //     );
  //     const formattedInputDate = formatDate(new Date(appointmentDate));

  //     return (
  //       String(appointment.employeeId) === String(employeeId) &&
  //       formattedAppointmentDate === formattedInputDate
  //     );
  //   });

  //   employeeAppointments?.forEach((appointment) => {
  //     bookedTimeSlots.push(appointment.appointmentTime);
  //   });
  //   return bookedTimeSlots;
  // };

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

  // Get the list of already booked time slots
  const bookedTimeSlots = getBookedTimeSlots(employeeId, appointmentDate);

  // Filter out booked time slots from the available options
  const availableTimeSlots = timeSlots.filter(
    (timeSlot) => !bookedTimeSlots.includes(timeSlot)
  );

  const handleCreateAppointment = async (e) => {
    e.preventDefault();
    const { employeeId, appointmentDate, appointmentTime } = formData;

    if (Object.keys(cart.cartItems).length === 0) {
      setError("A service is required to book an appointment.");
      return;
    }

    if (employeeId && appointmentDate && appointmentTime) {
      await dispatch(
        createAppointmentThunk(
          user.id,
          companyId,
          employeeId,
          appointmentDate,
          appointmentTime
        )
      );

      await dispatch(getCartThunk(companyId, user.id));

      setFormData({
        employeeId: "",
        appointmentDate: "",
        appointmentTime: "",
      });

      setError(null);

      history.push("/");
    }
  };

  const cartItemsArray = Object.values(cart.cartItems);
  const employeesArray = Object.values(employees?.employees || {});

  const handleQuantityChange = (serviceId, quantity) => {
    dispatch(
      updateCartThunk(cart.cartId, companyId, user.id, serviceId, quantity)
    );
  };

  const handleDeleteItem = (serviceId) => {
    dispatch(
      removeItemFromCartThunk(cart.cartId, companyId, user.id, serviceId)
    );
  };

  const handleDeleteCart = () => {
    dispatch(deleteCartThunk(cart.cartId, companyId, user.id)).then(() =>
      dispatch(getCartThunk(companyId, user.id))
    );
  };

  useEffect(() => {
    if (user) {
      dispatch(getCartThunk(companyId, user.id))
        .then(() => dispatch(fetchAllEmployeesThunk()))
        .then(() => dispatch(fetchAllAppointmentsThunk()));
    }
  }, [dispatch, user]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="cart-container">
        <h2 className="cart-title">Your Cart</h2>
        {cartItemsArray.length > 0 ? (
          <ul className="cart-items-container">
            {cartItemsArray.map((item) => (
              <li key={item.id} className="cart-items">
                <p className="cart-service">{item?.service?.name}</p>
                <label htmlFor={`quantity-${item.id}`}>Quantity:</label>
                <select
                  value={item.quantity}
                  className="cart-quantity"
                  onChange={(e) =>
                    handleQuantityChange(item.service.id, e.target.value)
                  }
                >
                  {[1, 2, 3, 4, 5].map((value) => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
                <p className="cart-price">Price: ${item.price}</p>
                <div>
                  <button
                    className="cart-item-delete"
                    onClick={() => handleDeleteItem(item.service.id)}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>Your Cart is Empty</p>
        )}
        <p className="cart-total">Total: ${cart.cartTotal}</p>
        {cartItemsArray.length > 0 && (
          <button
            className="delete-entire-cart-button"
            onClick={() => handleDeleteCart()}
          >
            Delete Entire Cart
          </button>
        )}
      </div>
      {/* Appointment Form */}
      <div className="appointment-form-container">
        <h2 className="appointment-form-title">Book an Appointment</h2>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleCreateAppointment} className="appointment-form">
          {/* Employee Dropdown */}
          <label htmlFor="employeeId" className="select-employee">
            Select Employee:{" "}
          </label>
          <select
            name="employeeId"
            value={formData.employeeId}
            onChange={handleInputChange}
            required
          >
            <option value="">-- Select Employee --</option>
            {employeesArray.map((employee) => (
              <option key={employee.id} value={employee.id}>
                {employee?.firstname} {employee?.lastname[0]}.
              </option>
            ))}
          </select>
          <label htmlFor="appointmentDate" className="select-date">
            Select Date:
          </label>
          <input
            type="date"
            name="appointmentDate"
            value={formData.appointmentDate}
            min={getInitialDate()}
            onChange={handleInputChange}
            required
          />
          <label htmlFor="appointmentTime" className="select-time">
            Select Time:
          </label>
          <select
            name="appointmentTime"
            defaultValue={null}
            onChange={handleInputChange}
            required
            size={8}
          >
            {availableTimeSlots.map((time) => (
              <option key={time} value={time}>
                {time}
              </option>
            ))}
          </select>
          <button
            type="submit"
            className="submit-appointment"
            onSubmit={handleCreateAppointment}
          >
            Book Appointment
          </button>
        </form>
      </div>
    </div>
  );
};

export default CartPage;

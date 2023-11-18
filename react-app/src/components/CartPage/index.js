import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  getCartThunk,
  updateCartThunk,
  removeItemFromCartThunk,
} from "../../store/cart";
import { createAppointmentThunk } from "../../store/appointments";
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
  const dispatch = useDispatch();

  const [formData, setFormData] = useState({
    employeeId: "",
    appointmentDate: "",
    appointmentTime: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleCreateAppointment = (e) => {
    e.preventDefault();
    const { employeeId, appointmentDate, appointmentTime } = formData;
    if (employeeId && appointmentDate && appointmentTime) {
      dispatch(
        createAppointmentThunk(
          user.id,
          employeeId,
          appointmentDate,
          appointmentTime
        )
      );
      setFormData({
        employeeId: "",
        appointmentDate: "",
        appointmentTime: "",
      });
    }
  };

  const cartItemsArray = Object.values(cart.cartItems);
  const employeesArray = Object.values(employees?.employees || {});

  const handleQuantityChange = (serviceId, quantity) => {
    console.log("Updating quantity...", serviceId, quantity);
    dispatch(updateCartThunk(1, user.id, serviceId, quantity));
  };

  const handleDeleteItem = (serviceId) => {
    dispatch(removeItemFromCartThunk(1, user.id, serviceId));
  };

  useEffect(() => {
    if (user) {
      dispatch(getCartThunk(1, user.id)).then(() =>
        dispatch(fetchAllEmployeesThunk())
      );
    }
  }, [dispatch, user]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="cart-container">
        <h2 className="cart-title">Your Cart</h2>
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
              <div className="cart-item-actions">
                <button onClick={() => handleDeleteItem(item.service.id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
        <p className="cart-total">Total: ${cart.cartTotal}</p>
      </div>
      {/* Appointment Form */}
      <div className="appointment-form-container">
        <h2 className="appointment-form-title">Book an Appointment</h2>
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
          >
            <option value="">-- Select Time --</option>
            {timeSlots.map((time) => (
              <option key={time} value={time}>
                {time}
              </option>
            ))}
          </select>
          <button type="submit-appointment">Book Appointment</button>
        </form>
      </div>
    </div>
  );
};

export default CartPage;

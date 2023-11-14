import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchAllServices } from "../../store/services";
import { useModal } from "../../context/Modal";
import { NavLink } from "react-router-dom";
import OpenModalButton from "../OpenModalButton";

const AdvancedSkincareTreatments = () => {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const services = useSelector((state) => state.services);
  const advancedSkincareTreatments = services.filter(
    (service) => service.type === "Advanced Skincare Treatments"
  );
};

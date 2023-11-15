import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchAllServicesThunk } from "../../../store/services";
import { fetchImageById } from "../../../store/images";
import { useModal } from "../../../context/Modal";
import { NavLink } from "react-router-dom";
import OpenModalButton from "../../OpenModalButton";
import "./AdvancedSkincareTreatments.css";

const AdvancedSkincareTreatments = () => {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const services = useSelector((state) => state.services);
  const advancedSkincareTreatments = Object.values(services).filter(
    (service) => service.type === "Advanced Skincare Treatments"
  );
  const user = useSelector((state) => state.session.user);
  const mainImageId = 8;
  const mainImage = useSelector((state) => state.images[mainImageId]);
  console.log("main image", mainImage);

  useEffect(() => {
    dispatch(fetchAllServicesThunk()).then(() =>
      dispatch(fetchImageById(mainImageId))
    );
  }, [dispatch, mainImageId]);

  return (
    <div className="page-container">
      {mainImage && (
        <div className={`image`}>
          <img src={mainImage.imageFile} alt={mainImage.name} />
        </div>
      )}
      <h2 className="advanced-skincare-title">Advanced Skincare Treatments</h2>
      <ul className="advanced-skincare-list">
        {advancedSkincareTreatments.map((service) => (
          <li key={service.id}>
            <p>{service.name}</p>
            <p>{service.description}</p>
            <p>Price: {service.price}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdvancedSkincareTreatments;

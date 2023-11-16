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
  const mainImageId1 = 3;
  const mainImageId2 = 4;
  const everythingLaserImageId = 10;
  const microneedleImageId = 11;
  const noPeelPeelImageId = 12;
  const mainImage1 = useSelector((state) => state.images[mainImageId1]);
  const mainImage2 = useSelector((state) => state.images[mainImageId2]);
  const everythingLaserImage = useSelector(
    (state) => state.images[everythingLaserImageId]
  );
  const microneedleImage = useSelector(
    (state) => state.images[microneedleImageId]
  );
  const noPeelPeelImage = useSelector(
    (state) => state.images[noPeelPeelImageId]
  );

  useEffect(() => {
    dispatch(fetchAllServicesThunk())
      .then(() => dispatch(fetchImageById(mainImageId1)))
      .then(() => dispatch(fetchImageById(mainImageId2)))
      .then(() => dispatch(fetchImageById(everythingLaserImageId)))
      .then(() => dispatch(fetchImageById(microneedleImageId)))
      .then(() => dispatch(fetchImageById(noPeelPeelImageId)));
  }, [
    dispatch,
    mainImageId1,
    mainImageId2,
    everythingLaserImageId,
    microneedleImageId,
    noPeelPeelImageId,
  ]);

  const serviceImageMap = {
    "Everything Laser": everythingLaserImage,
    Microneedle: microneedleImage,
    "No-Peel Peel": noPeelPeelImage,
  };

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="advanced-skincare-container">
        <div className="feature-info">
          <div className="image-container">
            {mainImage1 && (
              <div className="advanced-skincare-image1">
                <img src={mainImage1.imageFile} alt={mainImage1.name} />
              </div>
            )}
            {mainImage2 && (
              <div className="advanced-skincare-image2">
                <img src={mainImage2.imageFile} alt={mainImage2.name} />
              </div>
            )}
          </div>
          <div className="text-container">
            <p className="sub-title">
              Targeted Solutions for Lasting Transformation
            </p>
            <h2 className="advanced-skincare-title">
              <span>Advanced Skincare</span>
              <span>Treatments</span>
            </h2>
            <p className="advanced-info">
              Our targeted treatments are dedicated to addressing specific skin
              concerns with precision and expertise. Whether it's acne, fine
              lines, or uneven pigmentation, our skincare professionals will
              create a tailored treatment plan that focuses on delivering
              transformative and long-lasting improvements.
            </p>
          </div>
        </div>
        <ul className="advanced-skincare-list">
          {advancedSkincareTreatments.map((service) => (
            <li key={service.id} className="advanced-individual-service">
              {service.name === "Everything Laser" && everythingLaserImage && (
                <div className="advanced-skincare-service-container">
                  <img
                    src={everythingLaserImage.imageFile}
                    alt={everythingLaserImage.name}
                    className="service-image"
                  />
                  <p className="advanced-service-name">{service.name}</p>
                  <p className="advanced-service-description">
                    {service.description}
                  </p>
                  <p className="advanced-service-price">
                    Price: ${service.price}
                  </p>
                </div>
              )}
              {service.name === "Microneedle" && microneedleImage && (
                <div className="advanced-skincare-service-container">
                  <img
                    src={microneedleImage.imageFile}
                    alt={microneedleImage.name}
                    className="service-image"
                  />
                  <p className="advanced-service-name">{service.name}</p>
                  <p className="advanced-service-description">
                    {service.description}
                  </p>
                  <p className="advanced-service-price">
                    Price: ${service.price}
                  </p>
                </div>
              )}
              {service.name === "No-Peel Peel" && noPeelPeelImage && (
                <div className="advanced-skincare-service-container">
                  <img
                    src={noPeelPeelImage.imageFile}
                    alt={noPeelPeelImage.name}
                    className="service-image"
                  />
                  <p className="advanced-service-name">{service.name}</p>
                  <p className="advanced-service-description">
                    {service.description}
                  </p>
                  <p className="advanced-service-price">
                    Price: ${service.price}
                  </p>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AdvancedSkincareTreatments;

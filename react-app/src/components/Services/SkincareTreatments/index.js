import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchAllServicesThunk } from "../../../store/services";
import { fetchImageById } from "../../../store/images";
import { useModal } from "../../../context/Modal";
import { NavLink } from "react-router-dom";
import OpenModalButton from "../../OpenModalButton";
import { updateCartThunk } from "../../../store/cart";
import "./SkincareTreatments.css";

const SkincareTreatments = () => {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const services = useSelector((state) => state.services);
  const skincareTreatments = Object.values(services).filter(
    (service) => service.type === "Skincare Treatments"
  );
  const user = useSelector((state) => state.session.user);
  const cart = useSelector((state) => state.cart);
  const images = useSelector((state) => state.images);
  const mainImageId1 = 13;
  const mainImageId2 = 15;
  const mainImage1 = useSelector((state) => state.images[mainImageId1]);
  const mainImage2 = useSelector((state) => state.images[mainImageId2]);

  const handleAddToCart = (service) => {
    const cartId = cart.cartId;
    const companyId = 1;
    const userId = user.id;
    const serviceId = service.id;
    const quantity = 1;

    dispatch(updateCartThunk(cartId, companyId, userId, serviceId, quantity));
  };

  useEffect(() => {
    dispatch(fetchAllServicesThunk())
      .then(() => dispatch(fetchImageById(mainImageId1)))
      .then(() => dispatch(fetchImageById(mainImageId2)));
  }, [dispatch, mainImageId1, mainImageId2]);

  useEffect(() => {
    const fetchImages = async () => {
      for (const service of skincareTreatments) {
        const imageId = service.imageId;
        if (imageId && !images[imageId]) {
          await dispatch(fetchImageById(imageId));
        }
      }
    };
    if (skincareTreatments.length > 0 && Object.keys(images).length > 0) {
      fetchImages();
    }
  }, [dispatch, skincareTreatments, images]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="skincare-treatments-container">
        <div className="feature-info">
          <div className="image-container">
            {mainImage1 && (
              <div className="skincare-treatments-image1">
                <img src={mainImage1.imageFile} alt={mainImage1.name} />
              </div>
            )}
            {mainImage2 && (
              <div className="skincare-treatments-image2">
                <img src={mainImage2.imageFile} alt={mainImage2.name} />
              </div>
            )}
          </div>
          <div className="text-container">
            <p className="sub-title">Personalized Care, Radiant Skin.</p>
            <h2 className="skincare-treatments-title">
              <span>Skincare Treatments</span>
            </h2>
            <p className="skincare-info">
              Embrace the essence of self-care with our Skincare Treatments.
              Tailored to meet your skin's unique needs, these treatments offer
              a personalized touch to help you achieve a refreshed and radiant
              complexion.
            </p>
          </div>
        </div>
        <ul className="skincare-treatments-list">
          {skincareTreatments.map((service) => (
            <li key={service.id} className="skincare-individual-service">
              <div className="skincare-service-container">
                {/* Check if the service has an associated image */}
                {service.imageId && images[service.imageId] && (
                  <img
                    src={images[service.imageId].imageFile}
                    alt={images[service.imageId].name}
                    className="service-image"
                  />
                )}
                <p className="skincare-service-name">{service.name}</p>
                <p className="skincare-service-description">
                  {service.description}
                </p>
                <p className="skincare-service-price">
                  Price: ${service.price}
                </p>
                {user && (
                  <button
                    className="add-to-cart-button"
                    onClick={() => handleAddToCart(service)}
                  >
                    Add to Cart
                  </button>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SkincareTreatments;

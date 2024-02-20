import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchAllServicesThunk } from "../../../store/services";
import { fetchImageById } from "../../../store/images";
import { useModal } from "../../../context/Modal";
import { NavLink } from "react-router-dom";
import OpenModalButton from "../../OpenModalButton";
import { updateCartThunk } from "../../../store/cart";
import "./InjectableTreatments.css";

const InjectableTreatments = () => {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const services = useSelector((state) => state.services);
  const injectableTreatments = Object.values(services).filter(
    (service) => service.type === "Injectables"
  );
  const user = useSelector((state) => state.session.user);
  const regularUser = user && user.user;
  const cart = useSelector((state) => state.cart);
  const images = useSelector((state) => state.images);
  const mainImageId1 = 22;
  const mainImageId2 = 23;
  const mainImage1 = useSelector((state) => state.images[mainImageId1]);
  const mainImage2 = useSelector((state) => state.images[mainImageId2]);

  const handleAddToCart = (service) => {
    const cartId = cart.cartId;
    const companyId = 1;
    const userId = regularUser.id;
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
      for (const service of injectableTreatments) {
        const imageId = service.imageId;
        if (imageId && !images[imageId]) {
          await dispatch(fetchImageById(imageId));
        }
      }
    };
    if (injectableTreatments.length > 0 && Object.keys(images).length > 0) {
      fetchImages();
    }
  }, [dispatch, injectableTreatments, images]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="injectable-treatments-container">
        <div className="feature-info">
          <div className="image-container">
            {mainImage1 && (
              <div className="injectable-treatments-image1">
                <img src={mainImage1.imageFile} alt={mainImage1.name} />
              </div>
            )}
            {mainImage2 && (
              <div className="injectable-treatments-image2">
                <img src={mainImage2.imageFile} alt={mainImage2.name} />
              </div>
            )}
          </div>
          <div className="text-container">
            <p className="sub-title">Your Skin, Redefined.</p>
            <h2 className="injectable-treatments-title">
              <span>Signature Skin</span>
              <span>Therapies</span>
            </h2>
            <p className="injectable-treatments-info">
              Unlock the potential of your skin with our advanced aesthetic
              treatments that go beyond traditional skincare. Our non-invasive
              procedures are known for their powerful impact and minimal
              downtime. Experience the fusion of science and art as we redefine
              radiance and reveal your skin's true beauty.
            </p>
          </div>
        </div>
        <ul className="injectable-treatments-list">
          {injectableTreatments.map((service) => (
            <li
              key={service.id}
              className="injectable-treatments-individual-service"
            >
              <div className="injectable-treatments-service-container">
                {/* Check if the service has an associated image */}
                {service.imageId && images[service.imageId] && (
                  <img
                    src={images[service.imageId].imageFile}
                    alt={images[service.imageId].name}
                    className="service-image"
                  />
                )}
                <p className="injectable-treatments-name">{service.name}</p>
                <p className="injectable-treatments-description">
                  {service.description}
                </p>
                <p className="injectable-treatments-price">
                  Price: ${service.price}
                </p>
                {regularUser && (
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

export default InjectableTreatments;

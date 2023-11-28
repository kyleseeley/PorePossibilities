import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchAllServicesThunk } from "../../../store/services";
import { fetchImageById } from "../../../store/images";
import { useModal } from "../../../context/Modal";
import { NavLink } from "react-router-dom";
import OpenModalButton from "../../OpenModalButton";
import { updateCartThunk } from "../../../store/cart";
import "./SignatureSkinTherapies.css";

const SignatureSkinTherapies = () => {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const services = useSelector((state) => state.services);
  const signatureSkinTherapies = Object.values(services).filter(
    (service) => service.type === "Signature Skin Therapies"
  );
  const user = useSelector((state) => state.session.user);
  const cart = useSelector((state) => state.cart);
  const images = useSelector((state) => state.images);
  const mainImageId1 = 10;
  const mainImageId2 = 18;
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
      for (const service of signatureSkinTherapies) {
        const imageId = service.imageId;
        if (imageId && !images[imageId]) {
          await dispatch(fetchImageById(imageId));
        }
      }
    };
    if (signatureSkinTherapies.length > 0 && Object.keys(images).length > 0) {
      fetchImages();
    }
  }, [dispatch, signatureSkinTherapies, images]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="signature-skin-container">
        <div className="feature-info">
          <div className="image-container">
            {mainImage1 && (
              <div className="signature-skin-image1">
                <img src={mainImage1.imageFile} alt={mainImage1.name} />
              </div>
            )}
            {mainImage2 && (
              <div className="signature-skin-image2">
                <img src={mainImage2.imageFile} alt={mainImage2.name} />
              </div>
            )}
          </div>
          <div className="text-container">
            <p className="sub-title">Your Skin, Redefined.</p>
            <h2 className="signature-skin-title">
              <span>Signature Skin</span>
              <span>Therapies</span>
            </h2>
            <p className="signature-skin-info">
              Unlock the potential of your skin with our advanced aesthetic
              treatments that go beyond traditional skincare. Our non-invasive
              procedures are known for their powerful impact and minimal
              downtime. Experience the fusion of science and art as we redefine
              radiance and reveal your skin's true beauty.
            </p>
          </div>
        </div>
        <ul className="signature-skin-list">
          {signatureSkinTherapies.map((service) => (
            <li key={service.id} className="signature-skin-individual-service">
              <div className="signature-skin-service-container">
                {/* Check if the service has an associated image */}
                {service.imageId && images[service.imageId] && (
                  <img
                    src={images[service.imageId].imageFile}
                    alt={images[service.imageId].name}
                    className="service-image"
                  />
                )}
                <p className="signature-skin-name">{service.name}</p>
                <p className="signature-skin-description">
                  {service.description}
                </p>
                <p className="signature-skin-price">Price: ${service.price}</p>
                <button
                  className="add-to-cart-button"
                  onClick={() => handleAddToCart(service)}
                >
                  Add to Cart
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SignatureSkinTherapies;

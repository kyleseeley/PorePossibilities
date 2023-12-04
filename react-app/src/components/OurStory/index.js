import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState, useMemo, useCallback, useRef } from "react";
import { fetchImageById } from "../../store/images";
import "./OurStory.css";

const OurStory = () => {
  const dispatch = useDispatch();
  const imageId = 7;
  const image = useSelector((state) => state.images[imageId]);

  useEffect(() => {
    dispatch(fetchImageById(imageId));
  }, [dispatch, imageId]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="our-story-container">
        <div className="our-information">
          <h3 className="first-heading">Our Story</h3>
          <h2 className="second-heading">
            EMBRACE THE PORE POSSIBILITES DIFFERENCE
          </h2>
          <p className="our-story-paragraph">
            Welcome to Pore Possibilities, where we believe that skincare should
            be a journey of self-care, empowerment, and transformative results.
            Our story began with a passion for simplifying skincare, providing a
            sanctuary where clients can experience the ultimate in personalized
            care.
          </p>
          <p className="our-story-paragraph">
            At Pore Possibilities, we are driven by a patient-first approach. We
            take the time to listen, understand your unique skincare goals, and
            develop tailored solutions that address your specific concerns. Our
            dedicated team of skincare experts combines their expertise with the
            latest advancements in the industry to deliver exceptional results.
          </p>
        </div>
        {image && (
          <div className={`story-image`}>
            <img src={image.imageFile} alt={image.name} />
          </div>
        )}
      </div>
    </div>
  );
};

export default OurStory;

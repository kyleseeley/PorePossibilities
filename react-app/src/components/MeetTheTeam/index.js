import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState, useMemo, useCallback, useRef } from "react";
import { fetchImageById } from "../../store/images";
import "./MeetTheTeam.css";

const MeetTheTeam = () => {
  const dispatch = useDispatch();
  const ownerImageId = 29;
  const employee1ImageId = 30;
  const employee2ImageId = 31;
  const ownerImage = useSelector((state) => state.images[ownerImageId]);
  const employee1Image = useSelector((state) => state.images[employee1ImageId]);
  const employee2Image = useSelector((state) => state.images[employee2ImageId]);
  const employee = useSelector((state) => state.session.employee);

  useEffect(() => {
    dispatch(fetchImageById(ownerImageId));
    dispatch(fetchImageById(employee1ImageId));
    dispatch(fetchImageById(employee2ImageId));
  }, [dispatch, ownerImageId, employee1ImageId, employee2ImageId]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div>
        <h2 className="first-heading">Meet Our Team</h2>
        <h1 className="second-heading">OUR SKINCARE EXPERTS</h1>
      </div>
      {ownerImage && (
        <div className="owner-image">
          <img src={ownerImage.imageFile} alt={ownerImage.name} />
        </div>
      )}
      <div className="my-info">
        <div>
          <div>Kyle Seeley</div>
          <a href="https://github.com/kyleseeley">
            <i className="fa-brands fa-github" />
          </a>
          <a href="https://www.linkedin.com/in/kyle-seeley-6a856539/">
            <i className="fa-brands fa-linkedin" />
          </a>
        </div>
      </div>
    </div>
  );
};

export default MeetTheTeam;

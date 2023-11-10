import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState, useMemo } from "react";
import { authenticate } from "../../store/session";
import { fetchImageById } from "../../store/images";
import "./LandingPage.css";

const LandingPage = () => {
  const dispatch = useDispatch();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const mainImageIds = useMemo(() => [6, 7], []);
  const imageId = mainImageIds[currentImageIndex];
  const image = useSelector((state) => state.images[imageId]);

  useEffect(() => {
    dispatch(fetchImageById(imageId));
    const intervalId = setInterval(() => {
      setCurrentImageIndex(
        (prevIndex) => (prevIndex + 1) % mainImageIds.length
      );
    }, 8000);

    return () => clearInterval(intervalId);
  }, [dispatch, imageId, mainImageIds]);

  return (
    <div>
      {image && (
        <div className={`main-image`}>
          <img src={image.imageFile} alt={image.name} />
        </div>
      )}
    </div>
  );
};

export default LandingPage;

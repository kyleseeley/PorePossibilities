import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState, useMemo } from "react";
import { authenticate } from "../../store/session";
import { fetchImageById } from "../../store/images";
import { fetchReviews } from "../../store/reviews";
import "./LandingPage.css";

const LandingPage = () => {
  const dispatch = useDispatch();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const mainImageIds = useMemo(() => [6, 7], []);
  const imageId = mainImageIds[currentImageIndex];
  const image = useSelector((state) => state.images[imageId]);
  const user = useSelector((state) => state.session.user);
  const companyId = 1;
  const reviews = useSelector((state) => state.reviews[companyId] || []);

  const hasLeftReview =
    user &&
    reviews &&
    reviews.some((review) => {
      return review?.userId === user.id && review?.companyId === companyId;
    });

  const calculateTimeAgo = (reviewDate) => {
    const currentTime = new Date();
    const reviewTime = new Date(reviewDate);
    const timeDifference = currentTime - reviewTime;
    const minutesAgo = Math.floor(timeDifference / (1000 * 60));
    if (minutesAgo < 60) {
      return `${minutesAgo} minute(s) ago`;
    } else {
      const hoursAgo = Math.floor(minutesAgo / 60);
      if (hoursAgo < 24) {
        return `${hoursAgo} hour(s) ago`;
      } else {
        const daysAgo = Math.floor(hoursAgo / 24);
        return `${daysAgo} day(s) ago`;
      }
    }
  };

  console.log("has left review", hasLeftReview);

  useEffect(() => {
    dispatch(fetchImageById(imageId)).then(() =>
      dispatch(fetchReviews(companyId))
    );
    const intervalId = setInterval(() => {
      setCurrentImageIndex(
        (prevIndex) => (prevIndex + 1) % mainImageIds.length
      );
    }, 7950);

    return () => clearInterval(intervalId);
  }, [dispatch, imageId, mainImageIds, companyId]);

  return (
    <div>
      <div className="separator-line"></div>
      {image && (
        <div className={`main-image`}>
          <img src={image.imageFile} alt={image.name} />
        </div>
      )}
      <div className="separator-line"></div>
      <div className="reviews-container">
        <h2 className="review-title">Reviews</h2>
        <ul className="reviews-list">
          {reviews.map((review) => (
            <li key={review.id} className="review-item">
              <p className="review-name">
                {review?.firstname} {review?.lastname.charAt(0)}.
              </p>
              <p className="review-time">
                {calculateTimeAgo(review?.createdAt)} ago
              </p>
              <p className="review-rating">{review?.stars} Stars</p>
              <p className="review-content">{review?.review}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default LandingPage;

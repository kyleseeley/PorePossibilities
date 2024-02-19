import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState, useMemo, useCallback, useRef } from "react";
import { authenticate } from "../../store/session";
import { fetchImageById } from "../../store/images";
import { fetchReviews, deleteReviewById } from "../../store/reviews";
import { useModal } from "../../context/Modal";
import ReviewModal from "../ReviewModal";
import OpenModalButton from "../OpenModalButton";
import { usePageVisibility } from "react-page-visibility";
import { fetchAllBlogpostsThunk } from "../../store/blogposts";
import "./LandingPage.css";

const LandingPage = () => {
  const dispatch = useDispatch();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [lastUpdateTime, setLastUpdateTime] = useState(0);

  const mainImageIds = useMemo(() => [6, 7], []);
  const imageId = mainImageIds[currentImageIndex];
  const image = useSelector((state) => state.images[imageId]);
  const user = useSelector((state) => state.session.user);
  const regularUser = user && user.user;
  const employee = user && user.employee;
  const companyId = 1;
  const blogposts = useSelector((state) => state.blogposts.blogposts);
  const reviews = useSelector((state) => state.reviews[companyId] || []);
  const { setModalContent, closeModal } = useModal();
  const lastUpdateTimeRef = useRef(0);
  const isPageVisible = usePageVisibility();

  const handleEditReview = (review) => {
    setModalContent(
      <ReviewModal
        companyId={companyId}
        editReview={review}
        onClose={() => setModalContent(null)}
      />
    );
  };

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

  const calculateStarRating = () => {
    if (reviews.length) {
      const totalStars = reviews.reduce((acc, review) => acc + review.stars, 0);
      const averageStars = totalStars / reviews.length;
      return averageStars.toFixed(1);
    } else {
      return 0;
    }
  };

  const updatedStarRating = calculateStarRating();
  const numReviews = reviews.length;
  const sortedReviews = Array.isArray(reviews)
    ? reviews.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
    : [];

  const updateImageIndex = useCallback(() => {
    const currentTime = Date.now();
    if (currentTime - lastUpdateTimeRef.current > 8000 && isPageVisible) {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % 2);
      lastUpdateTimeRef.current = currentTime;
    }
    setTimeout(updateImageIndex, 8000);
  }, [lastUpdateTimeRef, setCurrentImageIndex, isPageVisible]);

  useEffect(() => {
    dispatch(fetchImageById(imageId)).then(() =>
      dispatch(fetchReviews(companyId)).then(() =>
        dispatch(fetchAllBlogpostsThunk())
      )
    );
    setTimeout(updateImageIndex, 8000);
    return () => clearTimeout(updateImageIndex);
  }, [dispatch, imageId, companyId, regularUser, updateImageIndex]);

  const hasLeftReview =
    regularUser &&
    Array.isArray(reviews) &&
    reviews.some((review) => {
      return (
        review?.userId === regularUser.id && review?.companyId === companyId
      );
    });

  // useEffect(() => {
  //   dispatch(fetchImageById(imageId)).then(() =>
  //     dispatch(fetchReviews(companyId)).then(() =>
  //       dispatch(fetchAllBlogpostsThunk())
  //     )
  //   );

  //   const timeoutId = setTimeout(updateImageIndex, 8000);

  //   return () => clearTimeout(timeoutId);
  // }, [dispatch, imageId, companyId, user, updateImageIndex]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      {image && (
        <div className={`main-image`}>
          <img src={image.imageFile} alt={image.name} />
        </div>
      )}
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="reviews-container">
        <h2 className="review-title">Reviews</h2>
        <p className="company-details">
          <b>
            {updatedStarRating} <i className="fa-solid fa-star" /> {"  "} (
            {numReviews} reviews)
          </b>
        </p>
        {regularUser && !hasLeftReview && (
          <OpenModalButton
            className="leave-review-button"
            buttonText="Leave a Review"
            modalComponent={
              <ReviewModal
                companyId={companyId}
                onClose={() => setModalContent(null)}
              />
            }
          />
        )}
        <ul className="reviews-list">
          {reviews.length > 0 ? (
            sortedReviews.map((review) => (
              <li key={review.id} className="review-item">
                <p className="review-name">
                  {review?.firstname}{" "}
                  {review?.lastname ? review.lastname.charAt(0) : ""}.
                </p>
                <p className="review-time">
                  {calculateTimeAgo(review?.createdAt)} ago
                </p>
                <div className="review-rating">
                  {Array.from({ length: review.stars }, (_, index) => (
                    <i key={index} className="fa-solid fa-star" />
                  ))}
                </div>
                <p className="review-content">{review?.review}</p>
                {regularUser?.id === review?.userId && (
                  <button
                    onClick={() => handleEditReview(review)}
                    className="edit-review-button"
                  >
                    Edit Your Review
                  </button>
                )}
                {regularUser?.id === review?.userId && (
                  <OpenModalButton
                    className="delete-review-button"
                    buttonText="Delete Your Review"
                    modalComponent={() => (
                      <div className="delete-modal">
                        <h3>Are you sure to delete this review?</h3>
                        <div className="button-container">
                          <button
                            className="yes-button"
                            onClick={() => {
                              dispatch(deleteReviewById(review?.id, companyId));
                              closeModal();
                            }}
                          >
                            Yes
                          </button>
                          <button className="no-button" onClick={closeModal}>
                            No
                          </button>
                        </div>
                      </div>
                    )}
                  />
                )}
              </li>
            ))
          ) : (
            <p>No reviews available</p>
          )}
        </ul>
      </div>
      <div className="blogposts-container">
        <h2 className="blogposts-title">Latest Blog Posts</h2>
        <ul className="blogposts-list">
          {blogposts?.map((blogpost) => (
            <li key={blogpost.id} className="blogpost-item">
              <Link to={`/blogposts/${blogpost.id}`}>
                <h3 className="blogpost-item-title">{blogpost.title}</h3>
                <p className="blogpost-blurb">
                  {blogpost.blog.substring(0, 70) + "..."}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default LandingPage;

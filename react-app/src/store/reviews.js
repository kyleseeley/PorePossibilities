import { csrfFetch } from "./csrf";

export const COMPANY_REVIEWS = "reviews/COMPANY_REVIEWS";
export const CREATE_REVIEW = "reviews/CREATE_REVIEW";
export const UPDATE_REVIEW = "reviews/UPDATE_REVIEW";
export const DELETE_REVIEW = "reviews/DELETE_REVIEW";
export const USER_REVIEWS = "reviews/USER_REVIEWS";

export const companyReviews = (companyId, reviews) => ({
  type: COMPANY_REVIEWS,
  companyId,
  reviews,
});

export const createReview = (review) => ({
  type: CREATE_REVIEW,
  review,
});

export const updateReview = (review) => ({
  type: UPDATE_REVIEW,
  review,
});

export const deleteReview = (reviewId) => ({
  type: DELETE_REVIEW,
  reviewId,
});

export const userReviews = (reviews) => ({
  type: USER_REVIEWS,
  reviews,
});

export const fetchReviews = (companyId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/companies/${companyId}/reviews`);

    if (!response.ok) {
      throw new Error("Error fetching reviews");
    }

    const responseData = await response.json();
    dispatch(companyReviews(companyId, responseData.reviews));
  } catch (error) {
    console.log("Error fetching reviews", error);
  }
};

export const createNewReview = (reviewData) => async (dispatch) => {
  try {
    const response = await csrfFetch(
      `/api/companies/${reviewData.companyId}/reviews`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          review: reviewData.review,
          stars: reviewData.stars,
        }),
      }
    );
    if (!response.ok) {
      throw new Error("Error creating a new review");
    }

    const responseData = await response.json();
    dispatch(createReview(responseData.review));
    dispatch(fetchReviews(responseData.companyId));
  } catch (error) {
    console.log("Error creating a new review", error);
  }
};

export const updateUserReview =
  (reviewId, updatedReviewData) => async (dispatch) => {
    try {
      const response = await csrfFetch(`/api/reviews/${reviewId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedReviewData),
      });

      if (!response.ok) {
        throw new Error("Error updating review");
      }

      const updatedReview = await response.json();

      dispatch(updateReview(updatedReview));
      dispatch(fetchReviews(updatedReviewData.companyId));

      return updatedReview;
    } catch (error) {
      console.log("Error updating review", error);
    }
  };

export const deleteReviewById = (reviewId, companyId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/reviews/${reviewId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Error deleting review");
    }
    dispatch(deleteReview(reviewId));
    dispatch(fetchReviews(companyId));
  } catch (error) {
    console.log("Error deleting review", error);
  }
};

export const fetchUserReviews = () => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/session/reviews`);
    if (!response.ok) {
      throw new Error("Erorr fetching user reviews");
    }
    const responseData = await response.json();
    const reviewsFromUser = responseData.reviews || [];
    dispatch(userReviews(reviewsFromUser));
  } catch (error) {
    console.log("Error fetching user reviews", error);
  }
};

const initialState = { reviewsChanged: false };

const reviewReducer = (state = initialState, action) => {
  let newState = { ...state };
  switch (action.type) {
    case COMPANY_REVIEWS:
      const { companyId, reviews } = action;
      return {
        ...newState,
        [companyId]: reviews,
      };
    case CREATE_REVIEW:
      newState[action.review.id] = action.review;
      return newState;
    case UPDATE_REVIEW:
      newState[action.review.id] = action.review;
      return newState;
    case DELETE_REVIEW:
      delete newState[action.reviewId];
      return newState;
    case USER_REVIEWS:
      action.reviews.forEach((review) => {
        if (!newState[review.id]) {
          newState[review.id] = review;
        }
      });
      return newState;
    default:
      return state;
  }
};

export default reviewReducer;

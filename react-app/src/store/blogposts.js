import { csrfFetch } from "./csrf";

const FETCH_ALL_BLOGPOSTS = "session/FETCH_ALL_BLOGPOSTS";
const FETCH_ONE_BLOGPOST = "session/FETCH_ONE_BLOGPOST";
const CREATE_BLOGPOST = "session/CREATE_BLOGPOST";
const UPDATE_BLOGPOST = "session/UPDATE_BLOGPOST";
const DELETE_BLOGPOST = "session/DELETE_BLOGPOST";

const fetchAllBlogposts = (blogposts) => ({
  type: FETCH_ALL_BLOGPOSTS,
  blogposts,
});

const fetchOneBlogpost = (blogpostId) => ({
  type: FETCH_ONE_BLOGPOST,
  blogpostId,
});

const createBlogpost = (blogpost) => ({
  type: CREATE_BLOGPOST,
  blogpost,
});

const updateBlogpost = (blogpostId, updatedBlogpostData) => ({
  type: UPDATE_BLOGPOST,
  blogpostId,
  updatedBlogpostData,
});

const deleteBlogpost = (blogpostId) => ({
  type: DELETE_BLOGPOST,
  blogpostId,
});

export const fetchAllBlogpostsThunk = () => async (dispatch) => {
  const response = await csrfFetch("/api/blogposts");
  if (!response.ok) {
    throw new Error("Error fetching blogposts");
  }

  const responseData = await response.json();

  dispatch(fetchAllBlogposts(responseData));
};

// export const fetchOneBlogpostThunk = (blogpostId) => async (dispatch) => {
//   const response = await csrfFetch(`/api/blogposts/${blogpostId}`);
//   if (!response.ok) {
//     throw new Error("Error fetching blogpost");
//   }

//   const responseData = await response.json();
//   console.log("Blogpost API Response:", responseData);

//   dispatch(fetchOneBlogpost(responseData));
// };

export const fetchOneBlogpostThunk = (blogpostId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/blogposts/${blogpostId}`);

    if (!response.ok) {
      throw new Error("Error fetching blogpost");
    }

    const responseData = await response.json();

    dispatch(fetchOneBlogpost(responseData));

    return responseData; // Return the response here
  } catch (error) {
    console.error("Error fetching blog post", error);
    throw error; // Re-throw the error to be caught by the caller
  }
};

export const createBlogpostThunk =
  (employeeId, title, blog) => async (dispatch) => {
    const response = await csrfFetch(`/api/blogposts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        employeeId,
        title,
        blog,
      }),
    });
    if (!response.ok) {
      throw new Error("Error create blogpost");
    }

    const responseData = await response.json();
    dispatch(createBlogpost(responseData));
  };

// export const updateBlogpostThunk =
//   (blogpostId, updatedBlogpostData) => async (dispatch) => {
//     const response = await csrfFetch(`/api/blogposts/${blogpostId}`, {
//       method: "PUT",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(updatedBlogpostData),
//     });
//     if (!response.ok) {
//       throw new Error("Error updating blogpost");
//     }

//     const responseData = await response.json();
//     dispatch(updateBlogpost(blogpostId, responseData));
//     dispatch(fetchOneBlogpost(blogpostId));
//   };

export const updateBlogpostThunk =
  (blogpostId, updatedBlogpostData) => async (dispatch) => {
    try {
      const response = await csrfFetch(`/api/blogposts/${blogpostId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedBlogpostData),
      });

      if (!response.ok) {
        throw new Error("Error updating blogpost");
      }

      const responseData = await response.json();
      console.log("Update Blogpost Response:", responseData);
      dispatch(updateBlogpost(blogpostId, responseData));
      return responseData;
    } catch (error) {
      console.error("Error updating blog post", error);
      throw error; // Re-throw the error to be caught by the caller
    }
  };

export const deleteBlogpostThunk = (blogpostId) => async (dispatch) => {
  const response = await csrfFetch(`/api/blogposts/${blogpostId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Error deleting blogpost");
  }

  dispatch(deleteBlogpost(blogpostId));
};

const initialState = {};

const blogpostReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_ALL_BLOGPOSTS:
      return { ...state, ...action.blogposts };
    case FETCH_ONE_BLOGPOST:
    case CREATE_BLOGPOST:
      return action.blogpost
        ? {
            ...state,
            [action.blogpost.id]: action.blogpost,
          }
        : state;
    case UPDATE_BLOGPOST:
      return {
        ...state,
        [action.blogpostId]: {
          ...state[action.blogpostId],
          ...action.updatedBlogpostData,
        },
      };
    case DELETE_BLOGPOST:
      const newState = { ...state };
      delete newState[action.blogpostId];
      return newState;
    default:
      return state;
  }
};

export default blogpostReducer;

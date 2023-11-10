import { csrfFetch } from "./csrf";

export const FETCH_IMAGES = "images/FETCH_IMAGES";
export const FETCH_ONE_IMAGE = "images/FETCH_ONE_IMAGE";
export const ADD_IMAGE = "images/ADD_IMAGE";
export const UPDATE_IMAGE = "images/UPDATE_IMAGE";
export const DELETE_IMAGE = "images/DELETE_IMAGE";

export const fetchImages = (images) => ({
  type: FETCH_IMAGES,
  images,
});

export const fetchOneImage = (image) => ({
  type: FETCH_ONE_IMAGE,
  image,
});

export const addImage = (image) => ({
  type: ADD_IMAGE,
  image,
});

export const updateImage = (image) => ({
  type: UPDATE_IMAGE,
  image,
});

export const deleteImage = (imageId) => ({
  type: DELETE_IMAGE,
  imageId,
});

export const fetchAllImages = () => async (dispatch) => {
  try {
    const response = await csrfFetch("/api/images");

    if (!response.ok) {
      throw new Error("Error fetching images");
    }

    const responseData = await response.json();
    dispatch(fetchImages(responseData.images));
  } catch (error) {
    console.log("Error fetching images", error);
  }
};

export const fetchImageById = (imageId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/images/${imageId}`);
    console.log("response", response);

    if (!response.ok) {
      throw new Error("Error fetching image");
    }

    const responseData = await response.json();
    console.log("responseData", responseData);
    dispatch(fetchOneImage(responseData));
  } catch (error) {
    console.log("Error fetching image", error);
  }
};

export const createNewImage = (name, imageFile) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/images`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        imageFile,
      }),
    });
    if (!response.ok) {
      throw new Error("Error creating image");
    }

    const responseData = await response.json();
    dispatch(addImage(responseData));
    return responseData.id;
  } catch (error) {
    console.log("Error creating image", error);
  }
};

export const updateOneImage =
  (imageId, updatedImageData) => async (dispatch) => {
    try {
      const response = await csrfFetch(`/api/images/${imageId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedImageData),
      });

      if (!response.ok) {
        throw new Error("Error updating image");
      }

      const updatedImage = await response.json();

      dispatch(updateImage(updatedImage));

      return updatedImage;
    } catch (error) {
      console.log("Error updating image", error);
    }
  };

export const deleteImageById = (imageId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/images/${imageId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Error deleting image");
    }
    dispatch(deleteImage(imageId));
  } catch (error) {
    console.log("Error deleting image", error);
  }
};

const initialState = {};

const imageReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_IMAGES:
      return {
        ...state,
        ...action.images.reduce(
          (obj, image) => ({ ...obj, [image.id]: image }),
          {}
        ),
      };
    case FETCH_ONE_IMAGE:
    case ADD_IMAGE:
    case UPDATE_IMAGE:
      return {
        ...state,
        [action.image.id]: action.image,
      };
    case DELETE_IMAGE:
      const newState = { ...state };
      delete newState[action.imageId];
      return newState;
    default:
      return state;
  }
};

export default imageReducer;

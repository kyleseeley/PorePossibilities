import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchOneBlogpostThunk,
  updateBlogpostThunk,
} from "../../store/blogposts";
import { useModal } from "../../context/Modal";
import "./UpdateBlogpostModal.css";

const UpdateBlogpostModal = ({ blogpostId, onClose }) => {
  const dispatch = useDispatch();
  const blogpost = useSelector(
    (state) => state.blogposts.blogposts[blogpostId - 1]
  );
  const [updatedTitle, setUpdatedTitle] = useState(blogpost?.title || "");
  const [updatedBlog, setUpdatedBlog] = useState(blogpost?.blog || "");

  const handleUpdate = async () => {
    try {
      await dispatch(
        updateBlogpostThunk(blogpostId, {
          title: updatedTitle,
          blog: updatedBlog,
        })
      );
      dispatch(fetchOneBlogpostThunk(blogpostId));
      onClose();
    } catch (error) {
      console.error("Error updating blog post", error);
    }
  };

  return (
    <div className="update-blogpost-modal">
      <h2 className="blogpost-heading">Update Blogpost</h2>
      <label className="blogpost-title" htmlFor="title">
        Title:{" "}
      </label>
      <input
        type="text"
        id="title"
        value={updatedTitle}
        onChange={(e) => setUpdatedTitle(e.target.value)}
      />

      <label className="blogpost-blog" htmlFor="blog">
        Blog:
      </label>
      <textarea
        id="blog"
        value={updatedBlog}
        onChange={(e) => setUpdatedBlog(e.target.value)}
      />

      <button onClick={handleUpdate}>Update</button>
      <button onClick={onClose}>Cancel</button>
    </div>
  );
};

export default UpdateBlogpostModal;

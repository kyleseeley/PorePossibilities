import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  fetchOneBlogpostThunk,
  fetchAllBlogpostsThunk,
  deleteBlogpostThunk,
  updateBlogpostThunk,
} from "../../store/blogposts";
// import { useModal } from "../../../context/Modal";
// import { NavLink } from "react-router-dom";
// import OpenModalButton from "../../OpenModalButton";
import UpdateBlogpostModal from "../UpdateBlogpostModal";
import { useModal } from "../../context/Modal";
import OpenModalButton from "../OpenModalButton";
import "./Blogposts.css";

const Blogposts = () => {
  const { blogpostId } = useParams();
  const blogpost = useSelector(
    (state) =>
      state.blogposts?.blogposts && state.blogposts.blogposts[blogpostId - 1]
  );
  console.log("Redux State:", blogpost);
  const user = useSelector((state) => state.session.user);
  const employee = user && user.employee;
  const dispatch = useDispatch();
  const { setModalContent, openModal } = useModal();
  //   const { closeModal } = useModal();
  //   const blogposts = useSelector((state) => state.blogposts.blogposts);

  useEffect(() => {
    dispatch(fetchAllBlogpostsThunk());
    dispatch(fetchOneBlogpostThunk(blogpostId));
  }, [dispatch, blogpostId]);

  useEffect(() => {
    console.log("Component re-rendered with blogpostId:", blogpostId);
    console.log("Redux state in useEffect:", blogpost);
  }, [blogpostId, blogpost]);

  // useEffect(() => {
  //   if (blogpostId) {
  //     console.log("one blogpost:", fetchOneBlogpostThunk(blogpostId));
  //     dispatch(fetchOneBlogpostThunk(blogpostId));
  //   }
  // }, [dispatch, blogpostId]);

  const handleDelete = async () => {
    try {
      await dispatch(deleteBlogpostThunk(blogpostId));
      // Redirect or navigate to another page after successful deletion
    } catch (error) {
      console.error("Error deleting blog post", error);
    }
  };

  const handleEditBlogpost = () => {
    // Open the modal with the UpdateBlogpostModal component
    setModalContent(
      <UpdateBlogpostModal
        blogpostId={blogpostId}
        onClose={() => setModalContent(null)}
      />
    );
  };

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="blogpost-page-container">
        <h2 className="blogpost-page-title">{blogpost?.title}</h2>
        <div className="blogpost-page-blog">{blogpost?.blog}</div>
      </div>
      {/* Conditional rendering of buttons based on user authorization */}
      {employee && employee.authorized && (
        <div>
          <button onClick={handleEditBlogpost}>Edit</button>
          <button onClick={handleDelete}>Delete</button>
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

export default Blogposts;

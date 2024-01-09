import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  fetchOneBlogpostThunk,
  fetchAllBlogpostsThunk,
} from "../../store/blogposts";
// import { useModal } from "../../../context/Modal";
// import { NavLink } from "react-router-dom";
// import OpenModalButton from "../../OpenModalButton";
import "./Blogposts.css";

const Blogposts = () => {
  const { blogpostId } = useParams();
  const blogpost = useSelector(
    (state) => state.blogposts.blogposts[blogpostId - 1]
  );
  console.log("blogpost", blogpost);
  const dispatch = useDispatch();
  //   const { closeModal } = useModal();
  //   const blogposts = useSelector((state) => state.blogposts.blogposts);

  useEffect(() => {
    console.log("Fetching blog post with ID:", blogpostId);
    dispatch(fetchAllBlogpostsThunk());
  }, [dispatch, blogpostId]);

  return (
    <div className="page-container">
      <div className="separator-line-container">
        <div className="separator-line" />
      </div>
      <div className="blogpost-page-container">
        <h2 className="blogpost-page-title">{blogpost?.title}</h2>
        <div className="blogpost-page-blog">{blogpost?.blog}</div>
      </div>
    </div>
  );
};

export default Blogposts;

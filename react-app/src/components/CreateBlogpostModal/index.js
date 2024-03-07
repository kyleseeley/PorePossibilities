import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  createBlogpostThunk,
  fetchAllBlogpostsThunk,
} from "../../store/blogposts";
import { useModal } from "../../context/Modal";
import "./CreateBlogpostModal.css";

const CreateBlogpostModal = ({ onClose }) => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.session.user);
  const employee = user && user.employee;
  const { setModalContent } = useModal();

  const [newTitle, setNewTitle] = useState("");
  const [newBlog, setNewBlog] = useState("");

  const handleCreate = async () => {
    try {
      const employeeId = employee.id;
      await dispatch(createBlogpostThunk({ title: newTitle, blog: newBlog }));
      await dispatch(fetchAllBlogpostsThunk());
      onClose();
    } catch (error) {
      console.error("Error creating blog post", error);
    }
  };

  return (
    <div className="create-blogpost-modal">
      <h2 className="create-blogpost-heading">Create Blogpost</h2>
      <label className="blogpost-title" htmlFor="newTitle">
        Title:
      </label>
      <input
        type="text"
        id="newTitle"
        value={newTitle}
        onChange={(e) => setNewTitle(e.target.value)}
      />

      <label className="create-blogpost-blog" htmlFor="newBlog">
        Blog:
      </label>
      <textarea
        className="create-text-area"
        id="newBlog"
        value={newBlog}
        onChange={(e) => setNewBlog(e.target.value)}
      />

      <button className="blogpost-create" onClick={handleCreate}>
        Create
      </button>
      <button className="blogpost-cancel" onClick={onClose}>
        Cancel
      </button>
    </div>
  );
};

export default CreateBlogpostModal;

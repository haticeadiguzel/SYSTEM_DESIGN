import React from "react";
import "./form.css";

export const Form = ({ userInput, onFormChange, onFormSubmit }) => {
  const handleChange = (event) => {
    onFormChange(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onFormSubmit();
  };

  return (
    <>
      <div className="thread-container">
        <form onSubmit={handleSubmit} className="thread-input-container">
          <input
            type="text"
            required
            value={userInput}
            onChange={handleChange}
            className="thread-input"
          ></input>
          <button type="submit" className="thread-button">
            Submit
          </button>
        </form>
      </div>
    </>
  );
};

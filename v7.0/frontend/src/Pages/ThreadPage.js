import React, { useState, useEffect } from "react";
import { Terminal } from "../Components/Terminal/terminal";
import { Form } from "../Components/Form/form";

export const ThreadPage = () => {
  const [thread, setThread] = useState([]);
  const [addThread, setAddThread] = useState("");

  useEffect(() => {
    fetch("/thread")
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => setThread(data));
  }, []);

  const handleFormChange = (inputValue) => {
    setAddThread(inputValue);
  };

  const handleFormSubmit = () => {
    fetch("/thread/create", {
      method: "POST",
      body: JSON.stringify({
        command: addThread,
      }),
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
      },
    })
      .then((response) => response.json())
      .then((responseData) => {
        getLatestThreads();
        setAddThread("");
      });
  };

  const getLatestThreads = () => {
    fetch("/thread")
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        setThread(data);
      });
  };

  return (
    <div>
      <Form
        userInput={addThread}
        onFormChange={handleFormChange}
        onFormSubmit={handleFormSubmit}
      />
      <Terminal listOfThreads={thread} />
    </div>
  );
};

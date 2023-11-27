import React, { useEffect, useState } from "react";
import "./terminal.css";

export const Terminal = ({ listOfThreads }) => {
  const [promptDirectory, setPromptDirectory] = useState("");

  useEffect(() => {
    fetch("/get_os")
      .then((response) => response.json())
      .then((data) => {
        setPromptDirectory(data.prompt_directory);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [listOfThreads]);

  return (
    <>
      <div className="terminal-container">
        <div className="terminal-output">
          {listOfThreads.map((thread) => {
            return (
              <ul key={thread.id}>
                <li>
                  {promptDirectory
                    ? `${promptDirectory} ${thread.command}`
                    : `>>> ${thread.command}`}
                </li>
                <li>{thread.output}</li>
              </ul>
            );
          })}
        </div>
      </div>
    </>
  );
};
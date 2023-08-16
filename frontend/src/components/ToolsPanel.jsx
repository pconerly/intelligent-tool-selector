import React, { useEffect, useState } from "react";
import ReactFlow, { Controls, Panel, NodeOrigin } from "reactflow";
import "./ToolsPanel.css";

import { shallow } from "zustand/shallow";

import useStore from "../App/store";

// import cn from "classnames";
// import * as styles from "./ToolsPanel.module.scss";
// console.log("styles", styles);

const selector = (state) => ({
  getTools: state.getTools,
  toolsData: state.toolsData,
  loading: state.loading,
  sendPrompt: state.sendPrompt,
});

export const ToolsPanel = () => {
  const { getTools, toolsData, loading, sendPrompt } = useStore(
    selector,
    shallow
  );
  const [error, setError] = useState(null);

  useEffect(() => {
    getTools(); // Call the getTools action when the component is mounted
  }, [getTools]);

  const handleSubmit = (event) => {
    event.preventDefault();
    const task = event.target.task.value.trim();
    if (task.length < 300) {
      setError(
        `Please enter a task description at least 300 characters long. Current length: ${task.length}`
      );
    }
    sendPrompt(task);

    // Here, you'd typically dispatch an action or make an API call
    // to get the tools for the given task.
  };

  let extraProps = {};
  if (loading) {
    extraProps = {
      disabled: loading,
    };
  }

  return (
    <Panel position="left" className="control-panel">
      <h2 className="sm-mg">Intelligent Tool Selector</h2>
      <form onSubmit={handleSubmit}>
        <div className="sm-mg">
          <label>
            What task do you need help finding tools for?
            <br />
            <textarea
              className="sm-mg"
              name="task"
              rows="4"
              cols="30"
              {...extraProps}
            ></textarea>
            {error && <div className="sm-mg error-msg">{error}</div>}
          </label>
        </div>
        <div className="sm-mg">
          <button className="submit-btn" type="submit" {...extraProps}>
            Search
          </button>
        </div>
      </form>
      <div className="sm-mg">
        <h3>Tools Available</h3>
        {toolsData &&
          toolsData.map((tool) => (
            <div key={tool.name} className="sm-mg">
              <strong>{tool.name}</strong>
              <p>{tool.description}</p>
              <p>Logged in: {tool.loggedIn ? "True" : "False"}</p>
              <hr />
            </div>
          ))}
      </div>
    </Panel>
  );
};

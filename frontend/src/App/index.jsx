import React from "react";
import ReactFlow, { Controls, Panel, NodeOrigin } from "reactflow";
import { shallow } from "zustand/shallow";

import useStore from "./store";

import { ToolsPanel } from "../components/ToolsPanel";

// we have to import the React Flow styles for it to work
import "reactflow/dist/style.css";

const selector = (state) => ({
  nodes: state.nodes,
  edges: state.edges,
  onNodesChange: state.onNodesChange,
  onEdgesChange: state.onEdgesChange,
});

// this places the node origin in the center of a node
const nodeOrigin = [0.5, 0.5];

function Flow() {
  // whenever you use multiple values, you should use shallow to make sure the component only re-renders when one of the values changes
  const { nodes, edges, onNodesChange, onEdgesChange } = useStore(
    selector,
    shallow
  );

  // should add a container
  // should add a sidebar with a list of tools
  // should add a input box for a new prompt

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      nodeOrigin={nodeOrigin}
      fitView
    >
      <Controls showInteractive={false} position="bottom-right" />
      <ToolsPanel />
    </ReactFlow>
  );
}

export default Flow;

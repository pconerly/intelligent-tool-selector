import {
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  OnNodesChange,
  OnEdgesChange,
  applyNodeChanges,
  applyEdgeChanges,
} from "reactflow";
import { create } from "zustand";
import { nanoid } from "nanoid";

const kFetchPrompt = `http://localhost:8000/prompt`;
const kGetTools = `http://localhost:8000/tools`;

const kRootNode = {
  id: "root",
  type: "default",
  data: { label: "React Flow Mind Map" },
  position: { x: 0, y: 0 },
};

const useStore = create((set, get) => ({
  nodes: [
    {
      id: "root",
      type: "default",
      data: { label: "React Flow Mind Map" },
      position: { x: 0, y: 0 },
    },
  ],
  edges: [],

  data: null,
  loading: false,
  error: null,

  toolsData: null,

  onNodesChange: (changes) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes),
    });
  },
  onEdgesChange: (changes) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
  },

  getTools: async () => {
    const response = await fetch(kGetTools);
    const toolsData = await response.json();

    set({ toolsData });
  },
  addChildNode: (parentNode, position, label) => {
    const newNode = {
      id: nanoid(),
      type: "default",
      data: { label },
      position,
      parentNode: parentNode.id,
    };

    const newEdge = {
      id: nanoid(),
      source: parentNode.id,
      target: newNode.id,
    };

    set({
      nodes: [...get().nodes, newNode],
      edges: [...get().edges, newEdge],
    });
  },
  sendPrompt: async (prompt) => {
    console.log("send prompt", prompt);
    set({ loading: true, error: null });

    try {
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt,
        }),
      };

      let nodes = [{ ...kRootNode, data: { label: prompt } }];

      set({ nodes: nodes, edges: [] });
      const response = await fetch(kFetchPrompt, requestOptions);
      const data = await response.json();
      console.log("data", data);
      set({ data, loading: false, error: null });

      // filter through tools
      // add children
      let relevantTools = get().toolsData.filter((tool) => {
        return data.recommended_tools.includes(tool.name);
      });

      // move y down 300 pixels
      const newY = 150;
      const deltaX = 200;
      const totalWidth = relevantTools.length * deltaX;
      const offsetX = 150;
      const startX = -totalWidth / 2 + offsetX;
      const addChildNode = get().addChildNode;

      relevantTools.forEach((tool, i) => {
        addChildNode(nodes[0], { x: startX + deltaX * i, y: newY }, tool.name);
      });
    } catch (error) {
      // If an error occurs, store the error message and reset loading state
      console.log("error", error);
      set({ error: error.message, loading: false });
    }
  },
}));

export default useStore;

// app/dashboard/network-graph/page.tsx
"use client";
import React, { useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Graph from "./graph_build";
const test_graph = {
  directed: false,
  multigraph: false,
  graph: {},
  nodes: [
    {
      id: 1,
      cluster: 0,
    },
    {
      id: 2,
      cluster: 1,
    },
    {
      id: 3,
      cluster: 2,
    },
    {
      id: 4,
      cluster: 3,
    },
    {
      id: 5,
      cluster: 8,
    },
    {
      id: 6,
      cluster: 5,
    },
    {
      id: 7,
      cluster: 6,
    },
    {
      id: 8,
      cluster: 5,
    },
    {
      id: 9,
      cluster: 8,
    },
    {
      id: 10,
      cluster: 7,
    },
    {
      id: 11,
      cluster: 5,
    },
    {
      id: 12,
      cluster: 8,
    },
    {
      id: 13,
      cluster: 4,
    },
    {
      id: 14,
      cluster: 5,
    },
    {
      id: 15,
      cluster: 8,
    },
    {
      id: 16,
      cluster: 8,
    },
  ],
  links: [
    {
      weight: 0.60986293074805,
      source: 5,
      target: 9,
    },
    {
      weight: 0.5344845631658858,
      source: 6,
      target: 14,
    },
    {
      weight: 0.5822896106454868,
      source: 8,
      target: 11,
    },
    {
      weight: 0.553649879230966,
      source: 8,
      target: 14,
    },
    {
      weight: 0.5969871879776599,
      source: 8,
      target: 16,
    },
    {
      weight: 0.5582595384961634,
      source: 9,
      target: 12,
    },
    {
      weight: 0.5770991460840533,
      source: 9,
      target: 14,
    },
    {
      weight: 0.5609148080345867,
      source: 9,
      target: 15,
    },
    {
      weight: 0.5485500967286061,
      source: 9,
      target: 16,
    },
    {
      weight: 0.5162470202854553,
      source: 11,
      target: 14,
    },
    {
      weight: 0.5289756798737117,
      source: 12,
      target: 14,
    },
    {
      weight: 0.5242273294063868,
      source: 12,
      target: 16,
    },
    {
      weight: 0.6308588050972438,
      source: 14,
      target: 16,
    },
  ],
  clusters: {
    Clusters: {
      "1": 0,
      "2": 1,
      "3": 2,
      "4": 3,
      "5": 8,
      "6": 5,
      "7": 6,
      "8": 5,
      "9": 8,
      "10": 7,
      "11": 5,
      "12": 8,
      "13": 4,
      "14": 5,
      "15": 8,
      "16": 8,
    },
  },
};
const NetworkGraph = () => {
  const [selectedOption, setSelectedOption] = useState("overall");
  const [graph, setGraph] = useState(test_graph);

  const handleTypeChange = async (value: string) => {
    console.log(value);
    const res = await fetch(`http://127.0.0.1:5000/graph/${value}`);
    const data = await res.json();
    console.log(data);
    setGraph((_) => data["Graph_Data"]);
  };

  return (
    <div>
      <div>NetworkGraph</div>
      <Select onValueChange={handleTypeChange}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Graph Parameter" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="overall">Overall</SelectItem>
          <SelectItem value="tag">Tag</SelectItem>
        </SelectContent>
      </Select>
      <div className="grid">{graph && <Graph graph={graph} />}</div>
    </div>
  );
};

export default NetworkGraph;

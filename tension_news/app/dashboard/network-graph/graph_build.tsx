"use client";

import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const Graph = ({ width = 1000, height = 600, graph }) => {
  const svgRef = useRef(null);

  useEffect(() => {
    // if (svgRef.current.children.length > 0)
    //   svgRef.current?.children.forEach((i) => svgRef.current.removeChild(i));
    const svg = d3.select(svgRef.current);

    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
    const thicknessScale = d3
      .scaleLinear()
      .domain([
        d3.min(graph.links, (d) => d.weight),
        d3.max(graph.links, (d) => d.weight),
      ])
      .range([1, 5]);

    const simulation = d3
      .forceSimulation(graph.nodes)
      .force(
        "link",
        d3
          .forceLink()
          .id((d) => d.id)
          .links(graph.links),
      )
      .force(
        "charge",
        d3.forceManyBody().strength(-100), // Adjust strength to increase spacing between nodes
      )
      .force("center", d3.forceCenter(width / 2, height / 2))
      .on("tick", ticked);

    const link = svg
      .append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(graph.links)
      .enter()
      .append("line")
      .attr("stroke-width", (d) => thicknessScale(d.weight))
      .style("stroke", "#999")
      .style("stroke-opacity", 0.6);

    const node = svg
      .append("g")
      .attr("class", "nodes")
      .selectAll("circle")
      .data(graph.nodes)
      .enter()
      .append("circle")
      .attr("r", 10)
      .attr("fill", (d) => colorScale(d.cluster))
      .call(
        d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended),
      );

    const nodeText = svg
      .append("g")
      .attr("class", "node-labels")
      .selectAll("text")
      .data(graph.nodes)
      .enter()
      .append("text")
      .attr("class", "node-id")
      .text((d) => d.title)
      .style("font-size", "10px")
      .style("text-anchor", "middle")
      .style("dominant-baseline", "central");

    function ticked() {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("transform", (d) => `translate(${d.x},${d.y})`);

      nodeText.attr("transform", (d) => `translate(${d.x},${d.y})`);
    }

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [graph, width, height]);

  return <svg ref={svgRef} width={width} height={height}></svg>;
};

export default Graph;

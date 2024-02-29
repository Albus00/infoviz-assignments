import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

// Declare the global data variable
let data1;
let data2;
let leftEpisodes = [];
let rightEpisodes = [];

let episodeSelector1 = d3.select("#episodeSelector1")
let episodeSelector2 = d3.select("#episodeSelector2")

// Declare the chart dimensions and margins.
let menuHeight = document.getElementById("menu").offsetHeight;
let width = window.innerWidth / 2 - 5;
let height = window.innerHeight - 20 - menuHeight;

// Declare the layout
let layout = d3.forceSimulation()

// Create a function that fetches the links from a selected episode
async function fetchEpisode(episode) {
  return await fetch('./starwars-interactions/starwars-episode-' + episode + '-interactions-allCharacters.json')
    .then(response => response.json())
    .then(data => {
      data.links.forEach(link => {
        link.source = data.nodes[link.source];
        link.target = data.nodes[link.target];
      });
      return data;
    }
    );
}

//get checked episodes from the first selector
episodeSelector1.on("change", (event) => {
  let checkedEpisodes = [];
  d3.selectAll(".l-episode").each(function (d) {
    let cb = d3.select(this);
    if (cb.property("checked")) {
      checkedEpisodes.push(cb.property("value"));
    }
  });
  data1 = undefined;
  if (checkedEpisodes.length === 0) {
    // No episodes are selected
    svg1.selectAll("*").remove(); // Clear the svg1
    return
  }
  leftEpisodes = checkedEpisodes;
  getEpisode("left", leftEpisodes);
});

//get checked episodes from the second selector
episodeSelector2.on("change", (event) => {
  let checkedEpisodes = [];
  d3.selectAll(".r-episode").each(function (d) {
    let cb = d3.select(this);
    if (cb.property("checked")) {
      checkedEpisodes.push(cb.property("value"));
    }
  });
  data2 = undefined;
  if (checkedEpisodes.length === 0) {
    // No episodes are selected
    svg2.selectAll("*").remove(); // Clear the svg1
    return
  }
  rightEpisodes = checkedEpisodes;
  getEpisode("right", rightEpisodes);
});

// Change the window width and height when the window is resized
window.onresize = function () {
  width = window.innerWidth / 2 - 5;
  height = window.innerHeight - 20 - menuHeight;
  svg1.attr("width", width / 2).attr("height", height);
  svg2.attr("width", width / 2).attr("height", height);

  // Update the layout
  updateCanvas(data1, svg1);
  updateCanvas(data2, svg2);

};

// Import data from selected episode
function getEpisode(field, episodes) {
  let dataFetch = new Promise((resolve, reject) => {
    episodes.forEach(async (episode, index) => {
      await fetchEpisode(episode).then(episode => {
        field === "left" ?
          data1 = updateDataset(data1, episode) :
          data2 = updateDataset(data2, episode)
      });
      // Check if the last episode has been fetched then resolve the promise
      index == episodes.length - 1 ? resolve() : null;
    })
  });

  dataFetch.then(() => {
    field === "left" ? updateCanvas(data1, svg1) : updateCanvas(data2, svg2);
  });
}

// Add new data to the dataset
function updateDataset(data, addedData) {
  // Create a copy of the data
  let addedNodes = addedData.nodes;
  let addedLinks = addedData.links;

  // Check if this is the first dataset to be added
  if (data === undefined) {
    return addedData;
  }
  addedNodes.forEach(addNode => {
    data.nodes.forEach(node => {
      // Check if the character already exists in the dataset
      if (node.name == addNode.name) {
        // Update edge value of the character
        node.value += addNode.value;

        // Update the links to the character
        addedLinks.forEach(link => {
          if (link.source.name === addNode.name) {
            link.source = node;
          }
          else if (link.target.name === addNode.name) {
            link.target = node;
          }
        });
        // Remove the duplicate node from the addedData
        addedNodes = addedNodes.filter(node => node.name !== addNode.name);
      }
    });
  });

  // Add the new and filtered data to the dataset
  data.nodes = data.nodes.concat(addedNodes);
  data.links = data.links.concat(addedLinks);
  return data;
}

// Function that turns a string into lowercase and replaces all spaces with -
function formatClassName(str) {
  return str.toLowerCase().replace(/ /g, "-");
}

// Create a function that checks if name is in dataset
function checkName(name, data) {
  let result = false;
  if (data === undefined) {
    return result;
  }
  data.nodes.forEach(node => {
    if (node.name === name) {
      result = node;
    }
  });
  return result;
}

// Create a function that finds the node in the data set and returns which characters it interacts with
function findInteractions(node, data) {
  let interactions = [];
  data.links.forEach(link => {
    if (link.source.name === node.name) {
      interactions.push([link.target.name, link.target.value]);
    }
    else if (link.target.name === node.name) {
      interactions.push([link.source.name, link.source.value]);
    }
  });
  return interactions;
}

// Write a function that highlights the node from another network when hovering over a node, based on the class name
function highlightNode(nodeName, toHighlight) {
  let className = formatClassName(nodeName);
  let svgArray = [svg1, svg2];
  if (toHighlight) {
    // Highlight the links connected to the node
    highlightLinks(nodeName, true);

    // Give the node a border and make it bigger
    svgArray.forEach(svg => {
      svg.selectAll("." + className)
        .attr("stroke", "black")
        .attr("stroke-width", 2)
        .attr("r", 15);
    });
  }
  else {
    highlightLinks(nodeName, false);

    svgArray.forEach(svg => {
      svg.selectAll("." + className)
        .attr("stroke", "none")
        .attr("r", 10);
    });
  }
}

// Function that highlights the links connected to a node
function highlightLinks(nodeName, toHighlight) {
  const highlight = (svg, data) => {
    data.links.forEach(link => {
      if (link.source.name === nodeName || link.target.name === nodeName) {
        // Match the class name format when searching for the lines
        const className = ".link_" + formatClassName(link.source.name) + "_" + formatClassName(link.target.name);
        svg.selectAll(className)
          .attr("stroke", toHighlight ? "red" : "black")
          .attr("stroke-width", toHighlight ? 2 : 1);
      }
    });
  };

  // Highlight the links in both networks
  data1 !== undefined ? highlight(svg1, data1) : null;
  data2 !== undefined ? highlight(svg2, data2) : null;
}

function generateTooltips(node) {
  const generateTooltipsContent = (char, interactions) => {
    let tooltipContent = "<div><h3>" + char.name + "</h3><h3>" + char.value + "</h3></div>";
    interactions.forEach(interaction => {
      tooltipContent += "<div><p>" + interaction[0] + "</p><p>" + interaction[1] + "</p></div>";
    });
    return tooltipContent;
  }

  // Left network
  let char;
  let tooltipHeight = 5;
  let tooltipContainer = document.getElementById("tooltips-left");
  tooltipContainer.innerHTML = "";
  if (char = checkName(node.name, data1)) {
    let interactions = findInteractions(char, data1);
    tooltipContainer.innerHTML = generateTooltipsContent(char, interactions);
    tooltipHeight += interactions.length * 0.8;
  }
  tooltipContainer.style.height = tooltipHeight + "rem";

  // Right network
  tooltipHeight = 5;
  tooltipContainer = document.getElementById("tooltips-right");
  tooltipContainer.innerHTML = "";
  if (char = checkName(node.name, data2)) {
    let interactions = findInteractions(char, data2);
    tooltipContainer.innerHTML = generateTooltipsContent(char, interactions);
    tooltipHeight += interactions.length * 0.8;
  }
  tooltipContainer.style.height = tooltipHeight + "rem";
}


// Add labels to the nodes
function createLabels(nodes_data, svg) {
  return svg.selectAll(null)
    .data(nodes_data)
    .enter()
    .append('text')
    .attr('font-size', '0.6em')
    .attr("dy", ".35em")
    .attr("dx", "15")
    .text(function (d) { return d.name; });
}

// Create the node circles
function createNodes(nodes_data, svg) {
  return svg.selectAll(".node")
    .data(nodes_data)
    .enter().append("circle")
    .attr("class", (d) => "node " + formatClassName(d.name))
    .attr("r", 10)
    .attr("fill", (d) => d.colour)
    // Add onclick that sends the node name to the console
    .on("mouseover", (event, d) => highlightNode(d.name, true))
    .on("mouseout", (event, d) => highlightNode(d.name, false))
    .on("click", (event, d) => generateTooltips(d));
}

// Create the link lines
function createLinks(links_data, svg) {
  return svg.selectAll(".link")
    .data(links_data)
    .enter().append("line")
    .attr("class", (d) => "link_" + formatClassName(d.source.name) + "_" + formatClassName(d.target.name))
    .attr("stroke", "black");
}

function updateCanvas(data, svg) {
  // Clear the svg
  svg.selectAll("*").remove();

  // Define the data for the nodes and links
  let nodes_data = data.nodes
  let links_data = data.links

  // Create the graph layout
  layout = d3.forceSimulation(nodes_data)
    .force("charge", d3.forceManyBody().strength(-height / 2))
    .force("link", d3.forceLink(links_data).distance(100))
    .force("center", d3.forceCenter().x(width / 2).y(height / 2))
    .restart();

  // Create the node circles and link lines
  let link = createLinks(links_data, svg);
  let node = createNodes(nodes_data, svg);

  // Call the function to add labels to the nodes (and make it global)
  var labels = createLabels(nodes_data, svg);

  // Update the positions of the nodes, links, and labels on each tick of the simulation
  layout.on("tick", function () {
    link.attr("x1", function (d) { return d.source.x; })
      .attr("y1", function (d) { return d.source.y; })
      .attr("x2", function (d) { return d.target.x; })
      .attr("y2", function (d) { return d.target.y; });

    // Update the node and make it impossible to go out of the svg area
    node.attr("cx", function (d) { return d.x = Math.max(10, Math.min(width - 20, d.x)); })
      .attr("cy", function (d) { return d.y = Math.max(10, Math.min(height - 10, d.y)); });

    // Update the label and make it switch side if node is at the end of the right half
    labels.attr("x", function (d) { return (d.x < (width / 8 * 7)) ? d.x : (d.x - 80); })
      .attr("y", function (d) { return d.y; });
  });

}

// Create the SVG containers for the two node network
let svg1 = d3.create("svg")
  .attr("width", width)
  .attr("height", height);
let svg2 = svg1.clone(true);

// Append the SVG element.
document.getElementById("container").append(svg1.node());
document.getElementById("container").append(svg2.node());
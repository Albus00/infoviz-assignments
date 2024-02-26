import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

// Declare the global data variable
let data1;
let data2;
let leftEpisodes = [];
let rightEpisodes = [];

let episodeSelector1 = d3.select("#episodeSelector1")
let episodeSelector2 = d3.select("#episodeSelector2")

//get checked episodes and update graph
episodeSelector1.on("change", (event) => {
  let checkedEpisodes = [];
  d3.selectAll(".l-episode").each(function (d) {
    let cb = d3.select(this);
    if (cb.property("checked")) {
      checkedEpisodes.push(cb.property("value"));
    }
  });
  leftEpisodes = checkedEpisodes;
  getEpisode("left", leftEpisodes);
});

episodeSelector2.on("change", (event) => {
  let checkedEpisodes = [];
  d3.selectAll("input").each(function (d) {
    let cb = d3.select(this);
    if (cb.property("checked")) {
      checkedEpisodes.push(cb.property("value"));
    }
  });
  updateEpisodes("right", checkedEpisodes);
});

// Import data from selected episode
async function getEpisode(field, episodes) {
  episodes.forEach(async (episode) => {
    await import('./starwars-interactions/starwars-episode-' + episode + '-interactions-allCharacters.json', {
      assert: { type: 'json' }
    }).then(({ default: data }) => {
      if (field === "left") {
        data1 = updateDataset(data1, data);
        console.log("1");
      }
      else if (field === "right") {
        updateDataset(data2, data);
      }
    });
  });
  if (field === "left") {
    svg1.selectAll("*").remove(); // Clear the svg1
    console.log("1");
    updateCanvas1(data1);         // Update the dataset for svg1
  } else if (field === "right") {
    svg2.selectAll("*").remove(); // Clear the svg2
    updateCanvas2(data2);         // Update the dataset for svg2
  }
}

// Add new data to the dataset
function updateDataset(data, addedData) {
  if (data === undefined) {
    return addedData;
  }
  addedData.nodes.forEach(node => {
    if (checkName(node.name, data)) {
      // Character already exists in the dataset
      data.nodes.forEach(dataNode => {
        if (dataNode.name === node.name) {
          dataNode.value += node.value;
        }
      });

      // Update the links in the addedData
      addedData.links.forEach(link => {
        if (link.source.name === node.name) {
          link.source = node.name;
        }
        else if (link.target.name === node.name) {
          link.target += node.name;
        }
      });
    }
  });
}

// Create a function that finds all the links connected to a node
function findLinks(nodeName, data) {
  let links = [];
  data.links.forEach(link => {
    if (link.source.name === nodeName || link.target.name === nodeName) {
      links.push(link);
    }
  });
  return links;
}

// Write a function that highlights the node from another network when hovering over a node, based on the class name
function highlightNode(nodeName, toHighlight) {
  let className = formatClassName(nodeName);
  if (toHighlight) {
    // Highlight the links connected to the node
    highlightLinks(nodeName, true);

    // Give the node a border and make it bigger
    svg1.selectAll("." + className)
      .attr("stroke", "black")
      .attr("stroke-width", 2)
      .attr("r", 15);

    svg2.selectAll("." + className)
      .attr("stroke", "black")
      .attr("stroke-width", 2)
      .attr("r", 15);
  }
  else {
    highlightLinks(nodeName, false);

    // Remove the border and make the node smaller
    svg1.selectAll("." + className)
      .attr("stroke", "none")
      .attr("r", 10);

    svg2.selectAll("." + className)
      .attr("stroke", "none")
      .attr("r", 10);
  }
}

// Create a function that highlights the links connected to a node
function highlightLinks(nodeName, toHighlight) {
  // Loop through each link
  data1.links.forEach(link => {
    // Check if the link is connected to the specified node
    if (link.source.name === nodeName || link.target.name === nodeName) {
      console.log("link: ", link.source.name, nodeName);
      // go through all the classes that contains the words link_ and the source and target names
      let className = ".link_" + formatClassName(link.source.name) + "_" + formatClassName(link.target.name);
      if (toHighlight) {
        // Highlight the link
        svg1.selectAll(className)
          .attr("stroke", "red")
          .attr("stroke-width", 2);
      }
      else {
        // Remove the highlight from the link
        svg1.selectAll(className)
          .attr("stroke", "black")
          .attr("stroke-width", 1);
      }
    }
  });
  // Loop through each link
  data2.links.forEach(link => {
    // Check if the link is connected to the specified node
    if (link.source.name === nodeName || link.target.name === nodeName) {
      console.log("link: ", link.source.name, nodeName);
      // go through all the classes that contains the words link_ and the source and target names
      let className = ".link_" + formatClassName(link.source.name) + "_" + formatClassName(link.target.name);
      if (toHighlight) {
        // Highlight the link
        svg2.selectAll(className)
          .attr("stroke", "red")
          .attr("stroke-width", 2);
      }
      else {
        // Remove the highlight from the link
        svg2.selectAll(className)
          .attr("stroke", "black")
          .attr("stroke-width", 1);
      }
    }
  });
}

// Create a function that turns a string into lowercase and replaces all spaces with -
function formatClassName(str) {
  return str.toLowerCase().replace(/ /g, "-");
}

// Create a function that finds the node in the data set and returns which characters it interacts with
function findInteractions(node, data) {
  console.log("node: ", node);
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

// Create a function that checks if name is in dataset
function checkName(name, data) {
  let found = false;
  data.nodes.forEach(node => {
    if (node.name === name) {
      found = true;
    }
  });
  return found;
}

function generateTooltips(node) {
  // Left network
  let height = 5;
  let leftTooltip = document.getElementById("tooltips-left");
  if (checkName(node.name, data1)) {
    let interactions = findInteractions(node, data1);
    leftTooltip.innerHTML = "<div><h3>" + node.name + "</h3><h3>" + node.value + "</h3></div>";
    interactions.forEach(interaction => {
      leftTooltip.innerHTML += "<div><p>" + interaction[0] + "</p><p>" + interaction[1] + "</p></div>";
      height += 0.7;
      console.log("height: ", height);
    });
  }
  else {
    leftTooltip.innerHTML = "";
  }
  leftTooltip.style.height = height + "rem";

  // Right network
  height = 5;
  let rightTooltip = document.getElementById("tooltips-right");
  if (checkName(node.name, data2)) {
    let interactions = findInteractions(node, data2);
    rightTooltip.innerHTML = "<div><h3>" + node.name + "</h3><h3>" + node.value + "</h3></div>";
    interactions.forEach(interaction => {
      rightTooltip.innerHTML += "<div><p>" + interaction[0] + "</p><p>" + interaction[1] + "</p></div>";
      height += 0.7;
    });
  }
  else {
    rightTooltip.innerHTML = "";
  }
  rightTooltip.style.height = height + "rem";
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
function createLinks(links_data, svg, isHighlighted) {
  return svg.selectAll(".link")
    .data(links_data)
    .enter().append("line")
    .attr("class", (d) => "link_" + formatClassName(d.source.name) + "_" + formatClassName(d.target.name))
    .attr("stroke", "black");
}

// Declare the chart dimensions and margins.
let menuHeight = document.getElementById("menu").offsetHeight;
let width = window.innerWidth / 2 - 5;
let height = window.innerHeight - 20 - menuHeight;

// Declare the layout
let layout, layout2;



// Change the window width and height when the window is resized
window.onresize = function () {
  width = window.innerWidth / 2 - 5;
  height = window.innerHeight - 20 - menuHeight;
  svg1.attr("width", width / 2).attr("height", height);
  svg2.attr("width", width / 2).attr("height", height);

  // Change the layout
  layout
    .force("center", d3.forceCenter().x(width / 2).y(height / 2))
    .restart();
  layout2
    .force("center", d3.forceCenter().x(width / 2).y(height / 2))
    .restart();

};

//#region SVG1
// Create the SVG container for the first node network
let svg1 = d3.create("svg")
  .attr("width", width)
  .attr("height", height);

function updateCanvas1(data) {
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
  let link = createLinks(links_data, svg1);
  let node = createNodes(nodes_data, svg1);

  // Call the function to add labels to the nodes (and make it global)
  var labels = createLabels(nodes_data, svg1);

  // Update the positions of the nodes, links, and labels on each tick of the simulation
  layout.on("tick", function () {
    link.attr("x1", function (d) { return d.source.x; })
      .attr("y1", function (d) { return d.source.y; })
      .attr("x2", function (d) { return d.target.x; })
      .attr("y2", function (d) { return d.target.y; });

    // Update the node and make it impossible to go out of the svg area
    node.attr("cx", function (d) { return d.x = Math.max(10, Math.min(width - 50, d.x)); })
      .attr("cy", function (d) { return d.y = Math.max(10, Math.min(height - 10, d.y)); });

    // Update the label and make it switch side if node is at the end of the right half
    labels.attr("x", function (d) { return (d.x < (width / 8 * 7)) ? d.x : (d.x - 80); })
      .attr("y", function (d) { return d.y; });
  });
}

// Create another SVG container for the second node network
let svg2 = d3.create("svg")
  .attr("width", width)
  .attr("height", height);

function updateCanvas2(data) {
  // Define the data for the second set of nodes and links
  let nodes_data = data.nodes;
  let links_data = data.links;

  // Create the second graph layout
  layout2 = d3.forceSimulation(nodes_data)
    .force("charge", d3.forceManyBody().strength(-height / 2))
    .force("link", d3.forceLink(links_data).distance(100))
    .force("center", d3.forceCenter().x(width / 2).y(height / 2))
    .restart();

  // Call the function to create the links for svg2
  let link = createLinks(links_data, svg2);

  // Create the second node circles
  let node = createNodes(nodes_data, svg2);

  // Add labels to the second nodes
  let labels = createLabels(nodes_data, svg2)

  // Update the positions of the nodes, links, and labels on each tick of the simulation
  layout2.on("tick", function () {
    link.attr("x1", function (d) { return d.source.x; })
      .attr("y1", function (d) { return d.source.y; })
      .attr("x2", function (d) { return d.target.x; })
      .attr("y2", function (d) { return d.target.y; });

    // Update the node and make it impossible to go out of the svg area
    node.attr("cx", function (d) { return d.x = Math.max(10, Math.min(width * 2 - 50, d.x)); })
      .attr("cy", function (d) { return d.y = Math.max(10, Math.min(height - 10, d.y)); });

    // Update the label and make it switch side if node is at the end of the right half
    labels.attr("x", function (d) { return (d.x < (width / 8 * 7)) ? d.x : (d.x - 80); })
      .attr("y", function (d) { return d.y; });
  });
}

//#endregion

// Append the SVG element.
document.getElementById("container").append(svg1.node());
document.getElementById("container").append(svg2.node());

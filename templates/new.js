var trace = {
x: ["Brown", "Brown", "Brown", "Brown", "Brown",
"Brown", "Brown", "Brown", "Green", "Green",
"Green", "Green", "Green", "Blue", "Blue",
"Blue", "Blue", "Blue", "Blue"],
y: [26.8, 27.9, 23.7, 25, 26.3, 24.8,
25.7, 24.5, 26.4, 24.2, 28, 26.9,
29.1, 25.7, 27.2, 29.9, 28.5, 29.4, 28.3],
type: "bar"
};
// Create the data array for our plot
var data = [trace];
// Define our plot layout
Plotly.newPlot("bar-plot", data);

$(document).ready(function () {
    // Define the API endpoint for fetching region data
    var apiEndpoint = "https://psgc.gitlab.io/api";

// Function to display region data in the HTML
function displayRegionData(data) {
    // Assuming there is a container with id "regionDataContainer" in your HTML
    var container = $("#regionDataContainer");

    // Clear any existing content in the container
    container.empty();

    // Check if data is an array
    if (Array.isArray(data)) {
        // Log the data to the console for verification
        console.log("Data:", data);

        // Iterate through the data and log the name property to the console
        data.forEach(function (region) {
            console.log("Region Name:", region.name);

            var regionHtml = `
                <div>
                    <p>Region: ${region.name}</p>
                </div>
                <hr>
            `;
            container.append(regionHtml);
        });
    } else {
        // Display a message if there is no data
        container.append("<p>No region data available.</p>");
    }
}
// Function to fetch and display region data
function fetchRegionData() {
    $.ajax({
        type: "GET",
        url: 'https://psgc.gitlab.io/api/island-groups/luzon/regions.json',
        success: function (response) {
            // Log the entire response to the console for inspection
            console.log(response);

            // Handle the successful response
            displayRegionData(response.data);
        },
        error: function (error) {
            // Handle the error
            console.error("Error fetching region data:", error);
        }
    });
}
    // Function to fetch and display data when the button is clicked
    window.fetchAndDisplayData = function () {
        fetchRegionData();
    };

    // Call the fetchRegionData function on page load
    fetchRegionData();
});

$(document).ready(function () {
    var apiEndpoint = "/householdprofiles";
    function fetchHouseholdData() {
        $.ajax({
            type: "GET",
            url: 'http://127.0.0.1:8000/householdprofiles/',
            success: function (response) {
                displayHouseholdData(response.data);
            },
            error: function (error) {
                console.error("Error fetching household data:", error);
            }
        });
    }
//display household data
function displayHouseholdData(data) {
    var container = $("#householdDataContainer");
    container.empty();

    if (data.length > 0) {
        data.forEach(function (household) {
            var householdHtml = `
                <div>
                    <p>Street: ${household.street}</p>
                    <p>Lot: ${household.lot}</p>
                    <!-- Add more fields as needed -->

                    <button type="button" onclick="deleteHousehold('${household.id}')">Delete</button>
                </div>
                <hr>
            `;
            container.append(householdHtml);
        });
    } else {
        container.append("<p>No household data available.</p>");
    }
}


    // Function to fetch and display data when the button is clicked
    window.fetchAndDisplayData = function () {
        fetchHouseholdData();
    };

    // Call the fetchHouseholdData function on page load
    fetchHouseholdData();
});

// ADD -----------------------------------------
    function submitHouseholdData(data) {
        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/householdprofiles/',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            success: function (response) {
                console.log("Successfully added household:", response.data);
            },
            error: function (error) {
                console.error("Error adding household data:", error);
            }
        });
    }
    // Function to handle form submission
    function handleFormSubmission() {
        var streetValue = $("#street").val();
        var lotValue = $("#lot").val();

        var householdData = {
            street: streetValue,
            lot: lotValue
        };

        submitHouseholdData(householdData);
    }

    // Attach form submission to the button click event
    $("#submitBtn").on("click", function () {
        handleFormSubmission();
    });
// DELETE---------------------------------------

function deleteHousehold(id) {
    var confirmDelete = confirm("Are you sure you want to delete this household?");
    if (confirmDelete) {
        $.ajax({
            type: "DELETE",
            url: `http://127.0.0.1:8000/householdprofiles/${id}`,
            success: function (response) {
                // Remove the deleted household from the UI
                $(`#${id}`).remove();
            },
            error: function (error) {
                console.error("Error deleting household data:", error);
            }
        });
    }
}

//ADD HOUSEHOLD---------------------------------------------

// Function to submit the form
function submitForm() {
    // Serialize the form data
    var formData = $("#householdForm").serializeArray();

    // Convert the serialized form data to a JSON object
    var jsonData = {};
    $.each(formData, function(index, field){
        jsonData[field.name] = field.value;
    });

  // Send a POST request
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/householdprofiles/",
            contentType: "application/json",
            data: JSON.stringify(jsonData),
            success: function (response) {
                // Handle the successful response
                fetchHouseholdData();
            },
            error: function (error) {
                // Log the error response text for debugging
                console.error("Error submitting form:", error.responseText);
            }
        });
    }

//UPDATE

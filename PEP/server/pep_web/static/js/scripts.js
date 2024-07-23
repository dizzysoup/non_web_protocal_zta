// Get the modal
var modal = document.getElementById("addHostModal");

// Get the button that opens the modal
var btn = document.getElementById("addHostButton");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("btn-close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    var modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    var modalInstance = bootstrap.Modal.getInstance(modal);
    modalInstance.hide();
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        var modalInstance = bootstrap.Modal.getInstance(modal);
        modalInstance.hide();
    }
}

// Handle form submission
document.getElementById("addHostForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission
    var formData = new FormData(this);
    var data = {};
    formData.forEach((value, key) => { data[key] = value });
    
    // Add Created and Status fields
    var now = new Date();
    var formattedDate = now.toISOString(); // Use ISO 8601 format
    data["created"] = formattedDate;
    data["status"] = "1";
    console.log(data); // For debugging purposes

    fetch('/add-proxy-host', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        location.reload()
        // Close the modal
        var modalInstance = bootstrap.Modal.getInstance(modal);
        modalInstance.hide();
        // Optionally, you can refresh the table data here
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Handle delete buttons
document.addEventListener("click", function(event) {
    if (event.target && event.target.classList.contains("btn-delete")) {
        var id = event.target.getAttribute("data-id");
        fetch(`/delete-proxy-host/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Deleted:', data);
            location.reload()
            // Optionally, you can refresh the table data here
            event.target.closest("tr").remove(); // Remove the row from the table
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});

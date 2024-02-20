document.getElementById("encryption-form").addEventListener("submit", function (event) {
    event.preventDefault();

    var formData = new FormData(this);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultContainer = document.getElementById("result-container");
        var resultElement = document.getElementById("result");
        var downloadLink = document.getElementById("download-link");

        if (data.error) {
            resultElement.innerText = "Error: " + data.error;
            downloadLink.style.display = "none";
        } else {
            resultElement.innerText = "Success!";

            // Check the selected algorithm
            var selectedAlgorithm = document.getElementById("algorithm").value;

            if (selectedAlgorithm === "AES" || selectedAlgorithm === "RSA") {
                // For AES or RSA, display the result as text
                resultElement.innerText += "\n" + data.result;
                downloadLink.style.display = "none";
            } else {
                // Handle other algorithms or custom logic here
                downloadLink.style.display = "block";
            }
        }

        resultContainer.style.display = "block";
    })
    .catch(error => console.error("Error:", error));
});

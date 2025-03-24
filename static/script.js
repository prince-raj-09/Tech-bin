document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const imageInput = document.getElementById("imageInput");
    const resultDiv = document.createElement("div");
    resultDiv.id = "result";
    document.body.appendChild(resultDiv);

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        
        const formData = new FormData();
        const file = imageInput.files[0];

        if (!file) {
            resultDiv.innerText = "Please select an image.";
            return;
        }

        formData.append("image", file);

        // Show uploading message
        resultDiv.innerText = "Uploading & Analyzing...";

        fetch("/analyze", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error("Server returned an error!");
            return response.json();
        })
        .then(data => {
            if (data.error) {
                resultDiv.innerText = "Error: " + data.error;
            } else {
                resultDiv.innerText = "Waste Type: " + data.result;
            }
        })
        .catch(error => {
            resultDiv.innerText = "Error: Unable to classify waste. Try again!";
            console.error("Error:", error);
        });
    });
});

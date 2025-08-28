document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    let fileInput = document.getElementById("fileInput");
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Send to backend
    let response = await fetch("/predict", {
        method: "POST",
        body: formData
    });

    let result = await response.json();
    document.getElementById("result").innerText = "Prediction: " + result.prediction;
});

// Image preview
document.getElementById("fileInput").addEventListener("change", function() {
    let file = this.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function(e) {
            let preview = document.getElementById("previewImage");
            preview.src = e.target.result;
            preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});
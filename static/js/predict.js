// static/js/predict.js

const uploadArea = document.getElementById("uploadArea");
const imageInput = document.getElementById("imageInput");
const fileName = document.getElementById("fileName");

// CLICK

uploadArea.addEventListener("click", () => {

    imageInput.click();

});

// FILE CHANGE

imageInput.addEventListener("change", () => {

    if(imageInput.files.length > 0){

        fileName.textContent =
        imageInput.files[0].name;

    }

});

// DRAG OVER

uploadArea.addEventListener("dragover", (e) => {

    e.preventDefault();

    uploadArea.style.borderColor = "#22c55e";

});

// DRAG LEAVE

uploadArea.addEventListener("dragleave", () => {

    uploadArea.style.borderColor =
    "rgba(255,255,255,0.4)";

});

// DROP

uploadArea.addEventListener("drop", (e) => {

    e.preventDefault();

    imageInput.files = e.dataTransfer.files;

    if(imageInput.files.length > 0){

        fileName.textContent =
        imageInput.files[0].name;

    }

});

// LOADING BUTTON

document
.getElementById("uploadForm")
.addEventListener("submit", () => {

    const button =
    document.querySelector(".predict-btn");

    button.innerHTML = `
        <span class="spinner-border spinner-border-sm"></span>
        Analyzing...
    `;

    button.disabled = true;

});
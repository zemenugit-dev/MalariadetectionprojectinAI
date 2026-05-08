
document.addEventListener("DOMContentLoaded", function () {

    const nameInput = document.querySelector("input[name='name']");
    const emailInput = document.querySelector("input[name='email']");
    const roleSelect = document.querySelector("select[name='role']");
    const form = document.querySelector("form");

    // =========================
    // LIVE VALIDATION EVENTS
    // =========================
    nameInput.addEventListener("input", validateName);
    emailInput.addEventListener("input", validateEmail);
    roleSelect.addEventListener("change", validateRole);

    // =========================
    // SUBMIT CONTROL
    // =========================
    form.addEventListener("submit", function (e) {

        if (!validateName() || !validateEmail() || !validateRole()) {
            e.preventDefault(); // stop submit if invalid
        }

    });

    // =========================
    // VALIDATION FUNCTIONS
    // =========================

    function validateName() {

        const value = nameInput.value.trim();
        const regex = /^[A-Za-z\s]+$/;

        if (value.length >= 3 && regex.test(value)) {
            setValid(nameInput);
            return true;
        } else {
            setInvalid(nameInput);
            return false;
        }
    }

    function validateEmail() {

        const value = emailInput.value.trim();
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (regex.test(value)) {
            setValid(emailInput);
            return true;
        } else {
            setInvalid(emailInput);
            return false;
        }
    }

    function validateRole() {

        if (roleSelect.value !== "") {
            setValid(roleSelect);
            return true;
        } else {
            setInvalid(roleSelect);
            return false;
        }
    }

    // =========================
    // UI HELPERS (RED / GREEN)
    // =========================

    function setValid(element) {
        element.style.border = "2px solid #2ecc71";
        element.style.boxShadow = "0 0 5px #2ecc71";
    }

    function setInvalid(element) {
        element.style.border = "2px solid #e74c3c";
        element.style.boxShadow = "0 0 5px #e74c3c";
    }

});
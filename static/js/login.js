
document.addEventListener("DOMContentLoaded", function () {

    const emailInput = document.querySelector("input[name='email']");
    const passwordInput = document.querySelector("input[name='password']");
    const form = document.querySelector("form");

    // =========================
    // LIVE EVENTS
    // =========================
    emailInput.addEventListener("input", validateEmail);
    passwordInput.addEventListener("input", validatePassword);

    // =========================
    // FORM SUBMIT CONTROL
    // =========================
    form.addEventListener("submit", function (e) {

        if (!validateEmail() || !validatePassword()) {
            e.preventDefault();
        }

    });

    // =========================
    // VALIDATIONS
    // =========================

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

    function validatePassword() {

        const value = passwordInput.value;

        if (value.length >= 6) {
            setValid(passwordInput);
            return true;
        } else {
            setInvalid(passwordInput);
            return false;
        }
    }

    // =========================
    // UI EFFECTS
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
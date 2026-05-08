
document.addEventListener("DOMContentLoaded", function () {

    const nameInput = document.querySelector("input[name='fullname']");
    const emailInput = document.querySelector("input[name='email']");
    const passwordInput = document.querySelector("input[name='password']");
    const confirmInput = document.querySelector("input[name='confirm_password']");
    const roleSelect = document.querySelector("select[name='role']");

    // create eye icon for password toggle
    addPasswordToggle(passwordInput);
    addPasswordToggle(confirmInput);

    // =========================
    // LIVE VALIDATION EVENTS
    // =========================

    nameInput.addEventListener("input", validateName);
    emailInput.addEventListener("input", validateEmail);
    passwordInput.addEventListener("input", validatePassword);
    confirmInput.addEventListener("input", validateConfirmPassword);
    roleSelect.addEventListener("change", validateRole);

    // =========================
    // FORM SUBMIT VALIDATION
    // =========================
    document.querySelector("form").addEventListener("submit", function (e) {

        if (
            !validateName() ||
            !validateEmail() ||
            !validatePassword() ||
            !validateConfirmPassword() ||
            !validateRole()
        ) {
            e.preventDefault(); // stop submit
        }

    });

    // =========================
    // VALIDATIONS
    // =========================

    function validateName() {
        const value = nameInput.value.trim();
        const regex = /^[A-Za-z\s]+$/;

        if (value.length >= 6 && regex.test(value)) {
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

    function validatePassword() {
        const value = passwordInput.value;

        const upper = /[A-Z]/;
        const lower = /[a-z]/;
        const number = /[0-9]/;
        const special = /[!@#$%^&*(),.?":{}|<>]/;

        if (
            value.length >= 6 &&
            upper.test(value) &&
            lower.test(value) &&
            number.test(value) &&
            special.test(value)
        ) {
            setValid(passwordInput);
            return true;
        } else {
            setInvalid(passwordInput);
            return false;
        }
    }

    function validateConfirmPassword() {
        if (confirmInput.value === passwordInput.value && confirmInput.value !== "") {
            setValid(confirmInput);
            return true;
        } else {
            setInvalid(confirmInput);
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

    // =========================
    // PASSWORD SHOW / HIDE
    // =========================

    function addPasswordToggle(input) {

        const wrapper = document.createElement("div");
        wrapper.style.position = "relative";

        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        const icon = document.createElement("span");
        icon.innerHTML = "👁️";
        icon.style.position = "absolute";
        icon.style.right = "10px";
        icon.style.top = "50%";
        icon.style.transform = "translateY(-50%)";
        icon.style.cursor = "pointer";
        icon.style.userSelect = "none";

        wrapper.appendChild(icon);

        icon.addEventListener("click", function () {
            if (input.type === "password") {
                input.type = "text";
                icon.innerHTML = "🙈";
            } else {
                input.type = "password";
                icon.innerHTML = "👁️";
            }
        });
    }

});
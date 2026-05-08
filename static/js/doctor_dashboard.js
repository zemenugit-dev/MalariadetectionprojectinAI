// static/js/doctor_dashboard.js

// SIDEBAR TOGGLE

const sidebar = document.getElementById("sidebar");
const menuToggle = document.getElementById("menuToggle");

menuToggle.addEventListener("click", () => {

    sidebar.classList.toggle("active");

});

// ACTIVE MENU EFFECT

const menuLinks = document.querySelectorAll(".menu a");

menuLinks.forEach(link => {

    link.addEventListener("click", function () {

        menuLinks.forEach(item => {
            item.classList.remove("active");
        });

        this.classList.add("active");

    });

});

// CARD ANIMATION

const cards = document.querySelectorAll(".stats-card");

cards.forEach((card, index) => {

    card.style.opacity = "0";
    card.style.transform = "translateY(40px)";

    setTimeout(() => {

        card.style.transition = "0.8s";
        card.style.opacity = "1";
        card.style.transform = "translateY(0px)";

    }, index * 200);

});

// ACTIVITY ANIMATION

const activities = document.querySelectorAll(".activity-item");

activities.forEach((item, index) => {

    item.style.opacity = "0";
    item.style.transform = "translateX(-30px)";

    setTimeout(() => {

        item.style.transition = "0.7s";
        item.style.opacity = "1";
        item.style.transform = "translateX(0px)";

    }, index * 250);

});
 document.querySelector(".logout-btn").addEventListener("click", function(e) {

    const confirmLogout = confirm("Are you sure you want to logout?");

    if (!confirmLogout) {
        e.preventDefault();
    }

});
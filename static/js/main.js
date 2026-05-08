// static/js/main.js

// Simple page animation

window.addEventListener("load", () => {

    document.body.style.opacity = "1";

});

// Smooth scrolling effect

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        document.querySelector(this.getAttribute("href")).scrollIntoView({
            behavior: "smooth"
        });

    });

});

// Hero animation effect

const heroTitle = document.querySelector(".hero-title");

if (heroTitle) {

    heroTitle.style.opacity = "0";
    heroTitle.style.transform = "translateY(40px)";

    setTimeout(() => {

        heroTitle.style.transition = "1s";
        heroTitle.style.opacity = "1";
        heroTitle.style.transform = "translateY(0px)";

    }, 300);

}
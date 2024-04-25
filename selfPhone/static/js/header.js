
// Header Nav Events & Sliders

// Slider
const sliderMenu = document.querySelector("#navigation");
const sliderBasket = document.querySelector(".basket-slider");
const sliderAccount = document.querySelector(".login-slider");

// Icons
const iconMenu = document.querySelector("#icon-menu");
const iconBasket = document.querySelector("#icon-basket");
const iconAccount = document.querySelector("#icon-account");
const iconsClose = Array.from(document.querySelectorAll(".icon-close"));
const allIcons = [iconMenu, iconBasket, iconAccount];

// Various
const overlay = document.querySelector(".overlay");
const allElements = [sliderMenu, sliderBasket, sliderAccount, iconMenu, iconBasket, iconAccount, overlay];


// Functions
function hideAll() {
    allElements.forEach(element => {
        element.classList.remove("visible");
    })
}

function showOverlay() {
    overlay.classList.add("visible");
}

function open(icon, slider) {
    hideAll();
    showOverlay();
    [icon, slider].forEach(element => {
        element.classList.add("visible");
    });
}


// Events

allIcons.forEach(icon => {
    icon.addEventListener('click', function () {
        overlay.classList.add("visible");
    })
})

iconMenu.addEventListener('click', function () {
    open(iconMenu, sliderMenu);
})

iconBasket.addEventListener('click', function () {
    open(iconBasket, sliderBasket);
})

iconAccount.addEventListener('click', function () {
    open(iconAccount, sliderAccount);
})

overlay.addEventListener('click', function () {
    hideAll();
})

iconsClose.forEach(icon => {
    icon.addEventListener('click', function () {
        hideAll();
    })
})


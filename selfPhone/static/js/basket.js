document.addEventListener('DOMContentLoaded', function() {
    const sliderBasket = document.querySelector(".basket-slider");
    const iconBasket = document.querySelector('#icon-basket');
    let isBasketLoaded = false;

    function loadBasket() {
        if (!isBasketLoaded && sliderBasket) {
            fetch('/basket/')
                .then(response => response.text())
                .then(data => {
                    sliderBasket.innerHTML = data;
                    isBasketLoaded = true;
                })
                .catch(error => {
                    console.error("Fehler beim Laden des Warenkorbs:", error);
                });
        }
    }

    if (iconBasket && sliderBasket) {
        iconBasket.addEventListener('click', function() {
            open(iconBasket, sliderBasket);
            loadBasket();
        });
    }
});

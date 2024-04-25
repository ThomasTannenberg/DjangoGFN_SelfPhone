document.addEventListener('DOMContentLoaded', function() {

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

    loadBasket();

});

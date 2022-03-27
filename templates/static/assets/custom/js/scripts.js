(function () {
    select_variation = document.getElementById('select-variation');
    variation_price = document.getElementById('variation-price');
    variation_promo = document.getElementById('variation-promo');

    if (!select_variation) {
        return;
    }

    if (!variation_price) {
        return;
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('date-price');
        promo = this.options[this.selectedIndex].getAttribute('date-promo');

        variation_price.innerHTML = price;

        if (variation_promo) {
            variation_promo.innerHTML = promo;
        }
    })
})();


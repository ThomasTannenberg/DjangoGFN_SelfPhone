// BRAND SLIDER ON start.html

$(document).ready(function(){
    $('.brand-slider').slick({
        slidesToShow: 6,
        slidesToScroll: 6,
        dots: false,
        infinite: true,
        autoplay: false,
        arrows: false,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 5,
                    slidesToScroll: 5
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 4
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3
                }
            }
        ]
    })
});

$(window).on('resize orientationchange', function() {
    $('.brand-slider').slick('resize');
});
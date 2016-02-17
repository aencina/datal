function initSlider(){
    $fDataServicesContainer.carouFredSel({
        circular: true,
        infinite: false,
        width: 410,
        height: 230,
        items: {
            minimum: 1,
            visible: 1,
            width: 410,
            height: 230
        },
        scroll: {
            items: 1,
            duration: 1000,
            pauseOnHover: true,
            onEnd: 
                function(){
                    $fDataServicesContainer.trigger("destroy");
                    $('.caroufredsel_wrapper').css('border', 0);
                    initSlider();
                    restartCharts();
                }
        },
        auto: {
            pauseDuration: 5000,
            delay: 5000,
            duration: 300,
            easing: "easeOutExpo"
        }
    });
}
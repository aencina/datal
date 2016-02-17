$(document).ready(function(){
    initFeaturedSlider();
    initPrioritiesSlider();
    initButtons();

    $(".welcome .pic, .featuredContent .pic, .prioritiesSlider .pic, .bottom article").imgLiquid();
});

function initButtons(){
    $('.buttons .caption').css({
        position: "absolute",
        top: "50%",
        width: "100%",
        marginTop: "-" + $('.buttons .caption').height() / 2 + "px"
    });
};

function initFeaturedSlider(){
    if($('.featuredSlider').length != 0){
        $(".featuredSlider .sliderHome").carouFredSel({
            circular: true, 
            infinite: true,
            align: false,
            width: "100%",
            height: 320,
            items: {
                visible: 1,
                width: "auto",
                height: 320
            },
            scroll: {
                easing: "easeOutExpo",
                duration: 1000,
                pauseOnHover: true
            },
            auto: {
                delay: 1500, 
                pauseDuration: 3500
            },
            prev : {
                button : ".featuredSlider .izq", 
                key : "left"
                },
            next : {
                button : ".featuredSlider .der",
                key : "right"
            }
        });
    }
};

function initPrioritiesSlider(){
    if($('.prioritiesSlider .panel').length > 3){
        $(".prioritiesSlider .sliderHome").carouFredSel({
            auto: false,
            circular: true, 
            infinite: true,
            align: false,
            width: "100%",
            height: 220,
            items: {
                visible: 1,
                width: 280,
                height: 220
            },
            scroll: {
                easing: "easeOutExpo",
                duration: 1000,
                pauseOnHover: true
            },
            prev : {
                button : ".prioritiesSlider .izq", 
                key : "left"
                },
            next : {
                button : ".prioritiesSlider .der",
                key : "right"
            }
        });
    }else{
        $(".prioritiesSlider").css('text-align', 'center');
        $(".prioritiesSlider .btn").css('display', 'none');
    }
};
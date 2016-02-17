$(document).ready(function(){
    initFeaturedSlider();
    initVideoOverlay();
});

function initFeaturedSlider(){
    if($('.featuredSlider').length != 0){
        $(".sliderHome").carouFredSel({
            circular: true, 
            infinite: true,
            align: false,
            width: 960,
            height: 320,
            items: {
                visible: 1,
                width: 960,
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
}

function initVideoOverlay(){

    var thePopup = $('#id_videoPopup');

      thePopup.overlay({
        top: 'center',
        left: 'center',
        mask: {
          color: '#000', 
          loadSpeed: 200, 
          opacity: 0.5, 
          zIndex: 99999
        }
      });

      $('[id*=id_panel_slider_]').click(function(event) {
        console.log(event.currentTarget);
        if( $(event.currentTarget).hasClass('videoSection') ){
            var videoContent = $(event.currentTarget).parent().find('[id*=dialog_]').html();
            thePopup.find('.videoContent').html(videoContent);
            thePopup.data('overlay').load();
        }
      });

}
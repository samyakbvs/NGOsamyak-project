(function($) {

    "use strict";
    /*----------------------
    Document-Reader-Function
    -----------------------*/
    $(document).on('ready', function(){
        
        /*----------------------
        Post-Gallery-Slider
        -----------------------*/
        $('.photo-slider').slick({
            dots: false,
            arrows: true,
            prevArrow: '<button class="slick-prev"  type="button"><i class="fa fa-angle-left"></i></button>',
            nextArrow: '<button class="slick-next" type="button"><i class="fa fa-angle-right"></i></button>',
            infinite: true,
            speed: 1000,
            slidesToShow: 1,
            slidesToScroll: 1,
            responsive: [
                {
                    breakpoint: 1170,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 480,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }
            ]
        });

    });
    /*------------------------
    Window-Load-Function
    -------------------------*/
    $(window).on("load", function () {
        $('.video-post').each(function () {
            var video_src = '';            
            $(this).find(".video-play-bttn").on("click", function (ev) {
                $('.video-post').children('.videoPoster,.video-play-bttn').fadeIn(300);
                $('.video-post').find("iframe").attr("src","");                
                video_src = $(this).siblings('iframe').data("src");                
                $(this).siblings('iframe').attr('src',video_src );              
                $(this).siblings('.videoPoster').fadeOut(300);
                $(this).fadeOut(300);
                return false;
            });
        });
    });
    
    
})(jQuery);
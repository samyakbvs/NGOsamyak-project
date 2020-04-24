;(function($){
    
    
    var WidgetprofundcoreLoadmoreHandler = function ( $scope, $back ) {
        var loaded_elem = $scope.find('.load-more-content').eq(0);        
        if (loaded_elem.length > 0) {            
            var settings = loaded_elem.data('load');
            var loaded_item = settings['loaded_item'];            
            var load_slice = settings['load_slice'];                
            $('.load-more-content').each(function(){
                $(this).children('.campaign-item').addClass('load-item');
                $(this).find(".load-item").hide();
                $(this).find(".load-item").slice(0, loaded_item).show();            
                $(this).siblings('.load-button').find(".load-more").on('click', function (e) {
                    e.preventDefault();
                    var hd_item = $(this).parent().siblings('.load-more-content').find(".load-item:hidden");
                    hd_item.slice(0, load_slice).slideDown(500);
                    if (hd_item.length <= load_slice) {
                        $(this).parent('.load-button').fadeOut('slow');
                    }
                    $('html,body').animate({
                        scrollTop: $(this).offset().top
                    }, 1500);
                });            
            });
        }
    };
    
    
    
    var WidgetprofundcoreProgressHandler = function () {
        $('.skillbar').each(function () {
            $(this).appear(function () {
                $(this).find('.count-bar').animate({
                    width: $(this).attr('data-percent')
                }, 1000);
                var percent = $(this).attr('data-percent');
                $(this).find('.count').html('<span>' + percent + '</span>');
            });
        });
    }
    
    var WidgetProfundcoreArrowButton = function () {
        if ( $( '.mouse-dir' ).length > 0 ) {
            $( '.mouse-dir' ).on( 'mouseenter', function ( e ) {
            var parentOffset = $( this ).offset( ),
                relX = e.pageX - parentOffset.left,
                relY = e.pageY - parentOffset.top;
                if ( $( this ).find( '.dir-part' ) ) {
                    $( '.mouse-dir .dir-part' ).css( {
                        top: relY,
                        left: relX,
                    } );
                }
            } );
            $( '.mouse-dir' ).on( 'mouseout', function ( e ) {
                var parentOffset = $( this ).offset( ),
                    relX = e.pageX - parentOffset.left,
                    relY = e.pageY - parentOffset.top;
                if ( $( this ).find( '.dir-part' ) ) {
                    $( '.mouse-dir .dir-part' ).css( {
                        top: relY,
                        left: relX,
                    } );
                }
            } );
        }
    }
    
    
    var WidgetprofundcoreFilterHandler = function () {
        // Portfolio Image Loded with Masonry
        var $PortfolioMasonry = $('.campaign_filter_items');
        if (typeof imagesLoaded == 'function') {
            imagesLoaded($PortfolioMasonry, function () {
                setTimeout(function () {
                    $PortfolioMasonry.isotope({
                        itemSelector: '.campaign-item',
                        resizesContainer: false,
                        layoutMode: 'masonry',
                        filter: '*'
                    });
                }, 500);

            });
        };
        // Set Active Class for Portfolio filter
        $('.campaign-filter-menu li').on('click', function (event) {
            $('.campaign-filter-menu li').removeClass('active');
            $(this).addClass('active');
            event.preventDefault();
        });
        // Filter JS for Porrtfolio
        $('.campaign-filter-menu').on('click', 'li', function () {
            var filterValue = $(this).attr('data-filter');
            $PortfolioMasonry.isotope({
                filter: filterValue
            });
        });
    }
    
    var WidgetprofundcoreCarouselHandler = function ($scope, $) {
        var carousel_elem = $scope.find('.profundcore-carousel-activation').eq(0);
        if (carousel_elem.length > 0) {
            var settings = carousel_elem.data('settings');
            var arrows = settings['arrows'];
            var arrow_prev_txt = settings['arrow_prev_txt'];
            var arrow_next_txt = settings['arrow_next_txt'];
            var dots = settings['dots'];
            var autoplay = settings['autoplay'];
            var autoplay_speed = parseInt(settings['autoplay_speed']) || 3000;
            var animation_speed = parseInt(settings['animation_speed']) || 300;
            var pause_on_hover = settings['pause_on_hover'];
            var center_mode = settings['center_mode'];
            var center_padding = settings['center_padding'] ? settings['center_padding'] : '50px';
            var display_columns = parseInt(settings['display_columns']) || 1;
            var scroll_columns = parseInt(settings['scroll_columns']) || 1;
            var tablet_width = parseInt(settings['tablet_width']) || 800;
            var tablet_display_columns = parseInt(settings['tablet_display_columns']) || 1;
            var tablet_scroll_columns = parseInt(settings['tablet_scroll_columns']) || 1;
            var mobile_width = parseInt(settings['mobile_width']) || 480;
            var mobile_display_columns = parseInt(settings['mobile_display_columns']) || 1;
            var mobile_scroll_columns = parseInt(settings['mobile_scroll_columns']) || 1;
            var carousel_style_ck = parseInt(settings['carousel_style_ck']) || 1;
            if (carousel_style_ck == 4) {
                carousel_elem.slick({
                    arrows: arrows,
                    prevArrow: '<button class="profundcore-carosul-prev"><i class="' + arrow_prev_txt + '"></i></button>',
                    nextArrow: '<button class="profundcore-carosul-next"><i class="' + arrow_next_txt + '"></i></button>',
                    dots: dots,
                    customPaging: function (slick, index) {
                        var data_title = slick.$slides.eq(index).find('.profundcore-data-title').data('title');
                        return '<h6>' + data_title + '</h6>';
                    },
                    infinite: true,
                    autoplay: autoplay,
                    autoplaySpeed: autoplay_speed,
                    speed: animation_speed,
                    fade: false,
                    pauseOnHover: pause_on_hover,
                    slidesToShow: display_columns,
                    slidesToScroll: scroll_columns,
                    centerMode: center_mode,
                    centerPadding: center_padding,
                    responsive: [
                        {
                            breakpoint: tablet_width,
                            settings: {
                                slidesToShow: tablet_display_columns,
                                slidesToScroll: tablet_scroll_columns
                            }
                        },
                        {
                            breakpoint: mobile_width,
                            settings: {
                                slidesToShow: mobile_display_columns,
                                slidesToScroll: mobile_scroll_columns
                            }
                        }
                    ]
                });
            } else {
                carousel_elem.slick({
                    arrows: arrows,
                    prevArrow: '<button class="slick-prev"><i class="' + arrow_prev_txt + '"></i></button>',
                    nextArrow: '<button class="slick-next"><i class="' + arrow_next_txt + '"></i></button>',
                    dots: dots,
                    infinite: true,
                    autoplay: autoplay,
                    autoplaySpeed: autoplay_speed,
                    speed: animation_speed,
                    fade: false,
                    pauseOnHover: pause_on_hover,
                    slidesToShow: display_columns,
                    slidesToScroll: scroll_columns,
                    centerMode: center_mode,
                    centerPadding: center_padding,
                    responsive: [
                        {
                            breakpoint: tablet_width,
                            settings: {
                                slidesToShow: tablet_display_columns,
                                slidesToScroll: tablet_scroll_columns
                            }
                        },
                        {
                            breakpoint: mobile_width,
                            settings: {
                                slidesToShow: mobile_display_columns,
                                slidesToScroll: mobile_scroll_columns
                            }
                        }
                    ]

                });
            }

        }
    }
    
          

    // Run this code under Elementor.
    $(window).on('elementor/frontend/init', function () {
        elementorFrontend.hooks.addAction('frontend/element_ready/profund-carousel-addons.default', WidgetprofundcoreCarouselHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/profund_Team.default', WidgetprofundcoreCarouselHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/profund-testimonial-addons.default', WidgetprofundcoreCarouselHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/profund-postcarousel-addons.default', WidgetprofundcoreCarouselHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/profund-campaign-box.default', WidgetprofundcoreCarouselHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/profund-campaign-box.default', WidgetprofundcoreProgressHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/profund-campaign-box.default', WidgetprofundcoreFilterHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/profund-campaign-box.default', WidgetprofundcoreLoadmoreHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/profund_button.default', WidgetProfundcoreArrowButton);
    });
    
}(jQuery));
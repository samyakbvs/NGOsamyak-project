;
(function ($) {
    "use strict";
    $(document).on('ready', function () {

        $('.header-search').each(function () {
            $('.search-popup-button').on('click', function () {
                $(this).siblings('.popup-search-form').fadeIn();
            });
            $('.popup-search-form .close-form').on('click', function () {
                $(this).parents('.popup-search-form').fadeOut();
            });
        });
        
        $('#mainmenu').slicknav({
            label: '',
            duration: 500,
            prependTo: '',
            closedSymbol: '<i class="flaticon-right-arrow"></i>',
            openedSymbol: '<i class="flaticon-right-arrow"></i>',
            appendTo: '.mainmenu-area',
            menuButton: '#mobile-toggle',
            closeOnClick: 'true' // Close menu when a link is clicked.
        });

        if (typeof imagesLoaded == 'function') {
            $('.masonrys > div').addClass('masonry-item');
            var $boxes = $('.masonry-item');
            $boxes.hide();
            var $container = $('.masonrys');
            $container.imagesLoaded(function () {
                $boxes.fadeIn();
                $container.masonry({
                    itemSelector: '.masonry-item',
                });
            });
        }
        // Select all links with hashes
        $('.mainmenu-area .primary-menu a[href*="#"]')
            // Remove links that don't actually link to anything
            .not('[href="#"]')
            .not('[href="#0"]')
            .on('click', function (event) {
                // On-page links
                if (
                    location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                    // Figure out element to scroll to
                    var target = $(this.hash);
                    target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                    // Does a scroll target exist?
                    if (target.length) {
                        // Only prevent default if animation is actually gonna happen
                        event.preventDefault();
                        $('html, body').animate({
                            scrollTop: target.offset().top
                        }, 1000, function () {
                            // Callback after animation
                            // Must change focus!
                            var $target = $(target);
                            $target.focus();
                            if ($target.is(":focus")) { // Checking if the target was focused
                                return false;
                            } else {
                                $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                                $target.focus(); // Set focus again
                            };
                        });
                    }
                }
            });

            $('.skillbar').each(function () {
                $(this).appear(function () {
                    $(this).find('.count-bar').animate({
                        width: $(this).attr('data-percent')
                    }, 1000);
                    var percent = $(this).attr('data-percent');
                    $(this).find('.count').html('<span>' + percent + '</span>');
                });
            });

            $('.give-sidebar .widget-title').append('<span></span>');
            $('.give-sidebar .widget-title').addClass('bottom-bar');
    });
    /* Preloader Js
    ===================*/
    $('.preloader .load-close').on('click',function(){
        $('.preloader').fadeOut(500);
    });
    $(window).on("load", function () {
        $('.preloader').fadeOut(500);
        $('#mainmenu .sub-menu').parent('li').children('a').append('<i class="plus"></i>');
        $(".post-single").fitVids();

        /*-- Drop-Down-Menu--*/
        function dropdown_menu() {            
            var sub_menu = $('.toggle-menu .sub-menu'),
                menu_a = $('.toggle-menu ul li a');
            sub_menu.hide();
            sub_menu.siblings('a').on('click', function () {
                $(this).parent('li').siblings('li').find('.sub-menu').slideUp();
                $(this).siblings('.sub-menu').find('.sub-menu').slideUp();
                $(this).siblings('.sub-menu').slideToggle();
                $(this).parents('li').siblings('li').removeClass('open');
                $(this).siblings('.sub-menu').find('li.open').removeClass('open');
                $(this).parent('li').toggleClass('open');
                return false;
            });
        }
        dropdown_menu();        
        $('.menu-toggle-button.button-active').on( 'click',function(){
            $(this).toggleClass('active');
            $('.toggle-menu').toggleClass('active');
            return false;
        });

    });
})(jQuery);
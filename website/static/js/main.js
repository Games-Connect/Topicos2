/*  ---------------------------------------------------
    Theme Name: Anime
    Description: Anime video tamplate
    Author: Colorib
    Author URI: https://colorib.com/
    Version: 1.0
    Created: Colorib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            FIlter
        --------------------*/
        $('.filter__controls li').on('click', function () {
            $('.filter__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.filter__gallery').length > 0) {
            var containerEl = document.querySelector('.filter__gallery');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    // Search model
    $('.search-switch').on('click', function () {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click', function () {
        $('.search-model').fadeOut(400, function () {
            $('#search-input').val('');
        });
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
		Hero Slider
	--------------------*/
    var hero_s = $(".hero__slider");
    hero_s.owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: true,
        nav: true,
        navText: ["<span class='arrow_carrot-left'></span>", "<span class='arrow_carrot-right'></span>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        mouseDrag: false
    });

    /*------------------
        Video Player
    --------------------*/
    const player = new Plyr('#player', {
        controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'captions', 'settings', 'fullscreen'],
        seekTime: 25
    });

    /*------------------
        Niceselect
    --------------------*/
    $('select').niceSelect();

    /*------------------
        Scroll To Top
    --------------------*/
    $("#scrollToTopButton").click(function() {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
     });

     function getPageList(totalPages, page, maxLength){
        function range(start, end){
            return Array.from(Array(end - start + 1), (_, i) => i + start);
        }
        var sideWidth = maxLength < 9 ? 1 : 2;
        var leftWidth = (maxLength - sideWidth * 2 - 3) >> 1;
        var rightWidth = (maxLength - sideWidth * 2 - 3) >> 1;

        if(totalPages <= maxLength){
            return range(1, totalPages);
        }

        if(page <= maxLength - sideWidth - 1 - rightWidth){
            return range(1, maxLength - sideWidth - 1).concat(0, range(totalPages - sideWidth + 1, totalPages));
        }

        if(page >= totalPages - sideWidth - 1 - rightWidth){
            return range(1, sideWidth).concat(0, range(totalPages - sideWidth - 1 - rightWidth - leftWidth, totalPages));
        }

        return range(1, sideWidth).concat(0, range(page - leftWidth, page + rightWidth), 0, range(totalPages - sideWidth + 1, totalPages));
    }

    $(function(){
        var numberOfItems = $(".card-content .product__item").length;
        var limitPerPage = 6;
        var totalPages = Math.ceil(numberOfItems / limitPerPage);
        var paginationSize = 7;
        var currentPage;

        function showPage(wichPage){
            if(wichPage < 1 || wichPage > totalPages) return false;

            currentPage = wichPage;

            $(".card-content .product__item").hide().slice((currentPage - 1) * limitPerPage, currentPage * limitPerPage).show();

            $(".product__pagination a").slice(1, -1).remove();
            
            getPageList(totalPages, currentPage, paginationSize).forEach(item => {
                $("<a>").toggleClass("current-page", item === currentPage)
                .attr({href: "javascript:void(0)"}).text(item || "...").insertBefore(".next-page");
            });
            $(".previous-page").toggleClass("disable", currentPage === 1);
            $(".next-page").toggleClass("disable", currentPage === totalPages);
            return true;
        }

        $(".product__pagination").append(
            $("<a>").addClass("previous-page").attr({href: "javascript:void(0)"}).text("Prev"),
            $("<a>").addClass("next-page").attr({href: "javascript:void(0)"}).text("Next"),
        );

        $(".card-content").show();
        showPage(1);

        $(document).on("click", ".product__pagination a:not(.current-page)", function(){
            if(!!parseInt($(this).text()))
                return showPage(+$(this).text());
        });

        $(".next-page").on("click", function(){
            debugger
            return showPage(currentPage + 1);
        });

        $(".previous-page").on("click", function(){
            debugger
            return showPage(currentPage - 1);
        });
    });

})(jQuery);
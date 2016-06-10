var Navbar = (function ($) {

    var menuTrigger = "#hn-header-trigger";
    var exitMenuTrigger = "#hn-header-close";

    var setClipProperty = function () {
        var headerHeight = $('#hn-header').height();
        var windowHeight = $(window).height();
        var headerTop = windowHeight - headerHeight;
        var windowWidth = $(window).width();
        
    };

    return {
        bindListeners: function () {
            $(menuTrigger).on('click', function () {
                $('#main-content').addClass('move-out');
                $('#main-navigation').addClass('is-visible');
            });
            $(exitMenuTrigger).on('click', function () {
                $('#main-content').removeClass('move-out');
                $('#main-navigation').removeClass('is-visible');
            });
            $(window).on('resize', function () {
               setClipProperty();
            });
        },
        setClipProperty: setClipProperty
    }

})(jQuery);

$(window).on('load', function () {
   Navbar.bindListeners();
});
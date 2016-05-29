var Alert = (function ($) {
    
    var closeTag = '.alert-close';

    return {
        // This function is called on a window load event
        listener: function () {
            $(closeTag).on('click', function (e) {
                e.preventDefault();
                console.log($(this).parent().slideUp(350));
            });
        }
    }
    
})(jQuery);

$(document).ready(function () {
  Alert.listener();
});
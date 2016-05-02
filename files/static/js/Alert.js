var Alert = (function () {
    
    var closeTag = '[data-close="alert"]';
    
    var closeAlert = function (e) {
        e.preventDefault();
        console.log('alert click');
        console.log('this', this);
        console.log('e', e.target);
        var parent = e.target;
        // Lacks matchesSelector
        while ((parent = parent.parentElement) && !((parent.matches('.hn-alert')))) {
            console.log('next');
        }
        console.log('found', parent);
        parent.parentElement.removeChild(parent);
    };


    return {
        // This function is called on a window load event
        listener: function () {
            var alerts = document.getElementsByClassName('hn-alert-dismiss');
            if (alerts.length > 0) {
                console.log('Add alert listeners');
                for (var i = 0; i < alerts.length; i++) {
                    alerts[i].addEventListener('click', closeAlert)
                }
            }
        }
    }

    
})();

window.addEventListener('load', function () {
  // Alert.listener();
});

// TODO: Add support for new DOM nodes as well
// var onNewElement = function () {
//   try {
//       switch (e.target.id) {
//           case 'hn-alert': Alert.listener; break;
//           default:
//               console.log('def');
//               break;
//       }
//   }  catch (exeption) {}
// };

//document.addEventListener('DOMNodeInserted', onNewElement, false);

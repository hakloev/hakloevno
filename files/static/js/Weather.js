var Weather = (function () {

    var apiURL = '/static/files/varsel.xml';

    var success = function (data) {
        document.getElementById('weather').innerHTML = JSON.stringify(data);
    };

    var getWeatherData = function () {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', apiURL, true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState != 4 || xhr.status != 200) return;

            var parser = new DOMParser();
            var doc = parser.parseFromString(xhr.responseText, "application/xml");
            var forecastNode = doc.getElementsByTagName('forecast')[0];
            var newestForecastNode = forecastNode.getElementsByTagName('tabular')[0].getElementsByTagName('time')[0];

            var symbol =  newestForecastNode.getElementsByTagName('symbol')[0].getAttribute('number');
            var windDirection = newestForecastNode.getElementsByTagName('windDirection')[0].getAttribute('name');
            var windSpeed =  newestForecastNode.getElementsByTagName('windSpeed')[0].getAttribute('mps');
            var windSpeedText =  newestForecastNode.getElementsByTagName('windSpeed')[0].getAttribute('name');
            var temperature = newestForecastNode.getElementsByTagName('temperature')[0].getAttribute('value');
            var pressure = newestForecastNode.getElementsByTagName('pressure')[0].getAttribute('value');

            success({
                'symbol': symbol,
                'windDirection': windDirection,
                'windSpeed': windSpeed,
                'windSpeedText': windSpeedText,
                'temperature': temperature,
                'pressure': pressure
            });
        };

        xhr.send();
    };

    return {
        get: getWeatherData
    }

})();

window.addEventListener('load', function () {
    Weather.get();
});

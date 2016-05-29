var Weather = (function () {

    var apiURL = '/static/files/varsel.xml';

    var success = function (data) {
        var temperatureString = data.temperature + "°C";
        var precipitationString = data.precipitation + " mm";
        var windString = data.windSpeed + " m/s from " + data.windDirection;

        document.getElementById('hn-weather-temperature').innerHTML = temperatureString;
        document.getElementById('hn-weather-precipitation').innerHTML = precipitationString;
        document.getElementById('hn-weather-wind').innerHTML = windString;
        document.getElementById('hn-weather-forecast').innerHTML = data.text;
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

            var text = forecastNode.getElementsByTagName('text')[0].getElementsByTagName('body')[0].childNodes[0].data;
            var symbol =  newestForecastNode.getElementsByTagName('symbol')[0].getAttribute('number');
            var precipitation = newestForecastNode.getElementsByTagName('precipitation')[0].getAttribute('value');
            var windDirection = newestForecastNode.getElementsByTagName('windDirection')[0].getAttribute('code');
            var windSpeed =  newestForecastNode.getElementsByTagName('windSpeed')[0].getAttribute('mps');
            var windSpeedText =  newestForecastNode.getElementsByTagName('windSpeed')[0].getAttribute('name');
            var temperature = newestForecastNode.getElementsByTagName('temperature')[0].getAttribute('value');
            var pressure = newestForecastNode.getElementsByTagName('pressure')[0].getAttribute('value');

            success({
                'text': text,
                'symbol': symbol,
                'precipitation': precipitation,
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
    var weather = document.getElementById('weather-card');
    if (weather) { Weather.get(); }
});

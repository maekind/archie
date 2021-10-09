# encoding:utf-8

"""
weather.py - open weather inteface to make online queries for forcasting
"""

import logging
import requests

class WeatherInterfaceRequestException(Exception):
    """ Custom Request Exception for Weather Interface """
    message = "Weather request error. Code 404"

class WeatherInterface():
    """
    Class to provide methods to request online forecast to openweather API
    """

    _base_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang={}&units=metric"
    _onecall_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely,alerts&appid={}&lang={}&units=metric"
     #one call: https://api.openweathermap.org/data/2.5/onecall?lat=41.725&lon=1.8266&exclude=hourly,minutely,alerts&appid=30524e1493576ced69c16d9831731363
    # example 1:
    #{
    #   "coord":{"lon":1.8266,"lat":41.725},
    #   "weather": [{"id":804,"main":"Clouds","description":"nubes","icon":"04d"}],
    #   "base":"stations",
    #   "main":{"temp":19.68,"feels_like":19.56,"temp_min":15.65,"temp_max":22.24,"pressure":1019,"humidity":71},
    #   "visibility":10000,
    #   "wind":{"speed":5.81,"deg":158,"gust":7.6},
    #   "clouds":{"all":98},
    #   "dt":1633787852,
    #   "sys":{"type":2,"id":2009765,"country":"ES","sunrise":1633759081,"sunset":1633800093},
    #   "timezone":7200,"id":3117533,"name":"Manresa","cod":200
    # }
    # example one call:
    # {
    #   "lat":41.725,"lon":1.8266,"timezone":"Europe/Madrid","timezone_offset":7200,
    #   "current":{"dt":1633789856,"sunrise":1633759081,"sunset":1633800093,"temp":292.69,"feels_like":292.58,"pressure":1018,"humidity":72,"dew_point":287.51,"uvi":1.39,"clouds":81,"visibility":10000,"wind_speed":5.81,"wind_deg":158,"wind_gust":8.49,"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}]},
    #   "daily":[
    #       {"dt":1633777200,"sunrise":1633759081,"sunset":1633800093,"moonrise":1633771680,"moonset":1633807200,"moon_phase":0.11,"temp":{"day":293.68,"min":286.8,"max":293.82,"night":288.58,"eve":292.14,"morn":286.85},"feels_like":{"day":293.36,"night":288.48,"eve":292.03,"morn":286.65},"pressure":1020,"humidity":60,"dew_point":285.66,"wind_speed":3.56,"wind_deg":171,"wind_gust":3.77,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":35,"pop":0.36,"rain":0.11,"uvi":4.32},
    #       {"dt":1633863600,"sunrise":1633845547,"sunset":1633886394,"moonrise":1633862760,"moonset":1633896180,"moon_phase":0.15,"temp":{"day":294.2,"min":287.9,"max":295.17,"night":288.22,"eve":291.83,"morn":288.95},"feels_like":{"day":293.74,"night":288.11,"eve":291.56,"morn":288.75},"pressure":1021,"humidity":53,"dew_point":283.36,"wind_speed":3.49,"wind_deg":200,"wind_gust":3.98,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"clouds":36,"pop":0.18,"uvi":4.65},
    #       {"dt":1633950000,"sunrise":1633932013,"sunset":1633972696,"moonrise":1633953600,"moonset":1633985760,"moon_phase":0.19,"temp":{"day":294.66,"min":285.05,"max":297.07,"night":288.41,"eve":292.91,"morn":285.42},"feels_like":{"day":293.81,"night":287.92,"eve":292.12,"morn":284.9},"pressure":1021,"humidity":36,"dew_point":278.31,"wind_speed":2.02,"wind_deg":254,"wind_gust":3.08,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":2,"pop":0,"uvi":4.62},
    #       {"dt":1634036400,"sunrise":1634018480,"sunset":1634058999,"moonrise":1634043900,"moonset":1634075820,"moon_phase":0.22,"temp":{"day":295.74,"min":285.23,"max":296.74,"night":288.62,"eve":290.71,"morn":285.53},"feels_like":{"day":294.94,"night":287.89,"eve":289.83,"morn":284.81},"pressure":1018,"humidity":34,"dew_point":278.19,"wind_speed":1.75,"wind_deg":351,"wind_gust":2.19,"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"clouds":12,"pop":0,"uvi":4.29},
    #       {"dt":1634122800,"sunrise":1634104947,"sunset":1634145302,"moonrise":1634133540,"moonset":0,"moon_phase":0.25,"temp":{"day":294.69,"min":284.94,"max":295.35,"night":287.08,"eve":288.91,"morn":284.94},"feels_like":{"day":293.6,"night":286.72,"eve":288.24,"morn":283.61},"pressure":1017,"humidity":27,"dew_point":274.27,"wind_speed":2.29,"wind_deg":152,"wind_gust":2.83,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":5,"pop":0,"uvi":4.04},
    #       {"dt":1634209200,"sunrise":1634191414,"sunset":1634231607,"moonrise":1634222520,"moonset":1634166300,"moon_phase":0.3,"temp":{"day":290.84,"min":284.12,"max":291.69,"night":286.34,"eve":287.53,"morn":284.12},"feels_like":{"day":290.26,"night":285.86,"eve":287.16,"morn":282.81},"pressure":1022,"humidity":61,"dew_point":282.31,"wind_speed":3.87,"wind_deg":188,"wind_gust":4.38,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"clouds":88,"pop":0.04,"uvi":5},
    #       {"dt":1634295600,"sunrise":1634277882,"sunset":1634317912,"moonrise":1634311020,"moonset":1634256900,"moon_phase":0.33,"temp":{"day":293.66,"min":283.92,"max":294.38,"night":286.95,"eve":288.98,"morn":283.92},"feels_like":{"day":292.99,"night":286.71,"eve":288.5,"morn":283.38},"pressure":1022,"humidity":47,"dew_point":281,"wind_speed":2.35,"wind_deg":238,"wind_gust":3.15,"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"clouds":18,"pop":0,"uvi":5},
    #       {"dt":1634382000,"sunrise":1634364350,"sunset":1634404218,"moonrise":1634399160,"moonset":1634347560,"moon_phase":0.36,"temp":{"day":294.57,"min":284.71,"max":295.37,"night":288.03,"eve":289.57,"morn":284.71},"feels_like":{"day":293.99,"night":287.98,"eve":289.43,"morn":284.14},"pressure":1020,"humidity":47,"dew_point":282,"wind_speed":2.62,"wind_deg":159,"wind_gust":3.12,"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":63,"pop":0.15,"uvi":5}
    #   ]
    # }

    def __init__(self, city, key, language):
        """
        Default constructor
        """
        self._logger = logging.getLogger("Weather interface")
        # Set base url with parameters
        self._base_url = format(self._base_url, city, key, language)

        # Set api key
        self._key = key

        # Set language
        self._language = language

    def search(self, when="today"):
        """
        Method to search the weather info
        """
        # call api
        response = requests.get(self._base_url)
        # get json response
        json_data = response.json()
        # Initialize weather info instance
        weather_info = WeatherInfo()

        # Check for request error
        if json_data["cod"] != "404":
            # Get coordinates for one call
            latitude = json_data["coord"].get("lat")
            longitude = json_data["coord"].get("lon")
            
            # Formatting one call request
            self._onecall_url = format(self._onecall_url, latitude, longitude, self._key, self._language)
            
            # call api
            response = requests.get(self._onecall_url)

            # get json response
            json_data = response.json()

            # Check for request error
            if json_data["cod"] != "404":
                main = json_data["main"]
                weather = json_data["weather"][0]
                wind = json_data["wind"]

            else:
                raise WeatherInterfaceRequestException()
            
        else:
            raise WeatherInterfaceRequestException()
        
              
        return weather_info

class WeatherInfo():
    """
    Class to store response from request
    """

    _city = ""
    _description = ""
    _current_temperature = 0
    _feels_like = 0
    _min_temperature = 0
    _max_temperature = 0
    _pressure = 0
    _humidity = 0
    _wind_speed = 0
    _clouds_percentage = 0

    @property
    def current_temperature(self):
        """
        Property current temperature
        """
        return self._current_temperature

    @current_temperature.setter
    def current_temperaure(self, value):
        """
        Setter for current temperature
        """
        self._current_temperature = value



    


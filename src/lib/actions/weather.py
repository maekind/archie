# encoding:utf-8

"""
weather.py - open weather inteface to make online queries for forcasting
It includes the following classes:
+ WeatherInterface -> Main class that returns a WeatherInfoList
+ WeatherInterfaceRequestException
+ WeatherInfoItem
+ WeatherInfoList
"""

import logging
from typing import List
from datetime import datetime
import requests
import json


class WeatherInterfaceRequestException(Exception):
    """ Custom Request Exception for Weather Interface """
    # Setting custom message
    message = "Weather request error. Code 404"


class WeatherInfoList(List):
    """ Class to handle a list of WeatherInfo items """


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
        # Set logger instance name
        self._logger = logging.getLogger("Weather interface")

        # Set base url with parameters
        self._base_url = self._base_url.format(city, key, language)

        # Set api key
        self._key = key

        # Set language
        self._language = language

        # Set city
        self._city = city

    def search(self, when="today") -> WeatherInfoList:
        """
        Method to request the weather info
        Returns an instance of WeatherInfoList with items of type WeatherInfoItem
        """
        self._logger.debug(f"Request coordinates for {self._city}")
        try:
            # call api
            response = requests.get(self._base_url)
            # get json response
            json_data = response.json()
            # Initialize weather info list
            weather_info_list = WeatherInfoList()

            # Get coordinates for one call
            latitude = json_data["coord"].get("lat")
            longitude = json_data["coord"].get("lon")

            self._logger.debug(
                f"{self._city}: lat({latitude}) lon({longitude})")

            self._logger.debug("Request for weather")
            # Formatting one call request
            self._onecall_url = self._onecall_url.format(
                latitude, longitude, self._key, self._language)

            # call api
            response = requests.get(self._onecall_url)

            # get json response
            json_data = response.json()
            # get current weather
            current = json_data.get("current")
            weather_current = WeatherInfoCurrent()
            weather_current.city = self._city
            weather_current.temperature = current.get("temp")
            weather_current.feels_like = current.get("feels_like")
            weather_current.pressure = current.get("pressure")
            weather_current.humidity = current.get("humidity")
            weather_current.wind_speed = current.get("wind_speed")
            weather_current.humidity = current.get("humidity")
            weather_current.clouds_percentage = current.get("clouds")
            weather_current.weather_main = current.get("weather")[
                0].get("main")
            weather_current.weather_description = current.get("weather")[
                0].get("description")
            # save current to weather list
            weather_info_list.append(weather_current)

            daily_list = json_data.get("daily")

            # iter daily list
            for day in daily_list:
                weather_day = WeatherInfoDay()
                weather_day.city = self._city
                weather_day.day = day.get("dt")
                weather_day.temperature = day.get("temp").get("day")
                weather_day.min_temperature = day.get("temp").get("min")
                weather_day.max_temperature = day.get("temp").get("max")
                weather_day.feels_like = day.get("feels_like").get("day")
                weather_day.pressure = day.get("pressure")
                weather_day.humidity = day.get("humidity")
                weather_day.wind_speed = day.get("wind_speed")
                weather_day.weather_main = current.get("weather")[
                    0].get("main")
                weather_day.weather_description = current.get(
                    "weather")[0].get("description")
                weather_day.clouds_percentage = current.get("clouds")

                # save day to weather list
                weather_info_list.append(weather_day)

        except Exception:
            raise WeatherInterfaceRequestException()

        return weather_info_list


class WeatherInfoItem():
    """
    Class to store response from request
    """

    _city = ""
    _weather_main = ""
    _weather_description = ""
    _temperature = 0
    _feels_like = 0
    _pressure = 0
    _humidity = 0
    _wind_speed = 0
    _clouds_percentage = 0

    @property
    def city(self):
        """
        Property city
        """
        return self._city

    @city.setter
    def city(self, value):
        """
        Setter for city
        """
        self._city = value

    @property
    def weather_main(self):
        """
        Property weather_main
        """
        return self._weather_main

    @weather_main.setter
    def weather_main(self, value):
        """
        Setter for weather_main
        """
        self._weather_main = value

    @property
    def weather_description(self):
        """
        Property weather_description
        """
        return self._weather_description

    @weather_description.setter
    def weather_description(self, value):
        """
        Setter for weather_description
        """
        self._weather_description = value

    @property
    def temperature(self):
        """
        Property temperature
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        """
        Setter for temperature
        """
        self._temperature = value

    @property
    def feels_like(self):
        """
        Property feels_like
        """
        return self._feels_like

    @feels_like.setter
    def feels_like(self, value):
        """
        Setter for feels_like
        """
        self._feels_like = value

    @property
    def pressure(self):
        """
        Property pressure
        """
        return self._pressure

    @pressure.setter
    def pressure(self, value):
        """
        Setter for pressure
        """
        self._pressure = value

    @property
    def humidity(self):
        """
        Property humidity
        """
        return self._humidity

    @humidity.setter
    def humidity(self, value):
        """
        Setter for humidity
        """
        self._humidity = value

    @property
    def wind_speed(self):
        """
        Property wind_speed
        """
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, value):
        """
        Setter for wind_speed
        """
        self._wind_speed = value

    @property
    def clouds_percentage(self):
        """
        Property clouds_percentage
        """
        return self._clouds_percentage

    @clouds_percentage.setter
    def clouds_percentage(self, value):
        """
        Setter for clouds_percentage
        """
        self._clouds_percentage = value


class WeatherInfoCurrent(WeatherInfoItem):
    """
    Class to store current weather
    """


class WeatherInfoDay(WeatherInfoItem):
    """
    Class to store weather for a day
    """
    _day = 0
    _min_temperature = 0
    _max_temperature = 0

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(\n\t%r %r\n\tmin temperature = %r ºC\n\tmax temperature = %rªC\n)" % (
            self.__class__.__name__, self._city, datetime.utcfromtimestamp(self._day).strftime('%d/%m/%Y'), self._min_temperature, self._max_temperature)

    @property
    def day(self):
        """
        Property day
        """
        return self._day

    @day.setter
    def day(self, value):
        """
        Setter for day
        """
        self._day = value

    @property
    def min_temperature(self):
        """
        Property min_temperature
        """
        return self._min_temperature

    @min_temperature.setter
    def min_temperature(self, value):
        """
        Setter for min_temperature
        """
        self._min_temperature = value

    @property
    def max_temperature(self):
        """
        Property max_temperature
        """
        return self._max_temperature

    @max_temperature.setter
    def max_temperature(self, value):
        """
        Setter for max_temperature
        """
        self._max_temperature = value


# Main test
if __name__ == "__main__":
    logargs = {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'}

    logargs["level"] = "INFO"

    logging.basicConfig(**logargs)

    # Get key
    # TODO: put here your key json file with the following content:
    # { "key": "put your 32 bytes openweather key here" }
    with open("../../../data/conf/openweather.json", "r") as key_file:
        key = json.loads(key_file.read()).get("key")

    # Request for weather in Barcelona
    try:
        logging.info("Create request")
        weather = WeatherInterface("Barcelona", key, "es")
        weatherInfo = WeatherInfoList()
        logging.info("Search")
        weatherInfo = weather.search()

        # Iter weather info
        for weaterItem in weatherInfo:
            if isinstance(weaterItem, WeatherInfoCurrent):
                logging.debug("Weather item current")
                pass
            elif isinstance(weaterItem, WeatherInfoDay):
                logging.debug("Weather item day")
                print(weaterItem)
    except Exception as e:
        logging.error(e.message)

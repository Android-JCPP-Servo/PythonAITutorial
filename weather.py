# Weather.py AI weather skill
# May 30, 2023

from pyowm import OWM
from geopy import Nominatim, location
from datetime import datetime

class Weather():
    # The location of where you want the forecast
    __location = "Manor, TX"
    
    # API key
    api_key = "f8abcaac0a58da856ec3123ccaa42a8d"

    # Initialization
    def __init__(self):
        self.owm = OWM(self.api_key)
        self.mgr = self.owm.weather_manager()
        locator = Nominatim(user_agent="myGeoCoder")
        city = "Austin"
        state = "TX"
        self.__location = city + ", " + state
        loc = locator.geocode(self.__location)
        self.lat = loc.latitude
        self.lon = loc.longitude
    
    def uv_index(self, uvi:float):
        """ Returns a message depending on the UV index provided """
        message = ""
        if uvi <= 2.0:
            message = f"The UV level is low: {uvi}. No skin protection necessary."
        if uvi >= 3.0 and uvi < 6.0:
            message = f"The UV level is medium: {uvi}. Skin protection is highly recommended."
        if uvi >= 6.0 and uvi < 8.0:
            message = f"The UV level is high: {uvi}. Skin protection is required."
        if uvi >= 8.0 and uvi < 11.0:
            message = f"The UV level is very high: {uvi}. Extra skin protection is required."
        if uvi >= 11.0:
            message = f"The UV level is extremely high: {uvi}. Caution is advised and extra skin protection is required."
        return message

    # Get the weather
    @property
    def weather(self):
        forecast = self.mgr.one_call(lat=self.lat, lon=self.lon)
        return forecast
    
    @property
    def forecast(self):
        """Returns the forecast at this location"""
        forecast = self.mgr.one_call(lat=self.lat, lon=self.lon)
        detail_status = forecast.forecast_daily[0].detailed_status
        pressure = str(forecast.forecast_daily[0].pressure.get('press'))
        humidity = str(forecast.forecast_daily[0].humidity)
        sunrise = datetime.utcfromtimestamp(forecast.forecast_daily[0].sunrise_time()).strftime("%H:%M:%S")
        sunset = datetime.utcfromtimestamp(forecast.forecast_daily[0].sunset_time()).strftime("%H:%M:%S")
        temperature = str(forecast.forecast_daily[0].temperature('fahrenheit').get("day"))
        uvi = forecast.forecast_daily[0].uvi
        
        message = f"Today's Weather: Today will be mostly {detail_status}, with a humidity of {humidity}%, and a pressure of {pressure} millibars. Sunrise was at {sunrise}, and sunset will be at {sunset}. The temperature is {temperature} degrees Fahrenheit. {self.uv_index(uvi)}"

        return message

# Demo
# myweather = Weather()
# print(myweather.forecast)
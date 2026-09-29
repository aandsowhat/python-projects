import requests
import os


api_key = os.environ.get("OPENWEATHER_API_KEY")

def get_weather(city, API_KEY=None):
    key = api_key or API_KEY
    if not key:
        return "API key is not set. Please set the OPENWEATHER_API_KEY environment variable."
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    print(requests.get(url).json())
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            messsage = data.get("message", "unknown error")
            return f"Could not retrieve weather data for {city}. Error: {messsage}"
        weather = data["weather"][0]["main"]
        temperature = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        return (f"The weather in {city} is {weather} with a temperature of"
               f" {temperature}°C and feels like {feels_like}°C.")
    except requests.exceptions.RequestException:
        return "An error occurred while trying to retrieve the weather data."
    except (KeyError, IndexError):
        return f"Could not parse weather data for {city}. The response format may have changed."

if __name__ == "__main__":
    city = input("Enter a city: ")
    print(get_weather(city))
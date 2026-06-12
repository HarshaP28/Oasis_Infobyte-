import requests
from datetime import datetime
 
# ─────────────────────────────────────────────────────────────
#  👇 PASTE YOUR FREE API KEY HERE
#  Get it free at: https://openweathermap.org
#  Sign Up → My API Keys → Copy → Paste below
# ─────────────────────────────────────────────────────────────
API_KEY = "3ea090b503ee9f4f911f00065691decd"
 
BASE_URL     = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
 
WEATHER_EMOJI = {
    "Clear"        : "☀️",
    "Clouds"       : "☁️",
    "Rain"         : "🌧️",
    "Drizzle"      : "🌦️",
    "Thunderstorm" : "⛈️",
    "Snow"         : "❄️",
    "Mist"         : "🌫️",
    "Fog"          : "🌫️",
    "Haze"         : "🌫️",
    "Smoke"        : "🌫️",
    "Dust"         : "🌪️",
    "Tornado"      : "🌪️",
}
 
 
def print_divider(char="─", length=50):
    print(char * length)
 
 
def get_weather(city, unit="metric"):
    """Fetch current weather data."""
    try:
        params   = {"q": city, "appid": API_KEY, "units": unit}
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, "❌ City not found! Please check the city name."
        elif response.status_code == 401:
            return None, "❌ Invalid API Key! Please check your key."
        else:
            return None, f"❌ Error {response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "❌ No internet connection!"
    except requests.exceptions.Timeout:
        return None, "❌ Request timed out. Try again!"
    except Exception as e:
        return None, f"❌ {str(e)}"
 
 
def get_forecast(city, unit="metric"):
    """Fetch 5-day forecast (every 3 hours, we pick one per day)."""
    try:
        params   = {"q": city, "appid": API_KEY, "units": unit, "cnt": 40}
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, "Could not fetch forecast."
    except Exception as e:
        return None, str(e)
 
 
def display_current_weather(data, unit):
    """Print current weather in a nice format."""
    city        = data["name"]
    country     = data["sys"]["country"]
    condition   = data["weather"][0]["main"]
    description = data["weather"][0]["description"].title()
    temp        = round(data["main"]["temp"])
    feels_like  = round(data["main"]["feels_like"])
    temp_min    = round(data["main"]["temp_min"])
    temp_max    = round(data["main"]["temp_max"])
    humidity    = data["main"]["humidity"]
    pressure    = data["main"]["pressure"]
    wind_speed  = data["wind"]["speed"]
    visibility  = data.get("visibility", 0) // 1000
    sunrise     = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
    sunset      = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
 
    unit_sym  = "°C" if unit == "metric"   else "°F"
    wind_unit = "m/s" if unit == "metric"  else "mph"
    emoji     = WEATHER_EMOJI.get(condition, "🌡️")
 
    print("\n")
    print_divider("═")
    print(f"  {emoji}  WEATHER FOR {city.upper()}, {country}")
    print_divider("═")
 
    print(f"\n  📍 Location     : {city}, {country}")
    print(f"  🕐 Time         : {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    print(f"  🌤️  Condition    : {description}")
 
    print_divider()
    print(f"  🌡️  Temperature  : {temp}{unit_sym}")
    print(f"  🤔 Feels Like   : {feels_like}{unit_sym}")
    print(f"  🔼 Max Temp     : {temp_max}{unit_sym}")
    print(f"  🔽 Min Temp     : {temp_min}{unit_sym}")
 
    print_divider()
    print(f"  💧 Humidity     : {humidity}%")
    print(f"  💨 Wind Speed   : {wind_speed} {wind_unit}")
    print(f"  👁️  Visibility   : {visibility} km")
    print(f"  🔵 Pressure     : {pressure} hPa")
 
    print_divider()
    print(f"  🌅 Sunrise      : {sunrise}")
    print(f"  🌇 Sunset       : {sunset}")
    print_divider("═")
 
 
def display_forecast(data, unit):
    """Print 5-day forecast."""
    unit_sym = "°C" if unit == "metric" else "°F"
    forecasts = data["list"]
 
    # Pick one reading per day (every 8th item = 24 hours apart)
    daily = {}
    for item in forecasts:
        date = item["dt_txt"].split(" ")[0]
        if date not in daily:
            daily[date] = item
 
    print("\n  📅  5-DAY FORECAST")
    print_divider("─")
 
    for i, (date, item) in enumerate(list(daily.items())[:5]):
        day_name    = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %b")
        condition   = item["weather"][0]["main"]
        description = item["weather"][0]["description"].title()
        temp        = round(item["main"]["temp"])
        emoji       = WEATHER_EMOJI.get(condition, "🌡️")
        print(f"  {emoji}  {day_name:<20} {temp}{unit_sym:<8} {description}")
 
    print_divider("═")
 
 
def show_weather(city, unit="metric"):
    """Main function — show full weather report."""
 
    if API_KEY == "your_api_key_here":
        print("\n" + "="*50)
        print("  ⚠️  API KEY MISSING!")
        print("="*50)
        print("  1. Go to: https://openweathermap.org")
        print("  2. Click Sign Up (it's FREE)")
        print("  3. Go to My API Keys")
        print("  4. Copy your key")
        print("  5. Paste it in the code where it says:")
        print("     API_KEY = 'your_api_key_here'")
        print("="*50)
        return
 
    print(f"\n  🔍 Searching weather for: {city}...")
 
    # Current weather
    data, error = get_weather(city, unit)
    if error:
        print(f"\n  {error}")
        return
    display_current_weather(data, unit)
 
    # Forecast
    forecast_data, forecast_error = get_forecast(city, unit)
    if forecast_data:
        display_forecast(forecast_data, unit)
    else:
        print(f"  Forecast not available: {forecast_error}")
 
 
# ── CELL 3 : Search weather for any city ─────────────────────
# Copy this in Cell 3 and change the city name:
 
# Search in Celsius (default)
show_weather("Bengaluru")
 
# Search in Fahrenheit
# show_weather("New York", unit="imperial")
 
# Search any city
# show_weather("London")
# show_weather("Tokyo")
# show_weather("Mumbai")
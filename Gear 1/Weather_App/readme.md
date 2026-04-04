# 🌤️ Weather App

<p align="center">
  <img src="https://media1.tenor.com/m/3EAMvXWYqfAAAAAC/ollie.gif" alt="Weather App" width="800"/>
</p>

> Type a city. Get the weather. No nonsense. ☀️

---

## 🎯 What it does

A clean GUI weather app built with PyQt5. Enter any city name and it fetches real-time weather data from the OpenWeatherMap API — displaying the temperature in Celsius, a weather emoji, and a short description.

---

## 📁 Files

| File | Description |
| --- | --- |
| `weather_app.py` | 🚀 The entire app — run this to check the weather |

---

## ⚙️ How it works

1. **Input** — Type a city name into the text field
2. **Fetch** — Click `Get Weather` to call the OpenWeatherMap API
3. **Display** — Temperature in °C, a matching weather emoji, and a description are shown
4. **Errors** — Any connection or HTTP error is caught and displayed cleanly on screen

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Weather_App"
```

### 2. Install dependencies
```bash
pip install PyQt5 requests
```

### 3. Add your API key

Open `weather_app.py` and replace the placeholder:
```python
API_key = "your api key here from openweather"
```

> Get a free API key from: https://openweathermap.org/api

### 4. Run the app
```bash
python weather_app.py
```

---

## 🌦️ Weather Emojis

| Condition | Emoji |
| --- | --- |
| Thunderstorm | ⛈️⚡🌩️ |
| Drizzle | 🌦️🌧️ |
| Rain | 🌧️🌦️☔ |
| Snow | 🌨️❄️☃️ |
| Fog / Mist | 🌫️🌁 |
| Volcano | 🌋 |
| Windy | 💨 |
| Tornado | 🌪️ |
| Clear Sky | ☀️🌞 |
| Cloudy | ☁️ |

---

## 📦 Requirements
```bash
pip install PyQt5 requests
```

---

## 📝 Notes

- Requires an active internet connection to fetch weather data
- Temperature is displayed in **Celsius**
- All HTTP errors (400, 401, 404, 500 etc.) are handled and shown on screen
- Free OpenWeatherMap API keys work fine for this app

---

*"Check the weather before you step out. Every time."*

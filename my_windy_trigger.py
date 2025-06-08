import requests
import os
from collections import defaultdict

# 🔐 Clés à garder secrètes
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 📍 Coordonnées de Liège
lat, lon = 50.6333, 5.5667

# 🔗 API OpenWeather
url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
response = requests.get(url)
data = response.json()

# 🌀 Regrouper les vitesses de vent par jour
vents_par_jour = defaultdict(list)

for forecast in data["list"]:
    date = forecast["dt_txt"].split(" ")[0]
    wind_speed_kmh = round(forecast["wind"]["speed"] * 3.6, 2)
    vents_par_jour[date].append((forecast["dt_txt"], wind_speed_kmh))

# 📩 Construire les messages
messages = []
for day, previsions in vents_par_jour.items():
    message = f"📅 Prévisions pour le {day} :\n"
    for dt, wind_kmh in previsions:
        alert = " ⚠️" if wind_kmh > 30 else ""
        hour = dt.split(" ")[1][:5]
        message += f"  - {hour} : {wind_kmh} km/h{alert}\n"
    messages.append(message)

# 🚀 Envoyer un message Telegram par jour
for message in messages:
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, data=payload)

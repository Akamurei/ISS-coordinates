import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv

load_dotenv()

MY_LAT = os.environ["MY_LAT"]
MY_LNG = os.environ["MY_LNG"]
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

print(iss_latitude)
print(iss_longitude)

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now()
hour = time_now.hour

print(hour)
while True:
    time.sleep(60)
    if (MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5) and \
       (MY_LNG - 5) <= iss_longitude <= (MY_LNG + 5):
        if sunset >= hour >= sunrise:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(EMAIL, PASSWORD)
                connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject: Look up\n\nThe ISS is near to you.   \nYour ISS is now visible.")

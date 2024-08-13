import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 33.720577
MY_LONG = -116.215561
MY_EMAIL = "testingpythondev@gmail.com"
MY_PASSWORD = "krcbnhefmircnqkn"


def send_email():
    # establish SMTP commection and enable transport layer security(encryption)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:Look Up!\n\nThe International Space Station should be viewable, "
                                f"go outside and check!"
                            )

def within_range():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    return MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and  MY_LONG - 5 <= iss_longitude <= MY_LONG + 5

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        # turn off the formatting of the datetime piece of data
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    #call the relevant values from our JSON response
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    return time_now.hour >= sunset or time_now.hour <= sunrise

while True:
    #run every minute
    time.sleep(60)
    #If the ISS is close to my current position         # and it is currently dark
    if within_range() and is_night():
        # Then send me an email to tell me to look up.
        send_email()
        print("email sent")

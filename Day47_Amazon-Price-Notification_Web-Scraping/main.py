import smtplib
import os
import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
from dotenv import load_dotenv

load_dotenv()

PYTHONIOENCODING="UTF-8"
AMAZON_TEST_SITE = "https://appbrewery.github.io/instant_pot/"
AMAZON_LIVE_URL = "https://www.amazon.com/Garmin-Multisport-Smartwatch-Flashlight-Capability/dp/B0BYFDZ6BM?th=1"
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
REQUEST_HEADERS= {
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8,jv;q=0.7,eu;q=0.6",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}
#------------GET HTML TEXT----------------------#

#---- ADD HEADERS------#
# Also, it will make your request look (slightly) more human and less like a bot. Headers include data that is sent over
# by a browser rather than a script. many web servers like Amazon's may block requests they think originate from bots.
response = requests.get(url=AMAZON_LIVE_URL, headers=REQUEST_HEADERS)
amazon_page = response.text
# print(amazon_page)

#---------------PARSE TEXT FOR PRICE AND DESCRIPTION-------------------#
soup = BeautifulSoup(amazon_page,"html.parser")
# print(soup.prettify())

# Find the HTML element containing the  price
price = soup.find(class_="a-offscreen").get_text()
# Removing the dollar sign and conv to float
price_float = float(price.split("$")[1])
print(price_float)

#fint the HTML element containing the product name
product_title = soup.find(id="productTitle").getText().strip()
# print(product_title)
#split the text into lines and remove empty lines
lines = product_title.splitlines()
cleaned_lines = [line.strip() for line in lines if line.strip()]
#join the lines again into a single string. joins them by a space
formatted_product_title = ' '.join(cleaned_lines)
print(formatted_product_title)


#--------------IF BELOW THRESHOLD; SEND EMAIL NOTIFICATION--------------------#
price_alert = False

#Threshold price limit is set manually at $100
if price_float < 699:
    price_alert = True

# if price_alert flag was switched above, send notification email
EMAIL_CONTENT =(f"Subject:***Amazon Price Notification Alert***\n\n"
                f"{formatted_product_title}\nNow: {price_float}\n{AMAZON_LIVE_URL}").encode('utf-8')
if price_alert:
    with smtplib.SMTP(os.environ.get("SMTP_ADDRESS")) as connection:
        #start transmission layer security
        connection.starttls()
        #pull connection password and email from the .env file
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        #Send email context
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="testemail@gmail.com",
            msg=EMAIL_CONTENT)

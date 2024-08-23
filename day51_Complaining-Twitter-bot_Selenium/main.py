import os
from dotenv import load_dotenv
from InternetSpeedTwitterBot import InternetSpeedTwitterBot
from time import sleep

# connect to the .env file to pull the confidential keys
load_dotenv()

CHROME_DRIVER_PATH = "/users/Kiernan/Development/chromedriver"
TWITTER_USERNAME = os.environ.get("TWITTER_ACCT")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")


# Outside of the class, initialise the object and call the two methods in order.
# Where you first get the internet speed and then tweet at the provider.
bot = InternetSpeedTwitterBot()
# bot.get_internet_speed()
# sleep(10)
#check the speed against promised amounts and tweet if needed
bot.tweet_at_provider(user=TWITTER_USERNAME, password=TWITTER_PASSWORD, message= f"Hey {bot.internet_provider}, why is my internet speed {bot.down}down/{bot.up}up, when I pay for {bot.PROMISED_DOWN}down/{bot.PROMISED_UP}up?"
)
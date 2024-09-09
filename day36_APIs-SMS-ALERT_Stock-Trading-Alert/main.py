import requests
import os
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = ""
STOCK_API_KEY = ""  # alphavantage

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_API = ""
TWILIO_ACCOUNT_SID =""
TWILIO_AUTH_TOKEN=""
TWILIO_NUMBER= ""

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
stock_params= {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey":STOCK_API_KEY, #alphavantage
    "outputsize":"compact"
}
# GET YESTERDAY'S CLOSING STOCK PRICE
response = requests.get(url=STOCK_ENDPOINT,params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
# value for key:value, from data(dict).items()
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
# print(f"Yesterday's closing price was: ${yesterday_closing_price}.")

# GET THE DAY BEFORE YESTERDAY'S CLOSING STOCK PRICE
day_before_data = data_list[1]
day_before_closing_price = float(day_before_data["4. close"])
# print(f"The closing price of the day before yesterday was: ${day_before_closing_price}.")

#FIND THE POSITIVE DIFFERENCE BETWEEN THE TWO ABS()
close_price_diff = yesterday_closing_price - day_before_closing_price
rounded_close_price_diff = round(close_price_diff,1)
if close_price_diff > 0:
    stock_direction = "🔺"
else:
    stock_direction = "🔻"

# print(f"The closing price difference was: ${close_price_diff}")
#WORK OUT THE VALUE OF 5% OF YESTERDAY'S CLOSING STOCK PRICE
five_pct_diff = (abs(close_price_diff) / yesterday_closing_price) * 100
# print(f"A five percent value of yesterday's price would equal: ${five_pct_diff}.")


## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
#HINT 1: Think about using the Python Slice Operator
if five_pct_diff > 1:
    news_params= {
        "apiKey": NEWS_API_KEY,
        "qInTitle":COMPANY_NAME
    }
    news_response = requests.get(url=NEWS_ENDPOINT,params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    # print(three_articles)


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
formatted_articles = [f"""{STOCK}: {stock_direction}{rounded_close_price_diff}\n
Headline: {article['title']}.\n
Brief: {article['description']}."""
                      for article in three_articles]
# print(summary)

# SEND EACH ARTICLE AS A SEPARATE MESSAGE W/ TWILIO

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_=TWILIO_NUMBER,
        to="+17608775865"
    )



import requests
import os
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = "8c4dcca27fe94e28aa801ede1b44b094"
STOCK_API_KEY = "67VWK7QXR59LF7WP"  # alphavantage

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_API = "a18c00ccd8d3cf6b5468b332d245100d"
TWILIO_ACCOUNT_SID ="AC2d8e7a362559b0a4714a984bea8e22b0"
TWILIO_AUTH_TOKEN="5ee41feff9d329f473f27e2d8d16fd8b"
#TWILIO Number: +18335060881

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
close_price_diff = abs(yesterday_closing_price-day_before_closing_price)
# print(f"The closing price difference was: ${close_price_diff}")
#WORK OUT THE VALUE OF 5% OF YESTERDAY'S CLOSING STOCK PRICE
five_pct_diff = (close_price_diff / yesterday_closing_price) * 100
# print(f"A five percent value of yesterday's price would equal: ${five_pct_diff}.")


## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator
if five_pct_diff > close_price_diff:
    #TODO: ADJUST THIS BACK TO < after testing
    news_params= {
        "X-Api-Key": "8c4dcca27fe94e28aa801ede1b44b094",
        "country":"us"
        }
    response = requests.get(url="https://newsapi.org/v2/everything",params=news_params)
    response.raise_for_status()
    data =response.json
    print(data)



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


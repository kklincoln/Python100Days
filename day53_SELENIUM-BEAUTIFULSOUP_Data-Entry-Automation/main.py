import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from time import sleep

load_dotenv()

FORM_URL = os.environ.get("FORM_URL")
GSHEET_URL = os.environ.get("GSHEET_URL")
ZILLOW_PAGE = "https://appbrewery.github.io/Zillow-Clone/"
REQUEST_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8,jv;q=0.7,eu;q=0.6",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

#provide user agent and accepted languages in a header day47
#------------------------------------------------GET HTML DATA ---------------------------------------------------#
response = requests.get(url=ZILLOW_PAGE, headers=REQUEST_HEADERS)
zillow_html = response.text
# print(zillow_html) #confirmed load

#--------------------------------------BEAUTIFUL SOUP TO SCRAPE THE LISTING DATA---------------------------------------#
soup = BeautifulSoup(zillow_html, "html.parser")

#----CREATE A LIST OF LINKS FOR ALL OF THE LISTINGS SCRAPED-----------------------#
hyperlinks = soup.findAll(class_="StyledPropertyCardDataArea-anchor")
#list comprehension to parse list for hyperlinks
hyperlink_list = [hyperlink["href"] for hyperlink in hyperlinks]
# print(hyperlink_list) #prints a list associated with all of the hyperlinks


#----CREATE A LIST OF PRICING FOR ALL OF THE LISTINGS SCRAPED-----------------------#
#gets all the prices associated with the prices
prices = soup.findAll(class_="PropertyCardWrapper")
#list comprehension: creates a new list from the hyperlink list; REMOVE ANY + SYMBOLS, FORMAT: "$1,111"
price_list =[price.getText().split(" ")[0].split("/")[0].replace("\n","").replace("+","")
                  for price in prices]
# print(price_list) #prints list


#----CREATE A LIST OF ADDRESSES FOR ALL THE LISTINGS SCRAPED-----------------------#
addresses = soup.select(".StyledPropertyCardDataWrapper address")
address_list = [address.getText().strip() for address in addresses]
# print(address_list) #prints list of addresses without extra whitespace


#------------------------------SELENIUM TO FILL THE FORM CREATED IN STEPS ABOVE----------------------------------------#
#------------establish a driver with auto-close turned off -----------------#
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options)
driver.get(url=FORM_URL)
sleep(2)
for i in range(len(prices)):
    #---------------populate address--------------------#
    address_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(address_list[i],Keys.TAB)
    sleep(1)
    #---------------populate price --------------------#
    price_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(price_list[i],Keys.TAB)
    sleep(1)
    #---------------populate hyperlink--------------------#
    hyperlink_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    hyperlink_input.send_keys(hyperlink_list[i],Keys.TAB)
    sleep(1)
    #---------------submit response-------------------#
    submit_btn = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_btn.click()
    sleep(2)
    #---------------click submit another response button---------------#
    submit_another_btn = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_btn.click()
    sleep(2)
driver.quit()
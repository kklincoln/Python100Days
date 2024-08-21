from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#connect to the chrome web driver and turn off auto close with detach
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# 1. Go to the game website and familiarise yourself with how it works:
# http://orteil.dashnet.org/experiments/cookie/ (classic version)
driver = webdriver.Chrome(chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# 2. Create a bot using Selenium and Python to click on the cookie as fast as possible.
cookie = driver.find_element(by=By.ID, value="cookie")
# cookie.click()
products = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
product = [product.get_attribute("id") for product in products]

# 3. Every 5 seconds, check the right-hand pane to see which upgrades are affordable and purchase the most expensive one.
# You'll need to check how much money (cookies) you have against the price of each upgrade.
# e.g. both Grandma and Cursor are affordable as we have 103 cookies, but Grandma is the more expensive one, so we'll
# purchase that instead of the cursor #iterate through the price array backwards
timeout = time.time() + 5 # 5 second intervals to click and update
five_min = time.time() + 60*5  # 5 minutes

#click loop
while True:
    cookie.click()

    # Every 5 seconds:
    if time.time() > timeout:
        # Get all upgrade <b> tags; <b> tags are associated with the price
        all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        item_prices = []

        # Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                #split the item that is linked to the product and get the second portion; e.g. cursor - 46; remove commas
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                #append the cost gathered into the item_prices list
                item_prices.append(cost)

        # Create dictionary of products and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = product[n]

        # Get count of my cookies; constantly updating
        money_element = driver.find_element(by=By.ID, value="money").text
        #if theres an amount more than 999, remove commas
        if "," in money_element:
            #remove the commas in thousand+ costs to store as int
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(by=By.ID, value=to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_s)
        break

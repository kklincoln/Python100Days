from selenium import webdriver
from selenium.webdriver.common.by import By

#keep chrome browser open after the program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

#initialize the driver so that we can use the selenium bridge to connect to Chrome
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.python.org")

#find element by class name
# price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_cents = driver.find_element(By.CLASS_NAME, value="a-price-fraction")
# print(f"The price is {price_dollar.text}{price_cents.text}")

search_bar =driver.find_element(By.NAME, value="q")
# print(search_bar.tag_name) #returns the tag type that the element is
# print(search_bar.get_attribute("placeholder")) #gets the placeholder text associated with the input box
# button = driver.find_element(By.ID,value="submit") #finds the element with the id of "submit" and then returns the size
# print(button.size)

#one of the easiest ways to find a particular element; a class of documentation-widget and an a href within it
# documentation_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(documentation_link.text)


#when all else fails, you can find an element with the XPATH; right click>inspect>right click>copy>copy xpath
donate_button = driver.find_element(By.XPATH, value='//*[@id="touchnav-wrapper"]/header/div/div[1]/a')
print(donate_button)


#this closes the browser, since we turned off the auto-close feature with the chrome_options code
# driver.close() #closes tab
driver.quit() #quits browser

#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
#
#
# #keep chrome browser open after the program finishes
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)
#
# #get webpage and objective is printing the article count number from the page title="Special:Statistics"
# driver = webdriver.Chrome(options=chrome_options)
#
# #navigate to webpage
# driver.get("https://en.wikipedia.org/wiki/Main_Page")
#
# #inspect by ID using #; select the "a"
# article_count = driver.find_element(By.CSS_SELECTOR, value="#articlecount a")
# # print(article_count.text)
# #-------------------DEMONSTRATING CLICKS-----------------------#
# # article_count.click()
#
#     #find element by link text
# all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")
# all_portals.click()
#
# #--------------------TYPING IN A SEARCH BAR----------------------#
# search_bar = driver.find_element(By.NAME, value="search")
# search_bar.send_keys("Python", Keys.ENTER)
#
# #---------------interact with the fake enrollment page https://secure-retreat-92358.herokuapp.com/----------------#
#
# #------------------------------------------#
#
# #------------------------------------------#
#
# #------------------------------------------#
# # driver.quit()
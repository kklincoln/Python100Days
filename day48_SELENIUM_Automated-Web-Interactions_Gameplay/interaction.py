from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#---------------interact with the fake enrollment page https://secure-retreat-92358.herokuapp.com/----------------#
#keep chrome browser open after the program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

#get webpage and objective is printing the article count number from the page title="Special:Statistics"
driver = webdriver.Chrome(options=chrome_options)

#navigate to webpage
driver.get("https://secure-retreat-92358.herokuapp.com/")

#inspect by NAME for the first name, last name, and email address blocks
fname_box = driver.find_element(By.NAME, value="fName")
fname_box.send_keys("test")
lname_box = driver.find_element(By.NAME, value="lName")
lname_box.send_keys("email")
email_box = driver.find_element(By.NAME, value="email")
email_box.send_keys("TestEmail@Gmail.com")

submit_btn = driver.find_element(By.CLASS_NAME, value="btn")
submit_btn.click()

#------------------------------------------#
# driver.quit()
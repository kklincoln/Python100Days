import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


load_dotenv()

FACEBOOK_EMAIL_ACCT = os.environ.get("FACEBOOK_EMAIL_ACCT")
FACEBOOK_PASSWORD = os.environ.get("FACEBOOK_PASSWORD")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")


#--------------------ESTABLISH A WEBDRIVER WITH THE AUTO-CLOSE FUNCTION TURNED OFF----------------------------#
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

#--------------------CONNECT TO TINDER PAGE ----------------------------#
driver = webdriver.Chrome(chrome_options)
driver.get("https://tinder.com/")

#-------------------- LOGIN WITH FACEBOOK ----------------------------#
#click login button
sleep(2)
login_button = driver.find_element(By.XPATH, value='//*[@id="q-612006581"]/div/div[1]/div/main/div[1]/div/div/div/div/div/header/div/div[2]/div[2]/a')
login_button.click()
sleep(1)
phone_login = driver.find_element(By.XPATH, value ='//*[@id="q1954579639"]/div/div/div/div[1]/div/div/div[2]/div[2]/span/div[3]/button/div[2]/div[2]')
phone_login.click()

sleep(5)
phone_entry = driver.find_element(By.XPATH,value='//*[@id="phone_number"]')
phone_entry.send_keys(PHONE_NUMBER)
phone_next_btn = driver.find_element(By.XPATH, value='/html/body/div[2]/div/div/div[1]/div/div[3]/button/div[2]/div[2]')
phone_next_btn.click()
sleep(30)
print("Sleeping for 10 seconds to allow entry of phone code.")
code_next_btn = driver.find_element(By.XPATH,value='/html/body/div[2]/div/div/div[1]/div/div[4]/button/div[2]/div[2]')
code_next_btn.click()
sleep(30)
print("Sleeping for 10 seconds to allow entry of email code.")
email_next_btn = driver.find_element(By.XPATH, value='//*[@id="q1954579639"]/div/div/div/div[1]/div/div[2]/div[2]/button/div[2]/div[2]/div')
email_next_btn.click()


# #--------------------CHANGE TO THE FACEBOOK WINDOW ----------------------------#
# sleep(2)
# base_window = driver.window_handles[0]
# fb_login_window = driver.window_handles[1]
# driver.switch_to.window(fb_login_window)
# #print out the facebook window title to confirm the switch
# print(driver.title)
#
# #-------------------- INPUT FACEBOOK LOGIN CREDENTIALS----------------------------#
# sleep(5)
# fb_email_prompt = driver.find_element(By.ID, value="email")
# fb_email_prompt.send_keys(FACEBOOK_EMAIL_ACCT)
# fb_password_prompt = driver.find_element(By.ID, value="pass")
# fb_password_prompt.send_keys(FACEBOOK_PASSWORD)
# fb_log_in_btn = driver.find_element(By.NAME, value="login")
# fb_log_in_btn.click()

#--------------------RETURN TO TINDER WINDOW AND DISMISS REQUESTS ----------------------------#
#switch back to the tinder window
# driver.switch_to.window(base_window)
# print(driver.title)
#
# #allow for page loading
# sleep(5)
#
# ##code below that is commented is only for initial running that allows for confirmation of tinder access to fb;
# fb_login = driver.find_element(By.XPATH, value ='//*[@id="q1954579639"]/div/div/div/div[1]/div/div/div[2]/div[2]/span/div[2]/button')
# fb_login.click()
# fb_confirm_login_window = driver.window_handles[2]
# driver.switch_to.window(fb_confirm_login_window)
# sleep(1)
# continue_login_btn = driver.find_element(By.XPATH, value='//*[@id="mount_0_0_33"]/div/div/div/div/div/div/div[1]/div[3]'
#                                                          '/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div[1]/'
#                                                          'div/div/div/div/div/div[1]/div/span/span')
# continue_login_btn.click()
# driver.switch_to.window(base_window)


# allow location access
allow_location_button = driver.find_element(By.XPATH, value='//*[@id="q1954579639"]/div/div/div/div/div[3]/button[1]/div[2]/div[2]')
allow_location_button.click()

# disallow notifications
disallow_notifications_button = driver.find_element(By.XPATH, value ='//*[@id="q1954579639"]/div/div/div/div/div[3]/button[2]/div[2]/div[2]/div')
disallow_notifications_button.click()

#-------------------- ----------------------------#
sleep(4)

like_btn = driver.find_element(By.XPATH,value='//*[@id="q-612006581"]/div/div[1]/div/main/div[2]/div/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button/span/span/svg/path')
dislike_btn = driver.find_element(By.XPATH, value='//*[@id="q-612006581"]/div/div[1]/div/main/div[2]/div/div/div/div[1]/div[1]/div/div[3]/div/div[2]/button/span/span/svg')

#tinder free tier capped at 100 per day; unless premium tier, use the following:

for n in range(100):
    #add one second delay
    sleep(2)
try:
    print("called")
    like_btn.click()
#catch match exceptions
except ElementClickInterceptedException:
    try:
        match_popup =  driver.find_element(By.CSS_SELECTOR, value="itsAMatch a")
        match_popup.click()
    #catches the exception of no page found yet; wait 2 seconds and retry
    except NoSuchElementException:
        sleep(2)

driver.quit()
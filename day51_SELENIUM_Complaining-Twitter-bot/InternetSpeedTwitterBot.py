import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os


# connect to Chrome driver and keep it open after finishing code/exceptions
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)





# In the init() method, create the Selenium driver and 2 other properties down and up .
class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options)
        self.down = 0
        self.up = 0
        self.internet_provider = "Testing"
        self.PROMISED_DOWN = 150
        self.PROMISED_UP = 10

    # Create two methods - get_internet_speed() and tweet_at_provider().
    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        sleep(10)
        #go to SpeedTest.Net and click the 'Go' button
        go_btn = self.driver.find_element(By.CLASS_NAME, value='js-start-test')
        go_btn.click()
        sleep(60)
        # self.down = self.driver.find_element(By.XPATH, value ='<span data-download-status-value="0.08" class="result-data-large number result-data-value download-speed">79.57</span>')
        # self.up = self.driver.find_element(By.XPATH, value='<span data-upload-status-value="0.07" class="result-data-large number result-data-value upload-speed">71.11</span>')

        self.down = self.driver.find_element(By.CLASS_NAME,value='download-speed').text
        self.up = self.driver.find_element(By.CLASS_NAME, value='upload-speed').text

    def tweet_at_provider(self, user, password, message):
        COMPLAINT = f"Hey {self.internet_provider}, why is my internet speed {self.down}down/{self.up}up, when I pay for {self.PROMISED_DOWN}down/{self.PROMISED_UP}up?"

        self.driver.get("https://x.com/")
        self.driver.maximize_window()
        sleep(2)
        #login
        login_btn = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a/div')
        login_btn.click()
        sleep(2)

        #pass login credentials
        email_entry = self.driver.find_element(By.XPATH, value ='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
        email_entry.send_keys(user)
        next_btn = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')
        next_btn.click()
        sleep(4)
        pass_entry = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        pass_entry.send_keys(password,Keys.ENTER)

        #close welcome window
        # sleep(2)
        # welcome_window = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/button/div')
        # welcome_window.click()

        #enter complaint in tweet box
        sleep(3)
        tweet_box = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')
        tweet_box.send_keys(COMPLAINT)
        sleep(2)

        post_btn = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span')
        post_btn.click()
        print("tweet completed")
        self.driver.quit()

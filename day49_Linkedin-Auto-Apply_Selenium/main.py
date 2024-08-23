import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

load_dotenv()

ACCOUNT_EMAIL = os.environ.get("LINKEDIN_EMAIL")
ACCOUNT_PASSWORD = os.environ.get("LINKEDIN_PASS")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")

#exit application if additional steps are required
def exit_application():
    #click exit button
    exit_btn = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
    exit_btn.click()

    time.sleep(2)
    #click discard application (doesn't save for later)
    # data - control - name = "discard_application_confirm_btn"
    discard_button = driver.find_element(By.CSS_SELECTOR, value='button[data-control-name="discard_application_confirm_btn"]')
    discard_button.click()

#keep chrome browser open after the program finishes/crashes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

#establish the web driver in Chrome and open the search for python developer, easy apply, past week
driver = webdriver.Chrome(chrome_options)
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4004943919&f_AL=true&f_TPR=r604800&f_WT=2"
           "&keywords=python%20developer"
           "&origin=JOB_SEARCH_PAGE_JOB_FILTER")
time.sleep(5)

#find the sign in button and log in automatically
nav_sign_in_btn = driver.find_element(By.CLASS_NAME, value="nav__button-secondary")
nav_sign_in_btn.click()
time.sleep(2)

email_entry = driver.find_element(By.ID, value="username")
email_entry.click()
email_entry.send_keys(ACCOUNT_EMAIL)
pass_entry = driver.find_element(By.ID, value="password")
pass_entry.click()
pass_entry.send_keys(ACCOUNT_PASSWORD)
submit_btn = driver.find_element(By.CLASS_NAME, value = "btn__primary--large")
submit_btn.click()

#you might see a CAPTCHA - solve manually
# input("Press Enter when you have solved the CAPTCHA")



# Get Listings
time.sleep(5)
all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")

# Apply for Jobs
for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(2)
    try:
        # Click Apply Button
        apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-s-apply button")
        apply_button.click()

        # Insert Phone Number
        # Find an <input> element where the id contains phoneNumber
        time.sleep(5)
        phone_entry = driver.find_element(by=By.CSS_SELECTOR, value="input[id*=phoneNumber]")
        if phone_entry.text == "":
            phone_entry.send_keys(Keys.CONTROL,"A",Keys.DELETE)
            phone_entry.send_keys(PHONE_NUMBER)
        # next_button = driver.find_element(By.CSS_SELECTOR, value="button[aria-label='Continue to next step']")
        # next_button.click()
        # review_app_btn = driver.find_element(By.CSS_SELECTOR, value="button[aria-label='Review your application']")
        # review_app_btn.click()

        # Check the Submit Button
        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
        if submit_button.get_attribute("aria-label") == "Continue to next step":
            exit_application()
            print("Complex application, skipped.")
            continue
        else:
            # Click Submit Button
            print("Submitting job application")
            submit_button.click()

        time.sleep(2)
        # Click Close Button
        close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        close_button.click()

    except NoSuchElementException:
        exit_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()

#     try:
#         #locate the apply button using the css selector that surrounds the button for easy apply
#         apply_button = driver.find_element(By.CSS_SELECTOR, value=".jobs-apply-button")
#         apply_button.click()
#         time.sleep(1)
#         #if phone number section is empty, populate
#         phone_entry = driver.find_element(By.CSS_SELECTOR, value="input[id*=phoneNumber]")
#         if phone_entry.text == "":
#             phone_entry.send_keys(Keys.CONTROL,"A",Keys.DELETE)
#             phone_entry.send_keys(PHONE_NUMBER)
#
#         #check the submit button exists:
#         submit_application_btn = driver.find_element(By.XPATH, value='//*[@id="ember1581"]')
#         if submit_application_btn.get_attribute("data-control-name") == "continue_unify":
#             exit_application()
#             print("Complex application, skipped.")
#             continue
#         else:
#             print("Submitting job application")
#             submit_application_btn.click()
#
#         time.sleep(2)
#         #click done on the application sent pop up window
#         popup_done_btn = driver.find_element(By.XPATH, value='//*[@id="ember1633"]/span')
#         popup_done_btn.click()
#
#     except NoSuchElementException:
#         exit_application()
#         print("No application button, skipped")
#         continue
# time.sleep(4)
# print("applications should have finished")
# # driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#objective: return a dictionary of upcoming events e.g. {0: {'time':'2020-08-28', 'name':'Pycon Somalia 2024'}, ...}
#keep chrome browser open after the program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.python.org")


#the time element lives inside LI, UL, Div class, div class="event-widget"
upcoming_event_times = driver.find_elements(By.CSS_SELECTOR,value=".event-widget time")
# for time in upcoming_event_times:
#     print(time.text)
#inside event-widget class, inside a list, then it's the "a" element
upcoming_event_names = driver.find_elements(By.CSS_SELECTOR,value=".event-widget li a")
# for name in upcoming_event_names:
#     print(name.text)
events = {}

for n in range(len(upcoming_event_times)):
    events[n] = {
        "time": upcoming_event_times[n].text,
        "name": upcoming_event_names[n].text
    }

print(events)



#objective: return a dictionary of upcoming events e.g. {0: {'time':'2020-08-28', 'name':'Pycon Somalia 2024'}, ...}
driver.quit() #quits browser
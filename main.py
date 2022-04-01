import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_driver_path = r"C:\selenium_web_driver\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service)

driver.get("https://tinder.com/")

# Delay by 2 seconds to allow page to load.
time.sleep(2)
log_in = driver.find_element(By.XPATH, "//span[text()='Log in']")
log_in.click()

time.sleep(2)
facebook_login = driver.find_element(By.XPATH, "//span[text()='Log in with Facebook']")
facebook_login.click()

time.sleep(2)
# move to pop up window
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)

time.sleep(5)

# log in to facebook
fb_login_text = driver.find_element(By.XPATH, '//*[@id="email"]')
fb_login_text.send_keys("FB_EMAIL")
fb_password_text = driver.find_element(By.XPATH, '//*[@id="pass"]')
fb_password_text.send_keys("FB_PASSWORD")

login_button = driver.find_element(By.XPATH, '//*[@id="loginbutton"]')
login_button.click()

# back to tinder window
driver.switch_to.window(base_window)

time.sleep(5)

# Allow location
allow_location = driver.find_element(By.XPATH, '//*[@id="c849239686"]/div/div[2]/div/div/div[1]/div[1]/button/span')
allow_location.click()

# Allow cookies
accept_cookies = driver.find_element(By.XPATH, '//*[@id="c-879141390"]/div/div/div/div/div[3]/button[1]/span')
accept_cookies.click()

# Disallow notifications
enable_notifications = driver.find_element(By.XPATH, '//*[@id="c-879141390"]/div/div/div/div/div[3]/button[1]/span')
enable_notifications.click()

# Tinder free tier only allows 100 "Likes" per day
for l in range(100):
    time.sleep(1)
    try:
        like = driver.find_element(By.XPATH,
                                   '//*[@id="c849239686"]/div/div[1]/div/div/main/div/div/div[1]/div/div[4]/div/div['
                                   '4]/button')
        like.click()
        # Catches the cases where there is a "Matched" pop-up in front of the "Like" button:
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, ".itsAMatch a")
            match_popup.click()

        # Catches the cases where the "Like" button has not yet loaded, so wait 2 seconds before retrying.
        except NoSuchElementException:
            time.sleep(2)

driver.quit()

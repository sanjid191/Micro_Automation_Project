from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open SauceDemo website
driver.get("https://www.saucedemo.com/")

# Enter credentials
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")

# Click login button
driver.find_element(By.ID, "login-button").click()

# Wait to see the result
time.sleep(3)

# Check if login successful
if "inventory.html" in driver.current_url:
    print(" Login successful!")
else:
    print(" Login failed!")

# Close browser
driver.quit()

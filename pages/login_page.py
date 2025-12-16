"""
Login Page Object Model
Contains all elements and methods related to login functionality
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    # Login Page class with locators and methods
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    # URLs
    LOGIN_URL = "https://www.saucedemo.com/"
    INVENTORY_URL = "https://www.saucedemo.com/inventory.html"
    
    def __init__(self, driver):
        # Initialize LoginPage with WebDriver instance
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open(self):
        # Navigate to the login page
        self.driver.get(self.LOGIN_URL)
        return self
    
    def enter_username(self, username):
        # Enter username in the username field
        username_field = self.wait.until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
        username_field.clear()
        username_field.send_keys(username)
        return self
    
    def enter_password(self, password):
        # Enter password in the password field
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login_button(self):
        # Click on the login button
        login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
        login_btn.click()
        return self
    
    def login(self, username, password):
        # Complete login process with credentials
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def is_login_successful(self):
        # Check if login was successful by verifying URL
        return self.INVENTORY_URL in self.driver.current_url
    
    def get_current_url(self):
        # Get current page URL
        return self.driver.current_url
    
    def is_error_message_displayed(self):
        # Check if error message is displayed
        try:
            error = self.driver.find_element(*self.ERROR_MESSAGE)
            return error.is_displayed()
        except:
            return False
    
    def get_error_message_text(self):
        # Get the error message text
        error = self.driver.find_element(*self.ERROR_MESSAGE)
        return error.text

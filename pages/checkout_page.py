# Checkout Page Object Model
# Contains all elements and methods related to checkout process
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    # Checkout Page class with locators and methods
    
    # Locators - Step 1: Your Information
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "input[type='submit'][value='Continue']")
    CANCEL_BUTTON = (By.ID, "cancel")
    
    # Locators - Step 2: Overview
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    
    # Locators - Complete Page
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    PONY_EXPRESS_IMAGE = (By.CLASS_NAME, "pony_express")
    
    # URLs
    CHECKOUT_STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
    CHECKOUT_STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
    CHECKOUT_COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"
    
    def __init__(self, driver):
        # Initialize CheckoutPage with WebDriver instance
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    # Step 1: Information Page Methods
    def is_checkout_info_page_loaded(self):
        # Check if checkout information page is loaded
        return self.CHECKOUT_STEP_ONE_URL in self.driver.current_url
    
    def enter_first_name(self, first_name):
        # Enter first name
        import time
        first_name_field = self.wait.until(
            EC.presence_of_element_located(self.FIRST_NAME_INPUT)
        )
        first_name_field.clear()
        time.sleep(0.1)
        first_name_field.send_keys(first_name)
        time.sleep(0.1)
        return self
    
    def enter_last_name(self, last_name):
        # Enter last name
        import time
        last_name_field = self.driver.find_element(*self.LAST_NAME_INPUT)
        last_name_field.clear()
        time.sleep(0.1)
        last_name_field.send_keys(last_name)
        time.sleep(0.1)
        return self
    
    def enter_postal_code(self, postal_code):
        # Enter postal code
        import time
        postal_field = self.driver.find_element(*self.POSTAL_CODE_INPUT)
        postal_field.clear()
        time.sleep(0.1)
        postal_field.send_keys(postal_code)
        time.sleep(0.1)
        return self
    
    def fill_checkout_information(self, first_name, last_name, postal_code):
        # Fill all checkout information fields
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self
    
    def click_continue(self):
        # Click continue button
        import time
        
        # Wait a bit to ensure all fields are filled
        time.sleep(0.5)
        
        # Check for any error messages
        try:
            error = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            if error.is_displayed():
                print(f"ERROR FOUND: {error.text}")
                raise Exception(f"Cannot continue - Error: {error.text}")
        except:
            pass
        
        continue_btn = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )
        
        # Print current values before clicking
        try:
            first = self.driver.find_element(*self.FIRST_NAME_INPUT).get_attribute("value")
            last = self.driver.find_element(*self.LAST_NAME_INPUT).get_attribute("value")
            postal = self.driver.find_element(*self.POSTAL_CODE_INPUT).get_attribute("value")
            print(f"Before click - First: '{first}', Last: '{last}', Postal: '{postal}'")
        except:
            pass
        
        continue_btn.click()
        time.sleep(2)  # Wait for navigation
        
        return self
    
    def click_cancel(self):
        # Click cancel button
        import time
        cancel_btn = self.wait.until(
            EC.element_to_be_clickable(self.CANCEL_BUTTON)
        )
        # Use JavaScript click as backup
        self.driver.execute_script("arguments[0].click();", cancel_btn)
        time.sleep(2)  # Wait for navigation back to cart
        return self
    
    # Step 2: Overview Page Methods
    def is_checkout_overview_page_loaded(self):
        # Check if checkout overview page is loaded
        return self.CHECKOUT_STEP_TWO_URL in self.driver.current_url
    
    def get_item_total(self):
        # Get item total from overview page
        item_total_elem = self.driver.find_element(*self.ITEM_TOTAL)
        # Extract number from "Item total: $XX.XX"
        total_text = item_total_elem.text.replace('Item total: $', '')
        return float(total_text)
    
    def get_tax(self):
        # Get tax amount from overview page
        tax_elem = self.driver.find_element(*self.TAX_LABEL)
        # Extract number from "Tax: $X.XX"
        tax_text = tax_elem.text.replace('Tax: $', '')
        return float(tax_text)
    
    def get_total(self):
        # Get total amount from overview page
        total_elem = self.driver.find_element(*self.TOTAL_LABEL)
        # Extract number from "Total: $XX.XX"
        total_text = total_elem.text.replace('Total: $', '')
        return float(total_text)
    
    def get_items_count_in_overview(self):
        # Get number of items shown in overview
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def click_finish(self):
        # Click finish button to complete order
        finish_btn = self.driver.find_element(*self.FINISH_BUTTON)
        finish_btn.click()
        return self
    
    # Complete Page Methods
    def is_order_complete_page_loaded(self):
        # Check if order complete page is loaded
        return self.CHECKOUT_COMPLETE_URL in self.driver.current_url
    
    def get_complete_header_text(self):
        # Get the completion header text
        header = self.wait.until(
            EC.presence_of_element_located(self.COMPLETE_HEADER)
        )
        return header.text
    
    def get_complete_message_text(self):
        # Get the completion message text
        message = self.driver.find_element(*self.COMPLETE_TEXT)
        return message.text
    
    def is_success_image_displayed(self):
        # Check if success image is displayed
        try:
            image = self.driver.find_element(*self.PONY_EXPRESS_IMAGE)
            return image.is_displayed()
        except:
            return False
    
    def click_back_home(self):
        # Click back home button
        back_btn = self.driver.find_element(*self.BACK_HOME_BUTTON)
        back_btn.click()
        return self
    
    def get_current_url(self):
        # Get current page URL
        return self.driver.current_url

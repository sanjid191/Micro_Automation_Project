# Cart Page Object Model
# Contains all elements and methods related to shopping cart functionality
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    # Cart Page class with locators and methods
    
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove-']")
    CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    
    # URLs
    CART_URL = "https://www.saucedemo.com/cart.html"
    
    def __init__(self, driver):
        # Initialize CartPage with WebDriver instance
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_page_loaded(self):
        # Check if cart page is loaded
        import time
        time.sleep(0.5)  # Brief wait for page load
        return self.CART_URL in self.driver.current_url or "cart" in self.driver.current_url
    
    def get_cart_item_count(self):
        # Get number of items in cart
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def click_checkout(self):
        # Click on checkout button
        checkout_btn = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        # Use JavaScript click for reliability
        self.driver.execute_script("arguments[0].click();", checkout_btn)
        return self
    
    def click_continue_shopping(self):
        # Click on continue shopping button
        continue_btn = self.driver.find_element(*self.CONTINUE_SHOPPING_BUTTON)
        continue_btn.click()
        return self
    
    def remove_item_from_cart(self):
        # Remove first item from cart
        remove_btn = self.driver.find_element(*self.REMOVE_BUTTON)
        remove_btn.click()
        return self
    
    def get_item_prices(self):
        # Get all item prices from cart
        price_elements = self.driver.find_elements(*self.ITEM_PRICE)
        prices = []
        for price_elem in price_elements:
            # Remove '$' and convert to float
            price_text = price_elem.text.replace('$', '')
            prices.append(float(price_text))
        return prices
    
    def calculate_total_price(self):
        # Calculate total price of items in cart
        prices = self.get_item_prices()
        return sum(prices)
    
    def is_cart_empty(self):
        # Check if cart is empty
        return self.get_cart_item_count() == 0
    
    def get_current_url(self):
        # Get current page URL
        return self.driver.current_url

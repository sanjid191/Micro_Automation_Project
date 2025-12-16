# Products Page Object Model
# Contains all elements and methods related to product inventory and selection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductsPage:
    # Products/Inventory Page class with locators and methods
    
    # Locators
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    HAMBURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    # Product specific locators (dynamic)
    ADD_TO_CART_BUTTON_TEMPLATE = "button[id='add-to-cart-{}']"
    REMOVE_BUTTON_TEMPLATE = "button[id='remove-{}']"
    
    # Product names for easy reference
    PRODUCT_BACKPACK = "sauce-labs-backpack"
    PRODUCT_BIKE_LIGHT = "sauce-labs-bike-light"
    PRODUCT_BOLT_TSHIRT = "sauce-labs-bolt-t-shirt"
    PRODUCT_FLEECE_JACKET = "sauce-labs-fleece-jacket"
    PRODUCT_ONESIE = "sauce-labs-onesie"
    PRODUCT_TEST_ALLTHETHINGS_TSHIRT = "test.allthethings()-t-shirt-(red)"
    
    def __init__(self, driver):
        # Initialize ProductsPage with WebDriver instance
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_page_loaded(self):
        # Check if products page is loaded
        try:
            self.wait.until(
                EC.presence_of_element_located(self.INVENTORY_CONTAINER)
            )
            return True
        except:
            return False
    
    def get_page_title(self):
        # Get the page title
        return self.driver.title
    
    def add_product_to_cart(self, product_name):
        # Add a specific product to cart by product name
        add_button_selector = self.ADD_TO_CART_BUTTON_TEMPLATE.format(product_name)
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, add_button_selector))
        )
        add_button.click()
        return self
    
    def add_multiple_products_to_cart(self, product_names):
        # Add multiple products to cart
        for product in product_names:
            self.add_product_to_cart(product)
        return self
    
    def get_cart_item_count(self):
        # Get the number of items in cart from badge
        try:
            badge = self.driver.find_element(*self.SHOPPING_CART_BADGE)
            return int(badge.text)
        except:
            return 0
    
    def click_cart_icon(self):
        # Click on shopping cart icon
        cart_link = self.driver.find_element(*self.SHOPPING_CART_LINK)
        cart_link.click()
        return self
    
    def open_hamburger_menu(self):
        # Open the hamburger menu
        menu_button = self.wait.until(
            EC.element_to_be_clickable(self.HAMBURGER_MENU)
        )
        menu_button.click()
        return self
    
    def logout(self):
        # Perform logout
        self.open_hamburger_menu()
        logout_link = self.wait.until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        )
        logout_link.click()
        return self
    
    def is_product_added(self, product_name):
        # Check if product's 'Add to cart' button changed to 'Remove'
        remove_button_selector = self.REMOVE_BUTTON_TEMPLATE.format(product_name)
        try:
            self.driver.find_element(By.CSS_SELECTOR, remove_button_selector)
            return True
        except:
            return False
    
    def get_product_count(self):
        # Get total number of products displayed
        products = self.driver.find_elements(*self.PRODUCT_ITEMS)
        return len(products)

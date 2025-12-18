import pytest
import time
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestSauceDemo:
    
    @pytest.mark.login
    @pytest.mark.smoke
    @pytest.mark.order(1)
    def test_01_login_with_valid_credentials(self, driver, valid_credentials):
        # Initialize Page Objects
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        
        # Step 1: Open login page
        login_page.open()
        
        # Step 2 & 3: Login with valid credentials
        login_page.login(
            valid_credentials["username"], 
            valid_credentials["password"]
        )
        
        # Assertions
        assert login_page.is_login_successful(), "Login failed - URL does not contain inventory.html"
        assert "inventory.html" in login_page.get_current_url(), "URL validation failed"
        assert products_page.is_page_loaded(), "Products page not loaded"
        assert "Swag Labs" in products_page.get_page_title(), "Page title mismatch"
        
        print("✓ Login test passed successfully")
    
    
    @pytest.mark.order
    @pytest.mark.smoke
    @pytest.mark.order(2)
    def test_02_order_single_product(self, driver, valid_credentials, single_product, checkout_information):
        # Initialize Page Objects
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        
        # Step 1: Login
        login_page.open()
        login_page.login(valid_credentials["username"], valid_credentials["password"])
        assert products_page.is_page_loaded(), "Login failed"
        
        # Step 2: Add single product to cart
        products_page.add_product_to_cart(single_product)
        time.sleep(0.5)  # Allow product to be added
        
        # Assertion: Verify product added
        assert products_page.is_product_added(single_product), "Product not added to cart"
        assert products_page.get_cart_item_count() == 1, "Cart count is not 1"
        
        # Step 3: Go to cart
        products_page.click_cart_icon()
        time.sleep(1.5)  # Wait for cart page to load
        print(f"\n DEBUG - Current URL: {driver.current_url}")
        print(f"DEBUG - Expected URL: {cart_page.CART_URL}")
        assert cart_page.is_page_loaded(), f"Cart page not loaded. URL: {driver.current_url}"
        assert cart_page.get_cart_item_count() == 1, "Cart does not contain 1 item"
        
        # Step 4: Proceed to checkout
        cart_page.click_checkout()
        assert checkout_page.is_checkout_info_page_loaded(), "Checkout info page not loaded"
        
        # Step 5: Fill checkout information
        checkout_page.fill_checkout_information(
            checkout_information["first_name"],
            checkout_information["last_name"],
            checkout_information["postal_code"]
        )
        checkout_page.click_continue()
        
        time.sleep(2)  # Allow page transition
        
        # Debug: Print current URL
        print(f"\nCurrent URL after continue: {driver.current_url}")
        
        # Assertion: Verify overview page
        assert checkout_page.is_checkout_overview_page_loaded(), f"Checkout overview page not loaded. Current URL: {driver.current_url}"
        assert checkout_page.get_items_count_in_overview() == 1, "Overview shows incorrect item count"
        
        # Verify pricing
        item_total = checkout_page.get_item_total()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()
        calculated_total = round(item_total + tax, 2)
        assert abs(total - calculated_total) < 0.01, f"Total mismatch: {total} != {calculated_total}"
        
        # Step 6: Complete order
        checkout_page.click_finish()
        
        # Assertions: Verify order completion
        assert checkout_page.is_order_complete_page_loaded(), "Order complete page not loaded"
        assert "checkout-complete" in checkout_page.get_current_url(), "URL does not contain checkout-complete"
        
        complete_header = checkout_page.get_complete_header_text()
        assert "Thank you for your order!" in complete_header, f"Success message not found: {complete_header}"
        
        assert checkout_page.is_success_image_displayed(), "Success image not displayed"
        
        print("✓ Single product order test passed successfully")
    
    
    @pytest.mark.order
    @pytest.mark.smoke
    @pytest.mark.order(3)
    def test_03_order_multiple_products(self, driver, valid_credentials, multiple_products, checkout_information):
        # Initialize Page Objects
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        
        # Step 1: Login
        login_page.open()
        login_page.login(valid_credentials["username"], valid_credentials["password"])
        assert products_page.is_page_loaded(), "Login failed"
        
        # Step 2: Add multiple products to cart
        products_page.add_multiple_products_to_cart(multiple_products)
        
        # Assertions: Verify all products added
        expected_count = len(multiple_products)
        for product in multiple_products:
            assert products_page.is_product_added(product), f"Product {product} not added"
        
        cart_count = products_page.get_cart_item_count()
        assert cart_count == expected_count, f"Cart count mismatch: {cart_count} != {expected_count}"
        
        # Step 3: Go to cart
        products_page.click_cart_icon()
        assert cart_page.is_page_loaded(), "Cart page not loaded"
        
        cart_items = cart_page.get_cart_item_count()
        assert cart_items == expected_count, f"Cart items mismatch: {cart_items} != {expected_count}"
        
        # Step 4: Proceed to checkout
        cart_page.click_checkout()
        assert checkout_page.is_checkout_info_page_loaded(), "Checkout info page not loaded"
        
        # Step 5: Fill checkout information and continue
        checkout_page.fill_checkout_information(
            checkout_information["first_name"],
            checkout_information["last_name"],
            checkout_information["postal_code"]
        )
        checkout_page.click_continue()
        
        time.sleep(1)  # Allow page transition
        
        # Debug: Print current URL
        print(f"\nCurrent URL after continue: {driver.current_url}")
        
        # Assertion: Verify overview page
        assert checkout_page.is_checkout_overview_page_loaded(), f"Checkout overview page not loaded. Current URL: {driver.current_url}"
        
        overview_items = checkout_page.get_items_count_in_overview()
        assert overview_items == expected_count, f"Overview items mismatch: {overview_items} != {expected_count}"
        
        # Verify pricing calculations
        item_total = checkout_page.get_item_total()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()
        
        assert item_total > 0, "Item total should be greater than 0"
        assert tax > 0, "Tax should be greater than 0"
        
        # Allow small floating point difference
        calculated_total = round(item_total + tax, 2)
        assert abs(total - calculated_total) < 0.01, f"Total mismatch: {total} != {calculated_total}"
        
        # Step 6: Complete order
        checkout_page.click_finish()
        
        # Assertions: Verify order completion
        assert checkout_page.is_order_complete_page_loaded(), "Order complete page not loaded"
        assert "checkout-complete" in checkout_page.get_current_url(), "URL validation failed"
        
        complete_header = checkout_page.get_complete_header_text()
        assert "Thank you for your order!" in complete_header, "Success message validation failed"
        
        complete_message = checkout_page.get_complete_message_text()
        assert len(complete_message) > 0, "Complete message is empty"
        
        assert checkout_page.is_success_image_displayed(), "Success image not displayed"
        
        print(f"✓ Multiple products order test passed successfully ({expected_count} products)")
    
    
    @pytest.mark.cancel
    @pytest.mark.order(4)
    def test_04_order_cancel_scenario(self, driver, valid_credentials, multiple_products):
        # Initialize Page Objects
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        
        # Step 1: Login
        login_page.open()
        login_page.login(valid_credentials["username"], valid_credentials["password"])
        assert products_page.is_page_loaded(), "Login failed"
        
        # Step 2: Add products to cart
        products_page.add_multiple_products_to_cart(multiple_products)
        
        expected_count = len(multiple_products)
        assert products_page.get_cart_item_count() == expected_count, "Products not added correctly"
        
        # Step 3: Go to cart
        products_page.click_cart_icon()
        assert cart_page.is_page_loaded(), "Cart page not loaded"
        assert cart_page.get_cart_item_count() == expected_count, "Cart item count mismatch"
        
        # Step 4: Start checkout process
        cart_page.click_checkout()
        assert checkout_page.is_checkout_info_page_loaded(), "Checkout page not loaded"
        
        # Step 5: Cancel the checkout
        checkout_page.click_cancel()
        
        # Debug output
        print(f"\nAfter cancel - Current URL: {driver.current_url}")
        
        # Assertions: Verify cancellation behavior
        # Cancel should redirect back to cart
        current_url = driver.current_url
        assert "cart.html" in current_url or "inventory.html" in current_url, f"Not redirected properly after cancel. Current URL: {current_url}"
        assert "cart.html" in cart_page.get_current_url(), "URL does not contain cart.html"
        
        # Verify items still in cart
        assert cart_page.get_cart_item_count() == expected_count, "Items removed from cart after cancel"
        assert not cart_page.is_cart_empty(), "Cart should not be empty after cancel"
        
        # Verify order did not complete
        current_url = driver.current_url
        assert "checkout-complete" not in current_url, "Order should not be completed"
        assert "inventory" not in current_url, "Should not be redirected to products page"
        
        print("✓ Order cancel scenario test passed successfully")
    
    
    @pytest.mark.logout
    @pytest.mark.order(5)
    def test_05_logout_functionality(self, driver, valid_credentials):
        # Initialize Page Objects
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        
        # Step 1: Login
        login_page.open()
        login_page.login(valid_credentials["username"], valid_credentials["password"])
        
        # Assertion: Verify login successful
        assert products_page.is_page_loaded(), "Login failed"
        assert "inventory.html" in driver.current_url, "Not on products page"
        
        # Step 2: Logout
        products_page.logout()
        
        time.sleep(1)  # Allow logout to complete
        
        # Assertions: Verify logout successful
        assert driver.current_url == login_page.LOGIN_URL, "Not redirected to login page"
        assert "saucedemo.com" in driver.current_url, "URL validation failed"
        assert "inventory" not in driver.current_url, "Still on inventory page after logout"
        
        # Verify login form is visible (confirming we're on login page)
        try:
            driver.find_element(*login_page.LOGIN_BUTTON)
            login_form_visible = True
        except:
            login_form_visible = False
        
        assert login_form_visible, "Login form not visible after logout"
        
        print("✓ Logout functionality test passed successfully")


# Additional test class for edge cases (optional)
class TestSauceDemoEdgeCases:
    
    @pytest.mark.login
    def test_login_page_elements_visibility(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        
        # Assertions: Verify page elements
        assert driver.find_element(*login_page.USERNAME_INPUT).is_displayed(), "Username field not visible"
        assert driver.find_element(*login_page.PASSWORD_INPUT).is_displayed(), "Password field not visible"
        assert driver.find_element(*login_page.LOGIN_BUTTON).is_displayed(), "Login button not visible"
        
        print("✓ Login page elements visibility test passed")
    
    
    @pytest.mark.order
    def test_cart_price_calculation(self, login_as_standard_user, multiple_products):
        driver = login_as_standard_user
        products_page = ProductsPage(driver)
        cart_page = CartPage(driver)
        
        # Add products
        products_page.add_multiple_products_to_cart(multiple_products)
        products_page.click_cart_icon()
        
        # Assertions
        assert cart_page.is_page_loaded(), "Cart page not loaded"
        
        total_price = cart_page.calculate_total_price()
        assert total_price > 0, "Total price should be greater than 0"
        
        item_count = cart_page.get_cart_item_count()
        assert item_count == len(multiple_products), "Item count mismatch"
        
        print(f"✓ Cart price calculation test passed (Total: ${total_price})")

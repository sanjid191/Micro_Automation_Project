# Pytest Configuration File (conftest.py)
# Contains fixtures and setup/teardown logic for test execution
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    # Fixture to initialize and quit WebDriver for each test
    # Scope: function - creates new browser instance for each test
    # Setup: Initialize Chrome driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(15)  # Increased wait time
    
    # Provide driver to test
    yield driver
    
    # Teardown: Close browser after test
    driver.quit()


@pytest.fixture(scope="function")
def login_as_standard_user(driver):
    # Fixture to login as standard user before test execution
    # Returns logged-in driver ready for testing
    from pages.login_page import LoginPage
    
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    
    return driver


# Test Data Fixtures
@pytest.fixture
def valid_credentials():
    # Fixture providing valid login credentials
    return {
        "username": "standard_user",
        "password": "secret_sauce"
    }


@pytest.fixture
def checkout_information():
    # Fixture providing checkout form data
    return {
        "first_name": "John",
        "last_name": "Doe",
        "postal_code": "12345"
    }


@pytest.fixture
def single_product():
    # Fixture providing single product name
    from pages.products_page import ProductsPage
    return ProductsPage.PRODUCT_BACKPACK


@pytest.fixture
def multiple_products():
    # Fixture providing multiple product names
    from pages.products_page import ProductsPage
    return [
        ProductsPage.PRODUCT_BACKPACK,
        ProductsPage.PRODUCT_BIKE_LIGHT,
        ProductsPage.PRODUCT_BOLT_TSHIRT
    ]


# Pytest Hooks
def pytest_configure(config):
    # Add custom markers
    config.addinivalue_line(
        "markers", "login: Tests related to login functionality"
    )
    config.addinivalue_line(
        "markers", "order: Tests related to order placement"
    )
    config.addinivalue_line(
        "markers", "cancel: Tests related to order cancellation"
    )
    config.addinivalue_line(
        "markers", "logout: Tests related to logout functionality"
    )
    config.addinivalue_line(
        "markers", "smoke: Smoke tests for critical functionality"
    )

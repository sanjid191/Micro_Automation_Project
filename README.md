# SauceDemo Automation Project

Complete automation framework for testing https://www.saucedemo.com using Selenium, Python, and Pytest with OOP design pattern.

## 📁 Project Structure

```
Micro Projrct on automation/
├── pages/                      # Page Object Model classes
│   ├── __init__.py
│   ├── login_page.py          # Login page elements and methods
│   ├── products_page.py       # Products/Inventory page
│   ├── cart_page.py           # Shopping cart page
│   └── checkout_page.py       # Checkout process pages
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures and configuration
│   └── test_saucedemo.py      # Main test suite
├── reports/                    # Test reports (auto-generated)
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## ✅ Features Implemented

### 1. **Login Automation**

- Valid credentials login
- URL and page element validation
- Assertions for login success

### 2. **Single Product Order**

- Add one product to cart
- Complete checkout process
- Order completion validation

### 3. **Multiple Products Order**

- Add multiple products (3 products)
- Cart count validation
- Total price calculation
- Order success verification

### 4. **Order Cancellation**

- Add products to cart
- Cancel during checkout
- Verify redirect and cart state
- Ensure order didn't proceed

### 5. **Logout Functionality**

- Automated logout process
- Login page visibility verification
- URL validation after logout

## 🛠️ Technical Implementation

### Object-Oriented Programming (OOP)

- **LoginPage**: Handles login operations
- **ProductsPage**: Manages product selection and cart operations
- **CartPage**: Shopping cart management
- **CheckoutPage**: Complete checkout flow (info, overview, completion)

### Pytest Features

- **Fixtures**:

  - `driver` - WebDriver initialization and cleanup
  - `login_as_standard_user` - Pre-login fixture
  - `valid_credentials` - Test data fixture
  - `checkout_information` - Checkout data fixture
  - `single_product` & `multiple_products` - Product selection fixtures

- **Markers/Decorators**:
  - `@pytest.mark.login` - Login tests
  - `@pytest.mark.order` - Order placement tests
  - `@pytest.mark.cancel` - Cancellation tests
  - `@pytest.mark.logout` - Logout tests
  - `@pytest.mark.smoke` - Critical smoke tests
  - `@pytest.mark.order(n)` - Test execution order

### Assertions Used

✓ URL validation  
✓ Text validation  
✓ Element presence checks  
✓ Element visibility checks  
✓ Count validations  
✓ Price calculation validations  
✓ Page load validations

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
pytest --version
```

## ▶️ Running Tests

### Run All Tests

```bash
pytest tests/test_saucedemo.py -v
```

### Run Specific Test

```bash
pytest tests/test_saucedemo.py::TestSauceDemo::test_01_login_with_valid_credentials -v
```

### Run Tests by Marker

```bash
# Run only login tests
pytest tests/test_saucedemo.py -m login -v

# Run only order tests
pytest tests/test_saucedemo.py -m order -v

# Run smoke tests
pytest tests/test_saucedemo.py -m smoke -v
```

### Run Tests in Order

```bash
pytest tests/test_saucedemo.py -v --tb=short
```

### Generate HTML Report

```bash
pytest tests/test_saucedemo.py --html=reports/test_report.html --self-contained-html
```

### Run Tests in Parallel (Optional)

```bash
pytest tests/test_saucedemo.py -n 3 -v
```

## 📊 Test Reports

After running tests with `--html` flag, reports are generated in the `reports/` folder:

- **test_report.html** - Detailed HTML report with pass/fail status

## 📝 Test Credentials

**Valid User:**

- Username: `standard_user`
- Password: `secret_sauce`

**Checkout Info (Dummy Data):**

- First Name: `John`
- Last Name: `Doe`
- Postal Code: `12345`

## 🧪 Test Cases

| Test # | Test Name                            | Description                  | Markers      |
| ------ | ------------------------------------ | ---------------------------- | ------------ |
| 1      | test_01_login_with_valid_credentials | Login with valid credentials | login, smoke |
| 2      | test_02_order_single_product         | Order a single product       | order, smoke |
| 3      | test_03_order_multiple_products      | Order multiple products      | order, smoke |
| 4      | test_04_order_cancel_scenario        | Cancel order during checkout | cancel       |
| 5      | test_05_logout_functionality         | Logout from application      | logout       |

## 🎯 Assignment Requirements Met

✅ Login with valid credentials and assertions  
✅ Single product order with success verification  
✅ Multiple products order with count/total validation  
✅ Order cancellation scenario with redirect verification  
✅ Logout with login page confirmation  
✅ OOP implementation with Page Object classes  
✅ Pytest framework with fixtures  
✅ Pytest markers and decorators  
✅ Comprehensive assertions throughout  
✅ Optional: HTML test report generation

## 🔍 Key Highlights

1. **Page Object Model (POM)**: Clean separation of page elements and test logic
2. **Reusable Components**: Helper methods in page classes
3. **Pytest Fixtures**: Setup/teardown automation
4. **Explicit Waits**: WebDriverWait for reliable element interactions
5. **Comprehensive Assertions**: Multiple validation points in each test
6. **Test Independence**: Each test can run independently
7. **Clear Documentation**: Docstrings and comments throughout

## 🐛 Troubleshooting

**Issue**: ChromeDriver not found  
**Solution**: The project uses `webdriver-manager` which auto-downloads drivers

**Issue**: Tests failing due to timing  
**Solution**: Implicit wait is set to 10 seconds in conftest.py

**Issue**: Element not found  
**Solution**: Check if locators in page classes match current website structure

## 📧 Notes

- Tests run on Chrome browser by default
- Each test creates a fresh browser instance
- Virtual environment (.venv) is already set up
- All dependencies should already be installed

---

**Created for**: QA Harbor Automation Assignment 02  
**Website**: https://www.saucedemo.com  
**Framework**: Selenium + Python + Pytest with OOP

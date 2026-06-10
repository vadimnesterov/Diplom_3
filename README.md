# Diplom 3 — UI Autotests for Stellar Burgers

**Author:** Vadim Nesterov

---

## Project Description

This project contains a suite of UI autotests for the educational service **Stellar Burgers**.  
Tests are written in **Python + Pytest + Selenium** and use **Allure** for reporting.

The following key user scenarios are covered:

- Authentication (via a pre-created API user)
- Main page and header navigation checks
- Burger constructor and order creation
- Ingredient detail modal (open and close)
- Order feed counters and "In Progress" block

---

## Project Structure

```
Diplom_3/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── urls.py                         # Base URL + relative page and API paths
│   └── user_data.py                    # Test user data
│
├── helpers/
│   ├── common_api_helper.py            # Random string generator for unique test data (email, name, password)
│   ├── order_helper.py                 # Order number normalisation utility
│   └── user_api_helper.py             # API client: create, login, delete test users via requests
│
├── locators/
│   ├── constructor_page_locators.py    # Locators for constructor tabs, ingredients, drop area
│   ├── login_page_locators.py          # Locators for the login page
│   ├── main_page_locators.py           # Locators for the main page and header
│   └── order_feed_locators.py          # Locators for the order feed, counters, "In Progress" block
│
├── pages/
│   ├── base_page.py                    # Base WebDriver methods (open, waits, clicks, drag&drop)
│   ├── constructor_page.py             # Constructor: tabs, drag&drop, order button
│   ├── login_page.py                   # User authentication
│   ├── main_page.py                    # Main page + header + order creation
│   └── order_feed_page.py             # Order feed, counters, "In Progress" block
│
└── tests/
    ├── conftest.py                                       # Global fixtures: WebDriver (Chrome/Firefox), api_user
    ├── test_ingredient_modal_close.py                    # UI test: ingredient modal open and close
    ├── test_main_page_functionality.py                   # Main page and header functionality tests
    └── test_order_creation.py                            # End-to-end order creation and feed tests
```

---

## Tests

The `tests/` directory contains UI autotests written with **Pytest + Selenium**, run in two browsers: **Chrome and Firefox**.

### `conftest.py`
Global project fixtures:
- WebDriver initialisation (Chrome, Firefox)
- `api_user` fixture: creates a test user via API before the test, passes credentials (email, password, accessToken) to UI tests, and deletes the user afterwards.

Used by all test files.

---

### `test_ingredient_modal_close.py`
Tests for the ingredient detail modal.

Verifies:
- Modal opens when an ingredient is clicked
- Modal closes when the cross button is clicked

Tests:
- `test_ingredient_modal_closes_by_cross` (Chrome, Firefox)

---

### `test_main_page_functionality.py`
Tests for the core functionality of the main page and header.

Verifies:
- Navigation to the Constructor via the header
- Navigation to the Order Feed via the header
- Ingredient detail modal opens on click
- Ingredient counter increases after drag&drop into the constructor

Tests:
- `test_go_to_constructor_from_header`
- `test_go_to_order_feed_from_header`
- `test_ingredient_modal_opens_on_click`
- `test_ingredient_counter_increases_after_drag`

(All tests run in Chrome and Firefox)

---

### `test_order_creation.py`
End-to-end tests for order creation and the order feed.

Verifies:
- Order creation via UI after login
- "Completed all time" counter increases after a new order
- "Completed today" counter increases after a new order
- New order number appears in the **"In Progress"** block in the order feed

Tests:
- `test_new_order_increases_total_counter`
- `test_new_order_increases_today_counter`
- `test_order_number_appears_in_in_progress_block`

(All tests run in Chrome and Firefox)

---

### General Notes
- All tests are independent of each other.
- Test users are created via API.
- Both UI elements and backend integration (via the order feed and counters) are verified.

---

## Prerequisites

Before running the tests, make sure the following are installed and available on your `PATH`:

- **Python 3.10 or higher** — required for the `int | None` union type syntax used in page classes
- **Google Chrome** + **ChromeDriver** matching your installed Chrome version ([chromedriver.chromium.org](https://chromedriver.chromium.org/downloads))
- **Mozilla Firefox** + **GeckoDriver** matching your installed Firefox version ([github.com/mozilla/geckodriver](https://github.com/mozilla/geckodriver/releases))

Both `chromedriver` and `geckodriver` executables must be on your system `PATH` (or placed in the project root).

---

## Installation and Setup

### 1. Clone the repository and navigate to the project folder

```bash
git clone <repository_url>
cd Diplom_3
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running Tests

### Run all tests

```bash
pytest -v
```

### Run a specific test file

```bash
pytest tests/test_order_creation.py -v
```

### Run a single test

```bash
pytest tests/test_order_creation.py::TestOrderFeed::test_new_order_increases_total_counter -v
```

---

## Allure Reports

### Generate results

```bash
pytest --alluredir=allure_results
```

### Open the report

```bash
allure serve allure_results
```

---

## Known Limitations

The tests run against the public Stellar Burgers training backend
(`stellarburgers.education-services.ru`). If the backend is temporarily
unavailable, tests may fail with connection timeout or browser network
errors. These are external service availability failures — not defects in
the test code.

---

## Technologies Used

- Python 3.10+
- Pytest
- Selenium WebDriver
- Allure Pytest
- Requests

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def browser():
    # Initialize WebDriver (here using Chrome, change to desired browser)
    driver = webdriver.Safari()
    yield driver
    driver.quit()


def test_click_customers_list(browser):
    # Open the webpage
    browser.get("https://test-engineer-assignment-manager.testenv.impel.io/")

    # Wait for the "Customers" dropdown menu to become visible
    customers_dropdown = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Customers')]"))
    )

    # Click on the "Customers" dropdown menu
    customers_dropdown.click()

    # Find the "List" option under the dropdown menu
    list_option = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'List')]"))
    )

    # Click on the "List" option
    list_option.click()

    # Wait for the page to load
    WebDriverWait(browser, 10).until(EC.url_contains("/my-customer/"))

    # Assertion to verify that the correct page has been loaded
    assert "/my-customer/" in browser.current_url, "Failed to navigate to the Customers List page"

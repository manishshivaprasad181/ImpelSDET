import pytest
import requests
import time
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_inputs_from_file(file_path):
    input_data = {}
    with open(file_path, "r") as file:
        for line in file:
            # Ignore empty lines and lines starting with '#' (comments)
            if line.strip() == '' or line.strip().startswith('#'):
                continue
            # Split the line into key and value by the first '='
            parts = line.split('=', 1)
            # Ensure there are exactly two parts
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                input_data[key] = value
            else:
                print(f"Ignore invalid line: {line.strip()}")
    return input_data


@pytest.fixture(scope="module")
def browser():
    # Initialize Safari WebDriver
    driver = webdriver.Safari()
    return driver


def test_admin_login(browser):
    # Retrieve admin credentials from command line
    inputs = read_inputs_from_file('input_file.txt')
    login_page_url = inputs["login_page_url"]
    main_page_url = inputs["main_page_url"]
    admin_username = inputs["admin_username"]
    admin_password = inputs["admin_password"]

    browser.get(login_page_url)

    username_input = browser.find_element(By.ID, 'email')
    password_input = browser.find_element(By.ID, 'password')
    username_input.send_keys(admin_username)
    password_input.send_keys(admin_password)
    password_input.send_keys(Keys.RETURN)
    submit_button = browser.find_element(By.ID, 'submit')

    # Click on the "Submit" button
    submit_button.click()
    WebDriverWait(browser, 1).until(EC.url_to_be(main_page_url))

    assert browser.current_url == main_page_url, f"Login failed. Expected URL: {main_page_url}, Actual URL: {browser.current_url}"
    browser.get(main_page_url)
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
    list_option_link = list_option.get_attribute('href')

    # Click on the "List" option
    list_option.click()

    # Navigate to the "List" page using the extracted link
    browser.get(list_option_link)
    print(list_option_link)

    WebDriverWait(browser, 10).until(EC.url_contains("/my-customer/"))
    time.sleep(10)
    add_customer_button = browser.find_element(By.XPATH, "//a[contains(text(),'Add Customer')]")

    # Click on the "Add Customer" button
    add_customer_button.click()
    time.sleep(10)
    # Assertion to verify that the correct page has been loaded
    assert "/my-customer/" in browser.current_url, "Failed to navigate to the Customers List page"

if __name__ == '__main__':
    pytest.main()
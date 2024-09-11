import time
from io import StringIO
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def scrape_market_data(desired_server):
    # URL of the webpage with the dynamic table
    url = 'https:/Community/Market'

    # Set up the WebDriver (this example uses Chrome)
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get(url)

    # CSS Selector for the dropdown and the loading overlay
    dropdown_css = "div.form-group > select.form-control.form-control-rounded.form-control-sm"
    overlay_css = "div.loading"

    # Wait for any loading overlays to disappear
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, overlay_css)))
    except TimeoutException:
        print("Loading overlay did not disappear in time.")
        driver.quit()
        return None

    # Wait and click the dropdown to expand it
    try:
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_css)))
        dropdown.click()
    except TimeoutException:
        print("Dropdown element not found or not interactable.")
        driver.quit()
        return None

    # Wait for the specific option to be clickable and then click it
    option_xpath = f"//select[@class='form-control form-control-rounded form-control-sm']/option[text()='{desired_server}']"
    try:
        option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()
    except TimeoutException:
        print(f"Option '{desired_server}' not found or not interactable.")
        driver.quit()
        return None

    # Add a delay to allow the page to react to the new selection
    time.sleep(3)

    # Scrape the table with id 'items-table'
    try:
        table_xpath = "//table[@id='items-table']"
        table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        table_html = table.get_attribute('outerHTML')
        df = pd.read_html(StringIO(table_html))[0]
        print("Table data scraped successfully.\n")
        print("Processing Data...")
    except Exception as e:
        print(f"An error occurred while scraping the table: {e}")
        driver.quit()
        return None

    # Close the WebDriver
    driver.quit()

    return df

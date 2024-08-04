import time
import sys
import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (ElementClickInterceptedException, NoSuchElementException,
TimeoutException, WebDriverException, ElementNotInteractableException)


# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def safe_send_keys(driver, html_element, locator, keys):
    """
    Safely sends keys to an element identified by the given locator.

    :param driver: The Selenium WebDriver instance.
    :param html_element: The HTML element type (e.g., By.ID, By.CLASS_NAME).
    :param locator: The locator of the element.
    :param keys: The keys to be sent to the element.
    :return: True if the keys are successfully sent, False otherwise.
    """
    attempts = 0
    timeout = 10
    max_attempts = 3
    screenshot_name = None
    while attempts < max_attempts:
        try:
            # Locate the element first
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((html_element, locator))
            )
            element.click()  # Ensure the element is focused
            for key in keys:
                element.send_keys(key)
            logging.info("Successfully sent keys to element: %s", locator)
            return True

        except ElementNotInteractableException:
            logging.error("Element not interactable at the moment.")
            driver.get_screenshot_as_file(screenshot_name)
            attempts += 1
        except NoSuchElementException:
            driver.get_screenshot_as_file(screenshot_name)
            attempts += 1
        except TimeoutException:
            logging.error("Timeout waiting for element to be clickable. Selector: %s", locator)
            if screenshot_name is None:
                screenshot_name = f"{locator.replace('>', '_').replace(' ', '')}_debug_screenshot.png"
                driver.get_screenshot_as_file(screenshot_name)
                attempts += 1
        logging.info("Retry %s/%s for selector: %s", attempts, max_attempts, locator)
        logging.error("Failed to add keys after %s max_attempts. Selector: %s", max_attempts, locator)
        if attempts >= max_attempts:
            print("Max attempts reached, exiting script.")
            sys.exit(1)  # Exit the script with an error status
    return False


def safe_click(driver, html_element, locator):
    """
    Safely clicks on an element identified by the given locator.
    Retries the click operation for a specified number of attempts.
    Takes a screenshot on failure.
    Returns True if the click is successful, False otherwise.
    """
    attempts = 0
    timeout = 10
    max_attempts = 3
    screenshot_name = None
    while attempts < max_attempts:
        try:
            # Locate the element first
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((html_element, locator)))
            element.click()
            logging.info("Successfully clicked on the element with selector: %s", locator)
            return True  # Return True if the click is successful
        except (ElementClickInterceptedException, NoSuchElementException, TimeoutException, WebDriverException) as e:
            error_message = str(e)
            logging.error("Error encountered: %s. Selector: %s", error_message, locator)
            if screenshot_name is None:
                # Check if locator is a tuple and convert it to a string representation
                if isinstance(locator, tuple):
                    locator_str = "_".join(str(item) for item in locator).replace('>', '_').replace(' ', '')
                else:
                    locator_str = str(locator).replace('>', '_').replace(' ', '')
                    screenshot_name = f"{locator_str}_debug_screenshot.png"
                    driver.get_screenshot_as_file(screenshot_name)
            # Attempt to click using JavaScript
            try:
                element = driver.execute_script(f'return document.querySelector("{locator}");')
                driver.execute_script("arguments[0].click();", element)
                logging.info(
                    "Successfully clicked on the element with JavaScript. Selector: %s", locator
                )
                return True  # Return True if the JavaScript click is successful
            except WebDriverException as js_e:
                logging.error("JavaScript click failed: %s. Selector: %s", str(js_e), locator)
                attempts += 1
            if isinstance(e, (NoSuchElementException, TimeoutException)):
                attempts += 1
                logging.info("Retry %s/%s for selector: %s", attempts, max_attempts, locator)
                continue
                logging.error("Failed to click after %s max_attempts. Selector: %s", max_attempts, locator)
        if attempts >= max_attempts:
            print("Max attempts reached, exiting script.")
            sys.exit(1)  # Exit the script with an error status
    return False

def format_tags(tags):
    """
    Formats a comma-separated string of tags by adding a '#' to the front of each tag.

    :param tags_string: A comma-separated string of tags.
    :return: A formatted string with each tag prefixed by '#'.
    """
    return [tag.strip() for tag in tags.split(',')]

def safe_tags(driver, html_element, locator, tags):
    """
    Safely sends tags to an element identified by the given locator.

    :param driver: The WebDriver instance.
    :param html_element: The HTML element type.
    :param locator: The locator of the element.
    :param tags: The tags to be sent.
    :return: True if the tags are successfully sent, False otherwise.
    """
    attempts = 0
    timeout = 10
    max_attempts = 3
    screenshot_name = None
    formatted_tags = format_tags(tags)
    while attempts < max_attempts:
        try:
            # Locate the element first
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((html_element, locator))
            )
            element.click()  # Ensure the element is focused
            for key in formatted_tags:
                element.send_keys(key)
                print(key)
            logging.info("Successfully sent tags to element: %s", locator)
            return True
        except ElementNotInteractableException:
            logging.error("Element not interactive at the moment.")
            driver.get_screenshot_as_file(screenshot_name)
            attempts += 1
        except NoSuchElementException:
            attempts += 1
        except TimeoutException:
            logging.error("Timeout waiting for element to be clickable. Selector: %s", locator)
            if screenshot_name is None:
                screenshot_name = f"{locator.replace('>', '_').replace(' ', '')}_debug_screenshot.png"
                driver.get_screenshot_as_file(screenshot_name)
                attempts += 1
                logging.info("Retry %s/%s for selector: %s", attempts, max_attempts, locator)
                logging.error("Failed to add tags after %s max_attempts. Selector: %s", max_attempts, locator)
        if attempts >= max_attempts:
            print("Max attempts reached, exiting script.")
            sys.exit(1)  # Exit the script with an error status
    return False

def safe_click_javascript(driver, html_element, locator):
    """
    Safely clicks on an element identified by the given locator using JavaScript.

    :param driver: The WebDriver instance.
    :param html_element: The HTML element type.
    :param locator: The locator of the element.
    :return: True if the click is successful, False otherwise.
    """
    attempts = 0
    timeout = 10
    max_attempts = 3
    screenshot_name = None
    while attempts < max_attempts:
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                driver.find_element(html_element, locator)
            )
            # Wait for the upload button to be clickable
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((html_element, locator))
            )
            element.click()
            # Wait after click to ensure any subsequent actions have a valid state to proceed
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            logging.info("Successfully clicked on the element with selector: %s", locator)
            time.sleep(timeout)
            return True
        except (
            ElementClickInterceptedException,
            NoSuchElementException,
            TimeoutException,
            WebDriverException
        ) as e:
            error_message = str(e)
            logging.error("Error encountered: %s. Selector: %s", error_message, locator)
            if screenshot_name is None:
                # Check if locator is a tuple and convert it to a string representation
                if isinstance(locator, tuple):
                    locator_str = "_".join(str(item) for item in locator).replace('>', '_').replace(' ', '')
                else:
                    locator_str = str(locator).replace('>', '_').replace(' ', '')
                    screenshot_name = f"{locator_str}_debug_screenshot.png"
                    attempts += 1
                    driver.get_screenshot_as_file(screenshot_name)
            if isinstance(e, (NoSuchElementException, TimeoutException)):
                attempts += 1
                logging.info("Retry %s/%s for selector: %s", attempts, max_attempts, locator)
                continue
            logging.error("Failed to click after %s max_attempts. Selector: %s", max_attempts, locator)
        if attempts >= max_attempts:
            print("Max attempts reached, exiting script.")
            sys.exit(1)  # Exit the script with an error status
    return False

def copy_rumble_video_links(driver, html_element, locator, returned_data):
    attempts = 0
    timeout = 10
    max_attempts = 3
    screenshot_name = None
    while attempts < max_attempts:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((html_element, locator))
            )
            returned_data = element.get_attribute("value")
            logging.info("Successfully clicked on the element with selector: %s", locator)
            time.sleep(timeout)
            return True and returned_data
        except (ElementClickInterceptedException, NoSuchElementException, TimeoutException, WebDriverException) as e:
            error_message = str(e)
            logging.error("Error encountered: %s. Selector: %s", error_message, locator)
            if screenshot_name is None:
                # Check if locator is a tuple and convert it to a string representation
                if isinstance(locator, tuple):
                    locator_str = "_".join(str(item) for item in locator).replace('>', '_').replace(' ', '')
                else:
                    locator_str = str(locator).replace('>', '_').replace(' ', '')
                screenshot_name = f"{locator_str}_debug_screenshot.png"
                attempts += 1
            driver.get_screenshot_as_file(screenshot_name)
            if isinstance(e, (NoSuchElementException, TimeoutException)):
                attempts += 1
                logging.info("Retry %s/%s for selector: %s", attempts, max_attempts, locator)
                continue
        logging.error("Failed to click after %s max_attempts. Selector: %s", max_attempts, locator)
        if attempts >= max_attempts:
            print("Max attempts reached, exiting script.")
            sys.exit(1)  # Exit the script with an error status
    return False

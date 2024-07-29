import time
import random
import os
import getpass
import stat
import sys
import json
import logging
import cProfile
import pstats
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (ElementClickInterceptedException, NoSuchElementException,
TimeoutException, WebDriverException, ElementNotInteractableException)
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
from rumble_uploader_app.models import RumbleVideo

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# randomize wait times
random_wait_time = random.uniform(5, 8)
short_wait_time = random.uniform(1, 2)

# Rumble element selectors
rumble_sign_in_button = 'body > header > div > div > button.header-user.round-button.btn-grey'
rumble_username_field_input = '#login-username'
rumble_password_field_input = '#login-password'
rumble_login_button = '#loginForm > button.login-button.login-form-button.round-button.bg-green'
rumble_green_upload_button = 'button.header-upload'
rumble_upload_video_button = 'div.hover-menu.header-upload-menu.pop-show a.header-user-menu__menu-item[href="/upload.php"]'   #body > header > div > div > div.hover-menu.header-upload-menu.pop-show > a:nth-child(1)
rumble_upload_file = "input[type='file']"
rumble_video_title_input = '#title'
rumble_video_description_input = '#description'
rumble_video_categories_input = '#form > div > div.video-details.form-wrap > div.form-wrap > div:nth-child(1) > div > input.select-search-input'
rumble_video_secondary_categories_input = '#form > div > div.video-details.form-wrap > div.form-wrap > div:nth-child(2) > div > input.select-search-input'
rumble_video_tag_input = '#tags'
visibility_option_selector_public = "visibility-options > div:nth-child(1) > label"
visibility_option_selector_unlisted = "visibility-options > div:nth-child(2) > label"
visibility_option_selector_private = "#visibility-options > div:nth-child(3) > label"
rumble_upload_button = 'submitForm'
rumble_visibility_radio_button = '#visibility_public'
rumble_only_button = '#form2 > div > div.video-more.form-wrap.licensingOptions.quarters-wrap > div:nth-child(4) > div > a'
rumble_terms_and_conditions1 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(2) > label'    #'#crights'
rumble_terms_and_conditions2 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(3) > label'
rumble_submit_button = 'submitForm2'
rumble_direct_link = "direct"
rumble_embed_code = 'embed'
rumble_monetized_embed_code = 'monetized'
rumble_video_uploader_progress_selector = "#form2 > div > div.video-more.form-wrap.progress-wrap > div > div > span.top_percent"

def safe_send_keys(driver, html_element, locator, keys):
    attempts = 0
    timeout=10
    retries=3
    screenshot_name=None
    while attempts < retries:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((html_element, locator))
            )
            element.click()  # Ensure the element is focused
            for key in keys:
                element.send_keys(key)
                time.sleep(short_wait_time)
            logging.info("Successfully sent keys to element: %s", locator)
            return True

        except ElementNotInteractableException:
            logging.error("Element not interactable at the moment.")
            driver.get_screenshot_as_file(screenshot_name)
            attempts += 1
        except NoSuchElementException:
            attempts += 1
            return False
        except TimeoutException:
            logging.error("Timeout waiting for element to be clickable. Selector: %s", locator)
            if screenshot_name is None:
                screenshot_name = f"{locator.replace('>', '_').replace(' ', '')}_debug_screenshot.png"
            driver.get_screenshot_as_file(screenshot_name)
        attempts += 1
        logging.info("Retry %s/%s for selector: %s", attempts, retries, locator)
    logging.error("Failed to add keys after %s retries. Selector: %s", retries, locator)


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
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((html_element, locator)))
            element.click()
            logging.info("Successfully clicked on the element with selector: %s", locator)
            time.sleep(short_wait_time)
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
    retries = 3
    screenshot_name = None
    formatted_tags = format_tags(tags)
    while attempts < retries:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((html_element, locator))
            )
            element.click()  # Ensure the element is focused
            for key in formatted_tags:
                element.send_keys(key)
                print(key)
                time.sleep(short_wait_time)
            logging.info("Successfully sent tags to element: %s", locator)
            return True
        except ElementNotInteractableException:
            logging.error("Element not interactive at the moment.")
            driver.get_screenshot_as_file(screenshot_name)
            attempts += 1
        except NoSuchElementException:
            attempts += 1
            return False
        except TimeoutException:
            logging.error("Timeout waiting for element to be clickable. Selector: %s", locator)
            if screenshot_name is None:
                screenshot_name = f"{locator.replace('>', '_').replace(' ', '')}_debug_screenshot.png"
            driver.get_screenshot_as_file(screenshot_name)
        attempts += 1
        logging.info("Retry %s/%s for selector: %s", attempts, retries, locator)
    logging.error("Failed to add tags after %s retries. Selector: %s", retries, locator)

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
            WebDriverWait(driver, short_wait_time).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            logging.info("Successfully clicked on the element with selector: %s", locator)
            time.sleep(short_wait_time)
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
            attempts += 1
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
            time.sleep(short_wait_time)
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

def wait_for_element_to_disappear(driver, by, value, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located((by, value))
    )

def upload_to_rumble(rumble_video_script_serialized_data):
    """
    Uploads the rumble video to Rumble.
    """
    # Assuming rumble_video_script_serialized_data is the variable you're trying to parse
    if rumble_video_script_serialized_data:
        try:
            rumble_video_data = json.loads(rumble_video_script_serialized_data)
        except json.JSONDecodeError as e:
            logging.error("Failed to decode JSON from rumble_video_script_serialized_data: %s", e)
            rumble_video_data = {}  # Provide a default value or handle the error as needed
    else:
        logging.error("rumble_video_script_serialized_data is empty.")
        rumble_video_data = {}  # Provide a default value or handle the error as needed

    # Setup Chrome options
    options = webdriver.ChromeOptions()


    options.add_argument("--headless=new")  # Run Chrome in headless mode (no GUI).
    options.add_argument("--verbose")
    options.add_argument("--log-path=chromedriver.log")
    options.add_argument("--enable-logging")
    options.add_argument("--no-sandbox")  # Bypass OS security model,
    options.add_argument("--disable-gpu")  # Add this line if running in a headless environment
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.
    options.add_argument("--remote-debugging-port=8989")  # If you need to connect to the browser
    options.add_argument("--v=1")
    options.add_argument("--disable-extensions")  # Explicitly disable extensions,

    # Ensure ChromeDriver is up-to-date and specify options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Initialize the driver
    driver.get("https://rumble.com/upload.php")

    time.sleep(short_wait_time)  # Wait for 10 seconds

    env_file_path = r'D:\Proton Drive Backup\rahw_coding_mobile\aux_coding\rumble_uploader\rumble_uploader_V4\.env'
    load_dotenv(env_file_path)

    # Assuming rumble_account holds the account identifier
    rumble_account = rumble_video_data["rumble_account"]
    # Dynamically construct the environment variable names
    rumble_username_env_var = f'RUMBLE_USERNAME_{rumble_account}'
    rumble_password_env_var = f'RUMBLE_PASSWORD_{rumble_account}'

    # Access the environment variables to get the username and password
    rumble_username = os.getenv(rumble_username_env_var)
    rumble_password = os.getenv(rumble_password_env_var)

        # Strip any leading or trailing whitespace
    if rumble_password:
        rumble_password = rumble_password.replace('"', '')

    if rumble_username is None:
        logging.error("Rumble username environment variable not found.")
        # Handle the error as needed, e.g., provide a default value or exit the script

    if rumble_password is None:
        logging.error("Rumble password environment variable not found.")
        # Handle the error as needed, e.g., provide a default value or exit the script

    print(rumble_username)
    print(rumble_password)

    # Sign in to Rumble account

    # Click sign up button
    # safe_click(driver, By.CSS_SELECTOR, rumble_sign_in_button)

    # Input username and password
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_username_field_input, rumble_username)
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_password_field_input, rumble_password)
    safe_click(driver, By.CSS_SELECTOR, rumble_login_button)

    # # beginning of the upload process
    # safe_click(driver, By.CSS_SELECTOR, rumble_green_upload_button)
    # safe_click(driver, By.CSS_SELECTOR, rumble_upload_video_button)

    #  Upload the video file
    rumble_video_pk = rumble_video_data["rumble_video_pk"]
    video_title = rumble_video_data["videoTitle"]
    video_description = rumble_video_data["videoDescription"]
    video_tags = rumble_video_data["videoTags"]
    video_category = rumble_video_data["videoCategory"]
    video_secondary_category = rumble_video_data["videoSecondCategory"]
    rumble_video_file = rumble_video_data["rumble_video_file"]
    rumble_video_visibility_setting = rumble_video_data["rumble_video_visibility"]
    print(rumble_video_visibility_setting)

    # Rumble video visibility settings
    def rumble_visibility(visibility_setting):
        video_visibility_option_selection = None

        if visibility_setting == "Private":
            video_visibility_option_selection = visibility_option_selector_private
        elif visibility_setting == "Public":
            video_visibility_option_selection = visibility_option_selector_public
        elif visibility_setting == "Unlisted":
            video_visibility_option_selection = visibility_option_selector_unlisted
        return video_visibility_option_selection

    # Now call the function with the correct argument
    visibility_option = rumble_visibility(rumble_video_visibility_setting)

    # Define the file path where the video is stored
    file_path = '/code/static/media/videos'

    # Define the function to find the file
    def find_file(rumble_video_file, file_path):
        # Construct the absolute path
        rumble_video_relative_path = rumble_video_file.replace(
        "videos/", "")
        print(rumble_video_relative_path)
        absolute_path = os.path.join(file_path, rumble_video_relative_path)
        print(absolute_path)
        return absolute_path

    rumble_video_file_upload = find_file(rumble_video_file, file_path)

    # Configure logging
    logging.basicConfig(filename='rumble_uploader_error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')


# Assuming 'rumble_video_file_upload' contains the path to your file
    def check_file_permissions(rumble_video_file_upload):
        # Check if the file exists
        if not os.path.exists(rumble_video_file_upload):
            raise FileNotFoundError(f"The specified file does not exist: {rumble_video_file_upload}")

        # Check if the file is readable (has read permission)
        if not os.access(rumble_video_file_upload, os.R_OK):
            raise PermissionError(f"The file is not accessible for reading: {rumble_video_file_upload}")

        # If both checks pass, return True
        return True

    try:
        # Attempt to check permissions on the specified file
        if check_file_permissions(rumble_video_file_upload):
            print("File is ready for upload.")
            # Proceed with your file upload or processing logic here
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit the script with an error status
    except PermissionError as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit the script with an error status

    # Check if the file exists and is accessible
    if os.path.exists(rumble_video_file_upload) and os.access(rumble_video_file_upload, os.R_OK):
        print("File exists and is accessible. Proceeding with upload.")
    else:
        # Get and print the file's permissions
        file_permissions = os.stat(rumble_video_file_upload).st_mode
        print("File Permissions:")
        print("- Readable by owner:", bool(file_permissions & stat.S_IRUSR))
        print("- Writable by owner:", bool(file_permissions & stat.S_IWUSR))
        print("- Executable by owner:", bool(file_permissions & stat.S_IXUSR))
        print("- Readable by group:", bool(file_permissions & stat.S_IRGRP))
        print("- Writable by group:", bool(file_permissions & stat.S_IWGRP))
        print("- Executable by group:", bool(file_permissions & stat.S_IXGRP))
        print("- Readable by others:", bool(file_permissions & stat.S_IROTH))
        print("- Writable by others:", bool(file_permissions & stat.S_IWOTH))
        print("- Executable by others:", bool(file_permissions & stat.S_IXOTH))

        # Get and print the current user
        current_user = getpass.getuser()
        print("Selenium script is operating under user:", current_user)
        print("File not found or not accessible. Please check the file path and permissions.")

    print("New upload started!")
    driver.get("https://rumble.com/upload.php")

    time.sleep(short_wait_time)

    try:
        file_input = WebDriverWait(driver, short_wait_time).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        file_input.send_keys(rumble_video_file_upload)
        print(rumble_video_file_upload)
        time.sleep(short_wait_time)

    except Exception as e:
        print("Unable to upload file:", str(e))
        retry_limit = 3  # Number of retries
        retry_count = 0
        print(f"Attempt {retry_count + 1} failed with error: {str(e)}")

        retry_count += 1
        if retry_count >= retry_limit:
            print("Maximum retry attempts reached. Unable to upload file.")
            # Handle maximum retry failure case here
        else:
            time.sleep(short_wait_time)  # Wait before retrying

    # Input Rumble video data
    # Input Rumble video video_title
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_video_title_input, video_title)
    # Input Rumble video video_description
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_video_description_input, video_description)
    # Input Rumble video video_category
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_video_categories_input, video_category)
    # Input Rumble video video_secondary_category
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_video_secondary_categories_input, video_secondary_category)
    # Input Rumble video video_tags
    safe_tags(driver, By.CSS_SELECTOR, rumble_video_tag_input, video_tags)
    # Select Rumble video visibility setting
    print(visibility_option)
    safe_click(driver, By.CSS_SELECTOR, visibility_option)
    # Click the upload button
    safe_click_javascript(driver, By.ID, rumble_upload_button)
    # Click the rumble only button
    safe_click(driver, By.CSS_SELECTOR, rumble_only_button)
    #  Accept the terms and conditions 1
    safe_click(driver, By.CSS_SELECTOR, rumble_terms_and_conditions1)
    #  Accept the terms and conditions 2
    safe_click(driver, By.CSS_SELECTOR, rumble_terms_and_conditions2)
    #  Click sumbit upload button
    safe_click_javascript(driver, By.ID, rumble_submit_button)

    time.sleep(10)

    # Initialize variables before try blocks to ensure they have default values
    rumble_direct_link_copied_text = None
    rumble_embed_code_copied_text = None
    rumble_monetized_embed_copied_text = None

    copy_rumble_video_links(driver, By.ID, rumble_direct_link, rumble_direct_link_copied_text)
    print(rumble_direct_link_copied_text)

    copy_rumble_video_links(driver, By.ID, rumble_embed_code, rumble_embed_code_copied_text)
    print(rumble_embed_code_copied_text)

    copy_rumble_video_links(driver, By.ID, rumble_monetized_embed_code, rumble_monetized_embed_copied_text)
    print(rumble_monetized_embed_copied_text)

    time.sleep(short_wait_time)

    rumble_video_links_return_data = {
        "rumble_video_direct_link": rumble_direct_link_copied_text,
        "rumble_video_embed_code_link": rumble_embed_code_copied_text,
        "rumble_video_rumble_monetized_embed_link": rumble_monetized_embed_copied_text
    }

    def update_rumble_video_link(rumble_video_pk, rumble_video_links_return_data):
        try:
        # Retrieve the RumbleVideo object by its primary key (pk)
            rumble_video = RumbleVideo.objects.get(pk=rumble_video_pk)
            # Update the rumble_direct_link field
            rumble_video.rumble_direct_link = rumble_video_links_return_data["rumble_video_direct_link"]
            rumble_video.rumble_embed_code = rumble_video_links_return_data["rumble_video_embed_code_link"]
            rumble_video.rumble_monetized_embed = rumble_video_links_return_data["rumble_video_rumble_monetized_embed_link"]
            rumble_video.uploaded_to_rumble_success = True
            # Save the updated object
            rumble_video.save()
            print("Rumble video link updated successfully.")
        except ObjectDoesNotExist:
            print("Rumble video with the specified pk does not exist.")

    update_rumble_video_link(rumble_video_pk, rumble_video_links_return_data)

    # wait_for_upload_completion(driver, By.CSS_SELECTOR, rumble_video_uploader_progress_selector)

    driver.quit()
    if __name__ == "__upload_to_rumble__":
        pr = cProfile.Profile()
        pr.enable()
        upload_to_rumble(rumble_video_script_serialized_data)
        pr.disable()

        # Print profiling results
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

    print("Script executed successfully.")
    try:
        # Your script logic here
        # If everything goes well
        return "Upload successful"
    except Exception as e:
        # Handle any exceptions, possibly logging them
        return f"An error occurred: {str(e)}"
    # sys.exit(10)
    # Profile the upload_to_rumble function

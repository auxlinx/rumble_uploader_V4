import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rumble_uploader.settings')
django.setup()

from rumble_uploader_app.models import RumbleVideo

import time
import random
import os
import getpass
import stat
import sys
import json
import logging
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
# rumble_green_upload_button = 'body > header > div > div > button.header-upload'    #body > header > div > div > button.header-upload
rumble_upload_video_button = 'body > header > div > div > div.hover-menu.header-upload-menu > a:nth-child(1)'  #body > header > div > div > div.hover-menu.header-upload-menu.pop-show > a:nth-child(1)
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
rumble_terms_and_conditions1 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(2)'
rumble_terms_and_conditions2 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(3)'
rumble_submit_button = '#submitForm2'
rumble_direct_link = "direct"
rumble_embed_code = 'embed'
rumble_monetized_embed_code = 'monetized'


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
            element.send_keys(keys)
            logging.info("Successfully sent keys to element: %s", locator)
            return True
        except ElementNotInteractableException:
            logging.error("Element not interactable at the moment.")
            driver.get_screenshot_as_file(screenshot_name)
        except NoSuchElementException:
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
                EC.element_to_be_clickable((html_element, locator))
            )
            element.click()
            logging.info("Successfully clicked on the element with selector: %s", locator)
            time.sleep(short_wait_time)
            return True
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
            if isinstance(e, (NoSuchElementException, TimeoutException)):
                attempts += 1
                logging.info("Retry %s/%s for selector: %s", attempts, max_attempts, locator)
                continue
        logging.error("Failed to click after %s max_attempts. Selector: %s", max_attempts, locator)
        if attempts >= max_attempts:
            print("Max attempts reached, exiting script.")
            sys.exit(1)  # Exit the script with an error status
    return False


rumble_video_script_serialized_data = ({
            "rumble_account": "rumblevideos",
            "videoTitle": "test",
            "videoDescription": "test",
            "videoTags": "test",
            "videoCategory": "test",
            "rumble_video_visibility": "Private",
            "videoSecondCategory": "test",
            "rumble_video_file": "videos/test.mp4",
        })


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
    driver.get("https://rumble.com/")

    time.sleep(10)  # Wait for 10 seconds

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
    print(rumble_username)
    print(rumble_password)
    # Sign in to Rumble account
    # Click sign up button
    safe_click(driver, By.CSS_SELECTOR, rumble_sign_in_button)

    # Input username and password
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_username_field_input, rumble_username)
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_password_field_input, rumble_password)
    safe_click(driver, By.CSS_SELECTOR, rumble_login_button)

    time.sleep(10)  # Wait for 10 seconds

    # beginning of the upload process
    # safe_click(driver, By.CSS_SELECTOR, rumble_green_upload_button)
    safe_click(driver, By.CSS_SELECTOR, rumble_upload_video_button)

    #  Upload the video file
    rumble_video_pk = rumble_video_data["rumble_video_pk"]
    video_title = rumble_video_data["videoTitle"]
    video_description = rumble_video_data["videoDescription"]
    video_tags = rumble_video_data["videoTags"]
    video_category = rumble_video_data["videoCategory"]
    video_secondary_category = rumble_video_data["videoSecondCategory"]
    rumble_video_file = rumble_video_data["rumble_video_file"]
    rumble_video_visibility_setting = rumble_video_data["rumble_video_visibility"]

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

    time.sleep(1)

    try:
        file_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        file_input.send_keys(rumble_video_file_upload)
        print(rumble_video_file_upload)
        time.sleep(random_wait_time)

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
            time.sleep(5)  # Wait before retrying


    safe_click(driver, By.CSS_SELECTOR, rumble_upload_video_button)

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
    safe_send_keys(driver, By.CSS_SELECTOR, rumble_video_tag_input, video_tags)
    # Select Rumble video visibility setting
    safe_click(driver, By.CSS_SELECTOR, visibility_option)


    try:
        # Scroll using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, rumble_upload_button))

        # Wait for the upload button to be clickable
        upload_button = WebDriverWait(driver, random_wait_time).until(
            EC.element_to_be_clickable((By.ID, "submitForm"))
        )
        upload_button.click()
        # Attempt to click the button
        try:
            upload_button.click()
        except Exception as click_exception:
            print("Standard click failed, attempting JavaScript click:", str(click_exception))
            # If standard click fails, use JavaScript to click
            driver.execute_script("arguments[0].click();", upload_button)

        # Wait after click to ensure any subsequent actions have a valid state to proceed
        WebDriverWait(driver, random_wait_time).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
    except Exception as e:
        print("Unable to click on upload button:", str(e))
        # Consider capturing a screenshot for debugging
        driver.get_screenshot_as_file("debug_screenshot.png")

    try:
        rumble_only = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_only_button)))
        rumble_only.click()
        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to click on Rumble Only", str(e))

    try:
        terms_and_conditions1 = WebDriverWait(driver, random_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_terms_and_conditions1)))
        terms_and_conditions1.click()
        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to click on Terms and Conditions 1", str(e))

    try:
        terms_and_conditions2 = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_terms_and_conditions2)))
        terms_and_conditions2.click()
        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to click on Terms and Conditions 2", str(e))

    try:
        submit_button = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_submit_button)))
        submit_button.click()
        time.sleep(random_wait_time)
        print("Upload complete!")
    except Exception as e:
        print("Unable to click on Submit button", str(e))

    # Initialize variables before try blocks to ensure they have default values
    rumble_direct_link_copied_text = None
    rumble_embed_code_copied_text = None
    rumble_monetized_embed_copied_text = None

    try:
        copy_rumble_direct_link = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.ID, rumble_direct_link)))
        rumble_direct_link_copied_text = copy_rumble_direct_link.get_attribute("value")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        copy_rumble_embed_code = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.ID, rumble_embed_code)))
        rumble_embed_code_copied_text = copy_rumble_embed_code.get_attribute("value")
    except Exception as e:
        print(f"An error occurred: {e}")
    try:
        copy_rumble_monetized_embed_code = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.ID, rumble_monetized_embed_code)))
        rumble_monetized_embed_copied_text = copy_rumble_monetized_embed_code.get_attribute("value")
    except Exception as e:
        print(f"An error occurred: {e}")

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

    driver.quit()
    print("Script executed successfully.")
    try:
        # Your script logic here
        # If everything goes well
        return "Upload successful"
    except Exception as e:
        # Handle any exceptions, possibly logging them
        return f"An error occurred: {str(e)}"
    # sys.exit(10)

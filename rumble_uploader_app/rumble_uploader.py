import time
import random
import os
import getpass
import stat
import sys
import json
import logging
from pathlib import Path
from urllib.parse import unquote
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from seleniumbase import Driver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

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
rumble_green_upload_button = 'body > header > div > div > button.header-upload'
rumble_upload_video_button = 'body > header > div > div > div.hover-menu.header-upload-menu.pop-show > a:nth-child(1)'
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

    # Configure Chrome options
    # options.add_experimental_option("debuggerAddress", "localhost:8989")
    options.add_argument("--headless=new")  # Run Chrome in headless mode (no GUI).
    options.headless = True
    options.add_argument("--no-sandbox")  # Bypass OS security model, WARNING: NOT RECOMMENDED FOR PRODUCTION!
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.
    options.add_argument("--remote-debugging-port=8989")  # If you need to connect to the browser for debugging.
    options.add_argument("--verbose")
    options.add_argument("--log-path=chromedriver.log")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    options.add_argument("--window-size=1920,1080")

    # Ensure ChromeDriver is up-to-date and specify options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Initialize the driver
    driver.get("https://rumble.com/")

    env_file_path = r'D:\Proton Drive Backup\rahw_coding_mobile\aux_coding\rumble_uploader\rumble_uploader_V4\.env'
    load_dotenv(env_file_path)

    # Access the RUMBLE_USERNAME environment variable
    rumble_username = os.getenv('RUMBLE_USERNAME_randomrumblevideos')
    rumble_password = os.getenv('RUMBLE_PASSWORD_randomrumblevideos')

    # Sign in to Rumble account
    try:
        sign_in_button = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_sign_in_button)))
        sign_in_button.click()
    except TimeoutException:
        print("Sign-in button click failed")

    try:
        username_field = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_username_field_input)))
        username_field.send_keys(rumble_username)
        # print(rumble_username)
    except TimeoutException:
        print("TimeoutException: Element not found or not clickable")

    try:
        password_field = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_password_field_input)))
        password_field.send_keys(rumble_password)
        # print(rumble_password)
    except TimeoutException:
        print("TimeoutException: Element not found or not clickable")

    login_button = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_login_button)))
    login_button.click()
    print("Sign-in was successful")
    print(driver.title)

    time.sleep(3)

    green_upload_button = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_green_upload_button)))
    green_upload_button.click()

    time.sleep(random_wait_time)
    upload_video_button = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_upload_video_button)))
    upload_video_button.click()

    video_title = rumble_video_data["videoTitle"]
    video_description = rumble_video_data["videoDescription"]
    video_tags = rumble_video_data["videoTags"]
    video_category = rumble_video_data["videoCategory"]
    video_secondary_category = rumble_video_data["videoSecondCategory"]
    rumble_video_file = rumble_video_data["rumble_video_file"]
    rumble_video_visibility_setting = rumble_video_data["rumble_video_visibility"]

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

    # def find_file(rumble_video_file, file_path):
    #     # Construct the absolute path
    #     rumble_video_relative_path = rumble_video_file.replace(
    #     "videos//", ""
    #     )
    #     absolute_path = os.path.join("C:", file_path, rumble_video_relative_path).replace("/", "\\")
    #     print(absolute_path)
    #     return absolute_path

    # rumble_video_file_upload = find_file(rumble_video_file, file_path)
    # # print(rumble_video_file_upload)


    # Configure logging
    logging.basicConfig(filename='rumble_uploader_error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')


    # Assuming the file to upload is 'RecklessRegiment.mp4'
    rumble_video_file_upload = '/code/static/media/videos/RecklessRegiment.mp4'
    print(rumble_video_file_upload)
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

        # Proceed with Selenium file upload
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

    # while True:
    print("New upload started!")
    driver.get("https://rumble.com/upload.php")

    time.sleep(1)

    try:
        # file_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_upload_file)))
        file_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        file_input.send_keys(rumble_video_file_upload)
        print(rumble_video_file_upload)
        # upload_button.click()
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

    try:
        video_title_input = WebDriverWait(driver, random_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_title_input)))
        video_title_input.send_keys(video_title)
        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to add Video Title", str(e))

    try:
        video_description_input = WebDriverWait(driver, random_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_description_input)))
        video_description_input.send_keys(video_description)
        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to add Video Description", str(e))

    try:
        video_categories_input = WebDriverWait(driver, random_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_categories_input)))
        video_categories_input.send_keys(video_category)
        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to add Video Category", str(e))

    try:
        video_secondary_categories_input = WebDriverWait(driver, random_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_secondary_categories_input)))
        video_secondary_categories_input.send_keys(video_secondary_category)
        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to add Video Secondary Category", str(e))

    try:
        video_tag_input = WebDriverWait(driver, random_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_tag_input)))
        video_tag_input.send_keys(video_tags)
        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to add Video Tag", str(e))

    try:
        # Wait for the visibility option to be clickable
        select_visibility_option = WebDriverWait(driver, random_wait_time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, visibility_option))
        )
        select_visibility_option.click()
    except Exception as e:
        print("Unable to click on the visibility option:", str(e))

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

    driver.quit()


    def generate_rumble_video_links(rumble_video_links_return_data):
        """
        Generate rumble video links and return them as JSON data.
        """
        # rumble_video_links_return_data = {
        #     "rumble_video_direct_link": rumble_direct_link_copied_text,
        #     "rumble_video_embed_code_link": rumble_embed_code_copied_text,
        #     "rumble_video_rumble_monetized_embed_link": rumble_monetized_embed_copied_text
        # }
        rumble_video_links_json_data = json.dumps(rumble_video_links_return_data)
        return rumble_video_links_json_data

    rumble_video_links_json_data = generate_rumble_video_links(rumble_video_links_return_data)

    print(rumble_video_links_json_data)

    sys.exit(10)

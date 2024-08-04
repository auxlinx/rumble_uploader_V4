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
from selenium.common.exceptions import ( NoSuchElementException, TimeoutException, WebDriverException)
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
# Import only necessary elements
from rumble_uploader_script_html_elements import (
    rumble_username_field_input,
    rumble_password_field_input,
    rumble_login_button,
    rumble_upload_video_button,
    rumble_upload_file,
    rumble_video_title_input,
    rumble_video_description_input,
    rumble_video_categories_input,
    rumble_video_secondary_categories_input,
    rumble_video_tag_input,
    visibility_option_selector_public,
    visibility_option_selector_unlisted,
    visibility_option_selector_private,
    rumble_upload_button,
    rumble_video_management_button_exclusive_selector,
    rumble_video_management_button_non_exclusive_selector,
    rumble_video_management_button_rumble_only_selector,
    rumble_terms_and_conditions1,
    rumble_terms_and_conditions2,
    rumble_submit_button,
    rumble_direct_link,
    rumble_embed_code,
    rumble_monetized_embed_code,
    rumble_video_uploader_progress_selector
)
from rumble_uploader_script_input_functions import safe_send_keys, safe_click, safe_tags, safe_click_javascript, copy_rumble_video_links
from rumble_uploader_app.models import RumbleVideo


# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# randomize wait times
random_wait_time = random.uniform(5, 8)
short_wait_time = random.uniform(1, 2)

def upload_to_rumble(rumble_video_script_serialized_data, headless=True):
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

    # Conditionally add the headless argument based on the parameter
    if headless:
        options.add_argument("--headless=new")  # Run Chrome in headless mode (no GUI).
        options.add_argument("--disable-gpu")  # Add this line if running in a headless environment

    # options.add_argument("--headless=new")  # Run Chrome in headless mode (no GUI).
    options.add_argument("--verbose")
    options.add_argument("--log-path=chromedriver.log")
    options.add_argument("--enable-logging")
    options.add_argument("--no-sandbox")  # Bypass OS security model,

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
    rumble_video_licensing_setting = rumble_video_data["rumble_video_licensing_options"]

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

    # Rumble video visibility settings
    def rumble_licensing_options(licensing_options):
        rumble_licensing_options_selection = None

        if licensing_options == "Rumble Video Management Exclusive":
            rumble_licensing_options_selection= rumble_video_management_button_exclusive_selector
        elif licensing_options == "Rumble Video Management Non Exclusive":
            rumble_licensing_options_selection= rumble_video_management_button_non_exclusive_selector
        elif licensing_options == "Rumble Video Management Rumble Only":
            rumble_licensing_options_selection= rumble_video_management_button_rumble_only_selector
        return rumble_licensing_options_selection

    # Now call the function with the correct argument
    licensing_option = rumble_licensing_options(rumble_video_licensing_setting)

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
    print(rumble_video_file_upload)

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

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        file_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        file_input.send_keys(rumble_video_file_upload)
        print(rumble_video_file_upload)
        time.sleep(random_wait_time)

    except TimeoutException as e:
        logger.error("Timeout while waiting for file input element: %s", str(e))
    except NoSuchElementException as e:
        logger.error(f"File input element not found: {str(e)}")
    except WebDriverException as e:
        logger.error(f"WebDriver error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        max_attempts = 3  # Number of retries
        retry_count = 0
        print(f"Attempt {retry_count + 1} failed with error: {str(e)}")

        retry_count += 1
        if retry_count >= max_attempts:
            print("Maximum retry attempts reached. Unable to upload file.")
            # Handle maximum retry failure case here
            sys.exit(1)  # Exit the script with an error status
        else:
            time.sleep(5)  # Wait before retrying

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
    safe_click(driver, By.CSS_SELECTOR, visibility_option)
    # Click the upload button
    safe_click_javascript(driver, By.ID, rumble_upload_button)
    # Click the rumble only button
    safe_click(driver, By.CSS_SELECTOR, licensing_option)
    #  Accept the terms and conditions 1
    safe_click(driver, By.CSS_SELECTOR, rumble_terms_and_conditions1)
    #  Accept the terms and conditions 2
    safe_click(driver, By.CSS_SELECTOR, rumble_terms_and_conditions2)
    #  Click sumbit upload button
    safe_click_javascript(driver, By.ID, rumble_submit_button)

    time.sleep(3)

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


# if __name__ == "__main__":
#     rumble_video_script_serialized_data = json.dumps(rumble_video_script_test_data)
#     upload_to_rumble(rumble_video_script_serialized_data)

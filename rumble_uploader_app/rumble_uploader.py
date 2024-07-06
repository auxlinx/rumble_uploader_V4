import time
import random
import os
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

# sys.exit(0)


# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv()

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
rumble_upload_file = '#Filedata'
rumble_video_title_input = '#title'
rumble_video_description_input = '#description'
rumble_video_categories_input = '#form > div > div.video-details.form-wrap > div.form-wrap > div:nth-child(1) > div > input.select-search-input'
rumble_video_secondary_categories_input = '#form > div > div.video-details.form-wrap > div.form-wrap > div:nth-child(2) > div > input.select-search-input'
rumble_video_tag_input = '#tags'
visibility_option_selector_public = "visibility-options > div:nth-child(1) > label"
visibility_option_selector_unlisted = "visibility-options > div:nth-child(2) > label"
visibility_option_selector_private = "#visibility-options > div:nth-child(3) > label"
rumble_upload_button = '#submitForm'
rumble_visibility_radio_button = '#visibility_public'
rumble_only_button = '#form2 > div > div.video-more.form-wrap.licensingOptions.quarters-wrap > div:nth-child(4) > div > a'
rumble_terms_and_conditions1 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(2)'
rumble_terms_and_conditions2 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(3)'
rumble_submit_button = '#submitForm2'
rumble_direct_link = '#direct'
rumble_embed_code = '#embed'
rumble_monetized_embed_code = '#monetized'

# Access the RUMBLE_USERNAME environment variable
rumble_username = os.getenv('random_rumblevideo_USERNAME')
rumble_password = os.getenv('random_rumblevideo__password')


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
    options.add_argument("--headless")  # Run Chrome in headless mode (no GUI).
    options.add_argument("--no-sandbox")  # Bypass OS security model, WARNING: NOT RECOMMENDED FOR PRODUCTION!
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.
    options.add_argument("--remote-debugging-port=8989")  # If you need to connect to the browser for debugging.
    options.add_argument("--verbose")
    options.add_argument("--log-path=chromedriver.log")

    # Ensure ChromeDriver is up-to-date and specify options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Initialize the driver
    driver.get("https://rumble.com/")

    # Sign in to Rumble account
    try:
        sign_in_button = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_sign_in_button)))
        sign_in_button.click()
    except TimeoutException:
        print("Sign-in button click failed")

    try:
        username_field = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_username_field_input)))
        username_field.send_keys(rumble_username)
    except TimeoutException:
        print("TimeoutException: Element not found or not clickable")

    try:
        password_field = WebDriverWait(driver, short_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_password_field_input)))
        password_field.send_keys(rumble_password)
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

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the static/media directory
    file_path = os.path.join(current_dir, 'static', 'media', 'videos')


    def find_file(rumble_video_file, file_path):
        # Construct the absolute path
        rumble_video_relative_path = rumble_video_file.replace(
        "videos//", ""
        )
        absolute_path = os.path.join(file_path, rumble_video_relative_path).replace("/", "\\")
        return absolute_path

    rumble_video_file_upload = find_file(rumble_video_file, file_path)
    # print(rumble_video_file_upload)

    # while True:
    print("New upload started!")
    driver.get("https://rumble.com/upload.php")

    time.sleep(1)

    try:
        file_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_upload_file)))
        file_input.send_keys(rumble_video_file_upload)

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
        upload_button = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_upload_button)))
        # print(upload_button.get_attribute('outerHTML'))
        upload_button.click()
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", upload_button)

        # Try clicking the button
        try:
            upload_button.click()
        except:
            # If click fails, use JavaScript to click
            driver.execute_script("arguments[0].click();", upload_button)

        time.sleep(random_wait_time)
    except Exception as e:
        print("Unable to click on upload button", str(e))


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


    try:
        copy_rumble_direct_link = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_direct_link)))
        copy_rumble_direct_link.click()
        rumble_direct_link_copied_text = copy_rumble_direct_link.text
        print(rumble_direct_link_copied_text)

    except Exception as e:
        print(f"An error occurred: {e}")


    try:
        copy_rumble_embed_code = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_embed_code)))
        rumble_embed_code_copied_text = copy_rumble_embed_code.text

    except Exception as e:
        print(f"An error occurred: {e}")


    try:
        copy_rumble_monetized_embed_code = WebDriverWait(driver, random_wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_monetized_embed_code)))
        rumble_monetized_embed_copied_text = copy_rumble_monetized_embed_code.text

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
    # def upload_success(is_success):
    #     """
    #     Print a success message if the upload is successful, otherwise print an error message and exit with an error code.
    #     """
    #     if is_success:
    #         print("Upload completed successfully.")
    #         sys.exit()  # Stops the script
    #     else:
    #         print("Upload failed.")
    #         sys.exit(1)  # Exits with an error


    # def perform_upload(data):
    #     """
    #     Placeholder for upload logic.
    #     Return True if upload succeeds, False otherwise.
    #     """
    #     return True  # Assuming upload is successful for demonstration


    # if __name__ == "__main__":
    #     if len(sys.argv) != 2:
    #         print("Usage: python rumble_uploader.py '< rumble_video_links_json_data>'")
    #         sys.exit(1)

    #     rumble_video_links_json_data = sys.argv[1]
    #     try:
    #         data = json.loads(rumble_video_links_json_data)
    #     except json.JSONDecodeError:
    #         print("Invalid JSON data.")
    #         sys.exit(1)

    #     # Assuming perform_upload returns a boolean indicating success
    #     upload_result = perform_upload(data)
    #     upload_success(upload_result)

    # if __name__ == "__main__":
    #     print("rumble_uploader.py is being run directly")
    # else:
    #     print(f"rumble_uploader.py is being imported by another module: {__name__}")

    sys.exit(10)

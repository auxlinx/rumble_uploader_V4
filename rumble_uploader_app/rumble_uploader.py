import time
import random
import os
import sys
import json
import logging
from pathlib import Path
from urllib.parse import unquote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from seleniumbase import Driver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv()

SELENIUM_WEBDRIVER_PATH = unquote(ChromeDriverManager().install())

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
rumble_upload_button = '#submitForm'
rumble_visibility_radio_button = '#visibility_public'
rumble_only_button = '#form2 > div > div.video-more.form-wrap.licensingOptions.quarters-wrap > div:nth-child(4) > div > a'
rumble_terms_and_conditions1 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(2)'
rumble_terms_and_conditions2 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(3)'
rumble_submit_button = '#submitForm2'
rumble_direct_link = '#direct'
rumble_embed_code = '#embed'
rumble_monetized_embed_code = '#monetized'
# Rumble account credentials
rumble_username = "randomrumblevideos@protonmail.com"
rumble_password = "XKpE@h!5%j#hTW"


#  unpacks json data
# Check if the script received the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python rumble_uploader.py '<json_data>'")
    sys.exit(1)

# The second argument is the serialized JSON string
serialized_data = sys.argv[1]

# # Deserialize the JSON string back into a Python dictionary
# rumble_video_data = json.loads(serialized_data)

# Assuming serialized_data is the variable you're trying to parse
if serialized_data:
    try:
        rumble_video_data = json.loads(serialized_data)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from serialized_data: {e}")
        rumble_video_data = {}  # Provide a default value or handle the error as needed
else:
    logging.error("serialized_data is empty.")
    rumble_video_data = {}  # Provide a default value or handle the error as needed

# Configure Chrome options
opt = Options()
opt.add_experimental_option("debuggerAddress", "localhost:8989")

# Initialize the driver
driver = Driver()
driver.get("https://rumble.com/")

# Sign in to Rumble account
try:
    sign_in_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_sign_in_button)))
    sign_in_button.click()
except TimeoutException:
    print("Sign-in button click failed")

try:
    username_field = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_username_field_input)))
    username_field.send_keys(rumble_username)
except TimeoutException:
    print("TimeoutException: Element not found or not clickable")

try:
    password_field = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_password_field_input)))
    password_field.send_keys(rumble_password)
except TimeoutException:
    print("TimeoutException: Element not found or not clickable")

login_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_login_button)))
login_button.click()
print("Sign-in was successful")
print(driver.title)

time.sleep(3)

green_upload_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_green_upload_button)))
green_upload_button.click()

time.sleep(random.uniform(5, 8))
upload_video_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_upload_video_button)))
upload_video_button.click()

# video_title = 'Deadpool & Wolverine | Old Bubs'
# video_description = 'Don’t think we can add another “and” to the title. #DeadpoolAndWolverine'
# video_tags = 'test34'
# video_category = 'Finance'
# video_secondary_category = 'History'
# rumble_video_file = r"C:\Users\auxil\Documents\rumble_script V3\static\media\videos\Deadpool&Wolverine-OldBubs.mp4"

video_title = rumble_video_data["videoTitle"]
video_description = rumble_video_data["videoDescription"]
video_tags = rumble_video_data["videoTags"]
video_category = rumble_video_data["videoCategory"]
video_secondary_category = rumble_video_data["videoSecondCategory"]
rumble_video_file = rumble_video_data["rumble_video_file"]
print(rumble_video_file)
rumble_video_file_path = str(Path(rumble_video_file))
print(rumble_video_file_path)

file_path = r"C:\Users\auxil\Documents\rumble_script V3\static\media"

def find_file(rumble_video_file, file_path):
    # Construct the absolute path
    rumble_video_relative_path = rumble_video_file.replace(
    "videos//", ""
)
    absolute_path = os.path.join(file_path, rumble_video_relative_path).replace("/", "\\")
    print(absolute_path)
    # Check if the file exists
    # if os.path.exists(absolute_path):
    # return absolute_path
    return r"{}".format(absolute_path.replace("\\", "\\\\"))

    # else:
    #     return f"File {rumble_video_relative_path} not found in {file_path}"


rumble_video_file_upload = find_file(rumble_video_file, file_path)
print(rumble_video_file_upload)


while True:
    print("New upload started!")
    driver.get("https://rumble.com/upload.php")

    time.sleep(1)

    # file_path =r"C:\Users\auxil\Documents\rumble_script V3\static\media\videos\"
                # C:\Users\auxil\Documents\rumble_script V3\static\media\videos\

    try:
        file_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_upload_file)))
        file_input.send_keys(rumble_video_file)
        print(rumble_video_file)
        time.sleep(random.uniform(5, 8))
        # break  # Exit loop if upload is successful

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
        break

    try:
        video_title_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_title_input)))
        print(video_title)
        video_title_input.send_keys(video_title)
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to add Video Title", str(e))
        break

    try:
        video_description_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_description_input)))
        print(video_description)
        video_description_input.send_keys(video_description)
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to add Video Description", str(e))
        break

    try:
        video_categories_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_categories_input)))
        video_categories_input.send_keys(video_category)
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to add Video Category", str(e))
        break

    try:
        video_secondary_categories_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_secondary_categories_input)))
        video_secondary_categories_input.send_keys(video_secondary_category)
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to add Video Secondary Category", str(e))
        break

    try:
        video_tag_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_video_tag_input)))
        video_tag_input.send_keys(video_tags)
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to add Video Tag", str(e))
        break

    try:
        upload_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_upload_button)))
        print(upload_button.get_attribute('outerHTML'))
        upload_button.click()
         # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", upload_button)
        
        # Try clicking the button
        try:
            upload_button.click()
        except:
            # If click fails, use JavaScript to click
            driver.execute_script("arguments[0].click();", upload_button)

        # time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to click on upload button", str(e))
        break

    try:
        rumble_only = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_only_button)))
        print(rumble_only.get_attribute('outerHTML'))
        rumble_only.click()
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to click on Rumble Only", str(e))
        break

    try:
        terms_and_conditions1 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, rumble_terms_and_conditions1)))
        terms_and_conditions1.click()
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to click on Terms and Conditions 1", str(e))
        break

    try:
        terms_and_conditions2 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_terms_and_conditions2)))
        terms_and_conditions2.click()
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print("Unable to click on Terms and Conditions 2", str(e))
        break

    try:
        submit_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_submit_button)))
        submit_button.click()
        time.sleep(random.uniform(5, 8))
        print("Upload complete!")
    except Exception as e:
        print("Unable to click on Submit button", str(e))
        break

    try:
        copy_rumble_direct_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_direct_link)))
        rumble_direct_link_copied_text = copy_rumble_direct_link.text
        # copy_rumble_direct_link = '#direct' = driver.find_element_by_css_selector('rumble_direct_link')
        # rumble_direct_link = copy_rumble_direct_link.text
    except Exception as e:
        print(f"An error occurred: {e}")
        break

    try: 
        copy_rumble_embed_code = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_embed_code)))
        rumble_embed_code_copied_text = copy_rumble_embed_code.text

    except Exception as e:
        print(f"An error occurred: {e}")
        break

    try: 
        copy_rumble_monetized_embed_code = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_monetized_embed_code)))
        rumble_monetized_embed_copied_text = copy_rumble_monetized_embed_code.text

    except Exception as e:
        print(f"An error occurred: {e}")
        break

    driver.quit()   

rumble_video_links_return_data = {
    "rumble_video_direct_link": rumble_direct_link_copied_text,
    "rumble_video_embed_code_link": rumble_embed_code_copied_text,
    "rumble_video_rumble_monetized_embed_link": rumble_monetized_embed_copied_text
}
json_data = json.dumps(rumble_video_links_return_data)

print(rumble_video_links_return_data)


def upload_success(is_success):
    if is_success:
        print("Upload completed successfully.")
        sys.exit()  # Stops the script
    else:
        print("Upload failed.")
        sys.exit(1)  # Exits with an error


def perform_upload(data):
    # Placeholder for upload logic
    # Return True if upload succeeds, False otherwise
    return True  # Assuming upload is successful for demonstration


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rumble_uploader.py '<json_data>'")
        sys.exit(1)

    json_data = sys.argv[1]
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        print("Invalid JSON data.")
        sys.exit(1)

    # Assuming perform_upload returns a boolean indicating success
    upload_result = perform_upload(data)
    upload_success(upload_result)

if __name__ == "__main__":
    print("rumble_uploader.py is being run directly")
else:
    print(f"rumble_uploader.py is being imported by another module: {__name__}")

sys.exit(0)


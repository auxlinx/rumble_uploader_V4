"""
This code block sets up the necessary imports and variables for the Rumble Uploader script.
"""

# Setup
import time
import os
# import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from seleniumbase import Driver
from webdriver_manager.chrome import ChromeDriverManager


SELENIUM_WEBDRIVER_PATH = ChromeDriverManager().install()
# SELENIUM_WEBDRIVER_PATH = ChromeDriverManager().install()

# if SELENIUM_WEBDRIVER_PATH is not None:
#     # You can safely call methods on SELENIUM_WEBDRIVER_PATH here
#     SELENIUM_WEBDRIVER_PATH.split()
# else:
#     print("SELENIUM_WEBDRIVER_PATH is None")

rumble_sign_in_button = 'body > header > div > div > button.header-user.round-button.transparent-button'
rumble_username_field_input = '#login-username'
rumble_password_field_input = '#login-password'
rumble_login_button = '#loginForm > button.login-button.login-form-button.round-button.bg-blue'
rumble_green_upload_button = 'body > header > div > div > button.header-upload'
rumble_upload_video_button = 'body > nav > div.hover-menu.header-upload-menu.pop-show > a:nth-child(1)'

rumble_video_text_input = '#title'
rumble_video_description_input = '#description'
rumble_video_categroies_input = '#form > div > div.video-details.form-wrap > div.form-wrap > div:nth-child(1) > div > input.select-search-input'


rumble_video_secondary_categroies_input = '#form > div > div.video-details.form-wrap > div.form-wrap > div:nth-child(2) > div > input.select-search-input'
rumble_videoTag_input = '#tags'
rumble_upload_button = '#submitForm'
rumble_visibility_radio_button = '#visibility_public'

rumble_only_button = '#form2 > div > div.video-more.form-wrap.licensingOptions.quarters-wrap > div:nth-child(4) > div > a'


rumble_termsandcoditions1 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(2)'
rumble_termsandcoditions2 = '#form2 > div > div.video-more.form-wrap.terms-options > div:nth-child(3)'
rumble_submit_button = '#submitForm2'

#  this allows me to use the password from the .env file
from dotenv import load_dotenv
from urllib.parse import unquote


load_dotenv()  # take environment variables from .env.

#  this is the location of the chrome drive whicn is in the file
# chromedriver_path = "D:\\Proton Drive\\My files\\rahw_coding_mobile\\aux_coding\\rumble_uploader\\chromedriver_win32 (1)\\chromedriver.exe"
# chromedriver_path = "C:\Chromedriver\chromedriver.exe"
opt = Options()
opt.add_experimental_option("debuggerAddress", "localhost:8989")

driver = Driver()
driver.get("https://rumble.com/")

rumble_username = os.getenv('RUMBLE_USERNAME')
rumble_password = unquote(os.getenv('RUMBLE_PASSWORD'))

# username = "randomrumblevideos@protonmail.com"
# password = "XKpE@h!1%j#hTW"
try:
    # Click the login button
    sign_in_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                    rumble_sign_in_button)))
    sign_in_button.click()
except TimeoutException:
    print("Sign-in button click failed")

try:
    username_field = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                rumble_username_field_input)))
    username_field.send_keys(rumble_username)
except TimeoutException:
    print("TimeoutException: Element not found or not clickable")

try:
    password_field = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                rumble_password_field_input)))
    password_field.send_keys(rumble_password)
except TimeoutException:
    print("TimeoutException: Element not found or not clickable")

# Click the login button
login_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                            rumble_login_button)))
login_button.click()
print("Sign-in was successful")
print(driver.title)

time.sleep(3)

green_upload_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                    rumble_green_upload_button)))
green_upload_button.click()

time.sleep(1)
uploadVideoButton = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                rumble_upload_video_button)))
uploadVideoButton.click()

videoTitle = "Test"
videoDescription = "Test"
videoTags = "Test"
videoCategory = "News"
videoSecondCategory = "Trending News"


def getFirstFile():
    # Set the path to the folder you want to get the first item from
    folder_path = "D:\\Proton Drive\\My files\\rahw_coding_mobile\\aux_coding\\rumble_uploader\\rumble_upload_test_video" # where your movies are at

    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Get the first file in the folder
    first_file = files[0]

    # Get the name of the first file
    first_file_name = os.path.basename(first_file)

    first_file_path = os.path.join(str(folder_path), str(first_file))

    print("First file in folder:", first_file)
    print("Name of first file:", first_file_name)
    return first_file_path


def deleteTheFile(nameOfFileAndPath):
    # delete the film from folder
    time.sleep(2)
    print("Deleting the movie from folder")
    os.remove(nameOfFileAndPath)


uploads = 0
# The worker

while True:
    print("New upload started!")
    driver.get("https://rumble.com/upload.php")

    time.sleep(1)
    while True:

        file_path = getFirstFile()

        try:
            # Find the file input element and upload the first file
            file_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'Filedata')))
            file_input.send_keys(file_path)

            time.sleep(1)
        except Exception as e:
            print("Unable to upload file:", str(e))
            break

        try:
            videoTitle_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                rumble_video_text_input)))
            videoTitle_input.send_keys(videoTitle)
            time.sleep(1)
        except Exception as e:
            print("Unable to add Video Title", str(e))
            break

        try:
            video_description_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                        rumble_video_description_input)))
            video_description_input.send_keys(videoDescription)
            time.sleep(1)
        except Exception as e:
            print("Unable to add Video Description", str(e))
            break

        # this selects the category
        try:
            video_categroies_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                    rumble_video_categroies_input)))
            video_categroies_input.send_keys(videoCategory)
            time.sleep(1)
        except Exception as e:
            print("Unable to add Video Category", str(e))
            break

        # this selects the secondary category
        try:
            video_secondary_categroies_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                                rumble_video_secondary_categroies_input)))
            video_secondary_categroies_input.send_keys(videoSecondCategory)
            time.sleep(1)
        except Exception as e:
            print("Unable to add Video Secondary Category", str(e))
            break

        try:
            videoTag_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                rumble_videoTag_input)))
            videoTag_input.send_keys(videoTags)
            time.sleep(1)
        except Exception as e:
            print("Unable to add Video Tag", str(e))
            break

        try:
            # Upload button
            upload_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                        rumble_upload_button)))
            print(upload_button.get_attribute('outerHTML'))
            upload_button.click()
            time.sleep(1)
        except Exception as e:
            print("Unable to click on upload button", str(e))
            break

        try:
            # Rumble Only
            rumbleOnly = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                        rumble_only_button)))
            print(rumbleOnly.get_attribute('outerHTML'))
            rumbleOnly.click()
            time.sleep(1)
        except Exception as e:
            print("Unable to click on Rumble Only", str(e))
            break


        try:
            # Terms and conditions
            # You have not signed an exclusive agreement with any other parties.
            termsandcoditions1 = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                    rumble_termsandcoditions1)))
            termsandcoditions1.click()
            time.sleep(1)
        except Exception as e:
            print("Unable to click on Terms and Conditions 1", str(e))
            break

        try:
            termsandcoditions2 = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                                rumble_termsandcoditions2)))
            termsandcoditions2.click()
            time.sleep(1)
        except Exception as e:
            print("Unable to click on Terms and Conditions 2", str(e))
            break

        try:
            submit_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                        rumble_submit_button)))
            submit_button.click()
            time.sleep(1)
        except Exception as e:
            print("Unable to click on Submit button", str(e))
            break
            print("Unable to click on Terms and conditions step 1", str(e))
            break

        try:
            # Check here if you agree to our terms of service.
            termsandcoditions2 = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_termsandcoditions2)))
            termsandcoditions2.click()
            time.sleep(1)
        except Exception as e:
            print("Unable to click on Terms and conditions step 2", str(e))
            break

        try:
            # Submit
            submit_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, rumble_submit_button)))
            submit_button.click()
            time.sleep(1)

            print("Upload complete!")
            time.sleep(1)

            # Delete the file that was used
            deleteTheFile(file_path)
            time.sleep(1)
            # back to start
            driver.get("https://rumble.com/upload.php")
            uploads += 1
            print(f"Their have been {uploads} uploads so far")
        except Exception as e:
            print("Unable to click on Submit button", str(e))
            break

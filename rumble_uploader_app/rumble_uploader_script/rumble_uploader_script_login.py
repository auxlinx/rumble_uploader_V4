import os
import logging
from dotenv import load_dotenv
# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_rumble_credentials(rumble_video_data):
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

    return rumble_username, rumble_password

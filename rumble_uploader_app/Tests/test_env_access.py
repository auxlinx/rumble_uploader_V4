import os
from dotenv import load_dotenv

# Load .env file
env_file_path = r'D:\Proton Drive Backup\rahw_coding_mobile\aux_coding\rumble_uploader\rumble_uploader_V4\.env'
load_result = load_dotenv(env_file_path)
if load_result:
    print(f"Success: Loaded .env file from {env_file_path}")
else:
    print(f"Failure: Could not load .env file from {env_file_path}")

# Attempt to read a variable
test_variable = os.getenv("RUMBLE_USERNAME_randomrumblevideos")

if test_variable is not None:
    print(f"Success: Able to read TEST_VARIABLE = {test_variable}")
else:
    print("Failure: Unable to read TEST_VARIABLE from .env file")

print(f"Current Working Directory: {os.getcwd()}")

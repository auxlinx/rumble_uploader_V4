import subprocess

"""
This module provides functionality to connect to ProtonVPN.
"""

def start_protonvpn():
    """
    Connects to the fastest ProtonVPN server.
    """
    try:
        # Command to connect to the fastest ProtonVPN server
        command = [r"env\\Lib\\site-packages\\protonvpn_cli\\cli.py", "connect", "--fastest"]

        # Execute the command
        subprocess.run(command, check=True)
        print("Connected to ProtonVPN successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to ProtonVPN: {e}")

if __name__ == "__main__":
    start_protonvpn()

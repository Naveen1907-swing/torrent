import os
import subprocess

# Set local download path
DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "Torrents")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Set the path to aria2c.exe - MODIFY THIS PATH to where you extracted aria2c.exe
ARIA2_PATH = r"C:\Path\To\aria2c.exe"  # Replace with your actual path

# Function to add torrents from magnet links
def add_magnet_links():
    while True:
        magnet_link = input("Enter Magnet Link Or Type Exit: ")
        if magnet_link.lower() == "exit":
            break
        try:
            # Use aria2c to download the torrent
            subprocess.run([ARIA2_PATH, magnet_link, '-d', DOWNLOAD_PATH])
        except Exception as e:
            print(f"Error adding torrent: {e}")

# Run the function
if __name__ == "__main__":
    try:
        add_magnet_links()
    except Exception as e:
        print(f"Error: {e}")

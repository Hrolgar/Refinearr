# qBittorrent Manager

This project provides a command-line tool to filter and delete torrents from qBittorrent based on defined criteria (e.g., age, last activity, popularity). It features interactive deletion with pretty-printing of torrent details, and leverages environment variables to manage sensitive data.

## Features

- Login: Connects to the qBittorrent WebUI API.
- Torrent Filtering: Lists and filters torrents based on configurable thresholds (age, last activity, popularity).
- Pretty-Printed Output: Displays torrent details in a colorful, boxed format.
- Interactive Deletion: Offers a prompt for interactive deletion (delete, skip, or delete all remaining torrents).
- Environment Management: Uses a .env file for easy management of configuration and credentials.

## Setup

You can set up the project in one of two ways: manually or by using an automated setup script.

### Manual Setup
1. Clone the Repository
````bash 
git clone https://your.repo.url/qbittorrent-manager.git
cd qbittorrent-manager
````
2. Create and Activate a Virtual Environment:

- Unix/macOS:
````bash 
python -m venv venv
source venv/bin/activate
````

- Windows:
python -m venv venv
venv\Scripts\activate

3. Install Dependencies:
````bash 
pip install -r requirements.txt
````

4. Create the .env File:

Create a file named .env in the project root with the following content:

````dotenv 
BASE_URL=http://10.69.4.6:8080/api/v2
USERNAME=username
PASSWORD=password
AGE_THRESHOLD_DAYS=16
LAST_ACTIVITY_THRESHOLD_DAYS=10
````

5. Run the Script:

````bash 
python main.py
````


### Automated Setup (Recommended)
If you prefer a one-command setup, you can use the provided shell or batch script. The scripts will:

- Create the virtual environment (if it does not exist)

- Activate the virtual environment

- Install dependencies from ``requirements.txt``

- Create the ``.env`` file with default values (if it doesn’t already exist)

### Unix/macOS Setup Script
Run the following command from the project root:
````bat 
setup\file.bat
````

### Windows Setup Script

Run the batch script by either double-clicking the file or executing it from a command prompt:
````batch
setup\file.bat
````

Once the appropriate setup script finishes, you can run the main script:
````batch
python main.py
````
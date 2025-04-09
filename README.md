# qBittorrent Manager

This project provides a command-line tool to filter and delete torrents from qBittorrent based on defined criteria (e.g., age, last activity, popularity). It features interactive deletion with pretty-printing of torrent details.

## Features

- Login to the qBittorrent WebUI API.
- List and filter torrents based on configurable thresholds.
- Pretty-print torrent details in a colorful, boxed format.
- Interactive deletion prompt (supports delete, skip, or delete all remaining).
- Uses environment variables to manage sensitive data.

## Setup

1. Clone the repository.
2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Unix/macOS
    venv\Scripts\activate     # on Windows
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the project root:
    ```dotenv
    BASE_URL=http://10.69.4.6:8080/api/v2
    USERNAME=username
    PASSWORD=password
    AGE_THRESHOLD_DAYS=16
    LAST_ACTIVITY_THRESHOLD_DAYS=10
    ```
4. Run the script:
    ```bash
    python main.py
    ```


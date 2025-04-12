# src/apis/qbittorrent_api.py

import os
import requests
from src.utils import logger
from dotenv import load_dotenv


class QbitAPI:
    """
    A class to interact with the qBittorrent WebUI API.
    """

    def __init__(self, base_url: str = None, username: str = None, password: str = None):
        """
        Initialize the QbitAPI client by setting up a requests session and loading
        configuration (base URL, username, and password) from environment variables.
        """
        self.session = requests.Session()
        # Use environment variables to configure the API client.
        self.base_url = base_url or os.environ.get("QBIT_BASE_URL")
        self.username = username or os.environ.get("QBIT_USERNAME")
        self.password = password or os.environ.get("QBIT_PASSWORD")

    def _build_url(self, endpoint: str) -> str:
        """
        Construct a full URL for a given endpoint.

        :param endpoint: API endpoint path, e.g., 'auth/login'.
        :return: Full URL string.
        """
        return f"{self.base_url}/{endpoint}"

    def login(self) -> bool:
        """
        Log in to the qBittorrent WebUI.

        :return: True if login is successful, False otherwise.
        """
        login_url = self._build_url("auth/login")
        logger.info("Logging in to %s with username %s", login_url, self.username)
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.session.post(login_url, data=data)
        if response.text.strip() == "Ok.":
            logger.info("Login successful!")
            return True
        else:
            logger.info("Login failed: %s", response.text)
            return False

    def list_torrents(self) -> list:
        """
        Retrieve the list of torrents from qBittorrent.

        :return: A list of torrent dictionaries; an empty list if the request fails.
        """
        torrents_url = self._build_url("torrents/info")
        response = self.session.get(torrents_url)
        if not response.ok:
            logger.info("Error retrieving torrents: %s", response.text)
            return []
        return response.json()

    def delete_torrent(self, torrent_name: str, torrent_hash: str, delete_files: bool = True) -> None:
        """
        Delete a torrent using its hash.

        :param torrent_name: Name of the torrent (for logging purposes).
        :param torrent_hash: Unique hash of the torrent to delete.
        :param delete_files: If True, also delete the downloaded data.
        """
        data = {
            "hashes": torrent_hash,
            "deleteFiles": "true" if delete_files else "false"
        }
        delete_url = self._build_url("torrents/delete")
        response = self.session.post(delete_url, data=data)
        if response.ok:
            logger.info("\033[92mSuccessfully deleted torrent %s\033[0m", torrent_name)
        else:
            logger.info("\033[91mFailed to delete torrent %s: %s\033[0m", torrent_name, response.text)


# Example usage for testing:
if __name__ == "__main__":
    load_dotenv(override=True)
    qbit = QbitAPI()
    if qbit.login():
        torrents = qbit.list_torrents()
        logger.info("Found %d torrents.", len(torrents))

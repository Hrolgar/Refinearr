# src/services/qbit.py

import os
import time
import schedule
from typing import Dict, Any
from dotenv import load_dotenv

from src.api import QbitAPI
from src.utils import logger
from src.utils import print_torrent_details

SECONDS_PER_DAY = 86400
AGE_THRESHOLD_DAYS = int(os.environ.get("AGE_THRESHOLD_DAYS", 16))
LAST_ACTIVITY_THRESHOLD_DAYS = int(os.environ.get("LAST_ACTIVITY_THRESHOLD_DAYS", 7))


class QbitService:
    """
    A service class that encapsulates the qBittorrent cleanup logic.
    """

    def __init__(self) -> None:
        """
        Initialize the QbitService with a QbitAPI instance and sleep interval.

        :param sleep_interval: Time (in seconds) to pause between API calls.
        """
        self.api = QbitAPI()

    @staticmethod
    def is_ready_for_delete(torrent: Dict[str, Any], current_time: float) -> bool:
        """
        Check if a torrent is ready for deletion based on its added time, last activity, popularity,
        and category.

        :param torrent: Dictionary representing torrent data.
        :param current_time: The current time (as a Unix timestamp).
        :return: True if the torrent meets the criteria for deletion.
        """
        added_age = current_time - torrent.get("added_on", 0)
        last_activity_age = current_time - torrent.get("last_activity", 0)
        popularity = torrent.get("popularity", 1.0)
        is_audiobook = torrent.get("category") == "audiobooks"
        return (added_age > AGE_THRESHOLD_DAYS * SECONDS_PER_DAY and
                last_activity_age > LAST_ACTIVITY_THRESHOLD_DAYS * SECONDS_PER_DAY and
                popularity < 0.6 and not is_audiobook)


    def run_cleanup(self, interactive: bool = True) -> None:
        """
        Execute the qBittorrent cleanup process once.
        This method logs in, retrieves the torrent list, filters torrents based on criteria,
        and then deletes the eligible torrents.

        :param interactive: If True, prompts the user; otherwise auto-deletes.
        """
        if not self.api.login():
            logger.info("qBit login failed.")
            return

        torrents = self.api.list_torrents()
        if not torrents:
            logger.info("No qBit torrents found.")
            return

        current_time = time.time()
        filtered_torrents = [torrent for torrent in torrents if self.is_ready_for_delete(torrent, current_time)]
        logger.info(f"[qBit] Found {len(filtered_torrents)} torrent(s) ready for deletion.")

        delete_all = False
        for torrent in filtered_torrents:
            print_torrent_details(torrent)
            name = torrent.get('name', 'N/A')
            torrent_hash = torrent.get('hash')

            if delete_all or not interactive:
                logger.info(f"[qBit] Auto-deleting: {name}")
                self.api.delete_torrent(name, torrent_hash, delete_files=True)
                continue

            # Interactive prompt
            answer = input(f"Delete torrent {name}? (yes/no/deleteall/exit): ").strip().lower()
            if answer == "deleteall":
                delete_all = True
                logger.info(f"[qBit] Deleting {name} and all following automatically.")
                self.api.delete_torrent(name, torrent_hash, delete_files=True)
            elif answer in ("yes", "y"):
                logger.info(f"[qBit] Deleting {name}.")
                self.api.delete_torrent(name, torrent_hash, delete_files=True)
            elif answer in ("no", "n"):
                logger.info(f"[qBit] Skipping {name}.")
            elif answer == "exit":
                logger.info("[qBit] Exiting cleanup loop.")
                break

    def register_schedule(self, run_time: str = "02:00") -> None:
        """
        Register the qBittorrent cleanup process to run daily at the specified time.

        This method only registers the cleanup job with the schedule library,
        without entering its own infinite loop.

        :param run_time: Time string in HH:MM (24-hour) format (default "02:00").
        """
        logger.info(f"Registering qBit cleanup daily at {run_time} (non-interactive).")
        schedule.every().day.at(run_time).do(self.run_cleanup, interactive=False)


# For testing purposes:
if __name__ == "__main__":
    load_dotenv(override=True)
    AGE_THRESHOLD_DAYS = int(os.environ.get("AGE_THRESHOLD_DAYS", 16))
    LAST_ACTIVITY_THRESHOLD_DAYS = int(os.environ.get("LAST_ACTIVITY_THRESHOLD_DAYS", 7))

    service = QbitService()
    service.run_cleanup(interactive=True)

    # To run the cleanup once (non-interactive mode):
    # service.run_cleanup(interactive=False)

    # To schedule the cleanup daily:
    # service.schedule_cleanup(run_time=os.environ.get("RUN_TIME", "02:00"))

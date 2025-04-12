# src/services/qbit.py

import os
import time
from typing import Dict, Any
from dotenv import load_dotenv

from src.api import QbitAPI
from src.services.base_service import BaseService
from src.utils import print_torrent_details
from src.utils.logger import setup_logger

SECONDS_PER_DAY = 86400
AGE_THRESHOLD_DAYS = int(os.environ.get("QBIT_TORRENT_AGE_THRESHOLD_DAYS", 16))
LAST_ACTIVITY_THRESHOLD_DAYS = int(os.environ.get("QBIT_TORRENT_LAST_ACTIVITY_THRESHOLD_DAYS", 7))

logger = setup_logger(__name__, service_name="qBit", color="cyan")

class QbitService(BaseService):
    """
    A service class that encapsulates the qBittorrent cleanup logic.
    """

    def __init__(self) -> None:
        """
        Initialize the QbitService with a QbitAPI instance and sleep interval.
        """
        super().__init__()
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
        is_audiobook = torrent.get("category") == "audiobooks"
        is_ebook = torrent.get("category") == "ebooks"
        return (added_age > AGE_THRESHOLD_DAYS * SECONDS_PER_DAY and
                last_activity_age > LAST_ACTIVITY_THRESHOLD_DAYS * SECONDS_PER_DAY and not is_audiobook and not is_ebook)


    def start(self, interactive: bool = True) -> None:
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

    @staticmethod
    def qbit_scheduled_cleanup():
        """
        Schedule the qBittorrent cleanup process to run based on environment variables.
        """
        qbit_interval = os.getenv("QBIT_INTERVAL_MINUTES")
        qbit_run_time = os.getenv("QBIT_RUN_TIME")
        if qbit_interval and qbit_run_time:
            logger.error("Both QBIT_INTERVAL_MINUTES and QBIT_RUN_TIME are defined. Please set only one.")
            exit(1)
        qbit_service = QbitService()
        if qbit_interval:
            try:
                interval = int(qbit_interval)
            except ValueError:
                logger.error("QBIT_INTERVAL_MINUTES must be an integer.")
                exit(1)
            qbit_service.register_schedule(interval_minutes=interval)
            next_run_time = time.strftime("%H:%M", time.localtime(time.time() + (interval * 60)))
            logger.info("Registered qBit cleanup to run every %d minutes, starting at %s", interval, next_run_time)

        elif qbit_run_time:
            qbit_service.register_schedule(run_time=qbit_run_time)
            logger.info("Registered qBit cleanup at %s", qbit_run_time)
        else:
            # Default schedule if nothing is provided
            qbit_service.register_schedule(run_time="02:00")
            logger.info("No QBIT schedule config found. Defaulting to daily at 02:00")


    def run_job(self, *args, **kwargs):
        self.start(interactive=False)
        if self.schedule_job and self.schedule_job.next_run:
            next_run = self.schedule_job.next_run.strftime("%d.%m.%Y %H:%M")
            logger.info("[qBit] Next run at: %s", next_run)
        else:
            logger.info("[qBit] Next run time is not available.")


if __name__ == "__main__":
    load_dotenv(override=True)
    AGE_THRESHOLD_DAYS = int(os.environ.get("AGE_THRESHOLD_DAYS", 16))
    LAST_ACTIVITY_THRESHOLD_DAYS = int(os.environ.get("LAST_ACTIVITY_THRESHOLD_DAYS", 7))

    service = QbitService()
    service.start(interactive=True)

import os
import schedule
import time
from utils.logger import logger
from api import login, list_torrents, delete_torrent
from utils.utils import print_torrent_details, is_ready_for_delete

def run_qbit_cleanup(interactive=True):
    """
    Performs the qBittorrent cleanup logic once.
    """
    if not login():
        logger.error("qBit login failed.")
        return

    torrents = list_torrents()
    if not torrents:
        logger.info("No qBit torrents found.")
        return

    current_time = time.time()
    filtered_torrents = [t for t in torrents if is_ready_for_delete(t, current_time)]
    logger.info(f"[qBit] Found {len(filtered_torrents)} torrent(s) ready for deletion.")

    # Example non-interactive vs. interactive handling
    delete_all = False
    for torrent in filtered_torrents:
        print_torrent_details(torrent)
        name = torrent.get('name', 'N/A')
        hash_ = torrent.get('hash')

        if delete_all or not interactive:
            logger.info(f"[qBit] Auto-deleting: {name}")
            delete_torrent(name, hash_, delete_files=True)
            continue

        # If interactive, prompt the user
        answer = input(f"Delete torrent {name}? (yes/no/deleteall/exit): ").strip().lower()
        if answer == "deleteall":
            delete_all = True
            logger.info(f"[qBit] Deleting {name} and all following automatically.")
            delete_torrent(name, hash_, delete_files=True)
        elif answer in ("yes", "y"):
            logger.info(f"[qBit] Deleting {name}.")
            delete_torrent(name, hash_, delete_files=True)
        elif answer in ("no", "n"):
            logger.info(f"[qBit] Skipping {name}.")
        elif answer == "exit":
            logger.info("[qBit] Exiting loop.")
            break

def schedule_qbit(run_time="02:00", interactive=False, sleep_interval=60):
    """
    Runs qBit cleanup daily at the specified run_time in non-interactive mode by default.
    """
    logger.info(f"Scheduling qBit cleanup daily at {run_time}. Non-interactive={not interactive}")
    schedule.every().day.at(run_time).do(run_qbit_cleanup, interactive=interactive)
    while True:
        schedule.run_pending()
        time.sleep(sleep_interval)

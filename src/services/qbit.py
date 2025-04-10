import schedule
import time
import os
from src.utils import logger, print_torrent_details
from src.api import login, list_torrents, delete_torrent

SECONDS_PER_DAY = 86400
AGE_THRESHOLD_DAYS = int(os.environ.get("AGE_THRESHOLD_DAYS", 16))
LAST_ACTIVITY_THRESHOLD_DAYS = int(os.environ.get("LAST_ACTIVITY_THRESHOLD_DAYS", 10))


def is_ready_for_delete(torrent, current_time):
    added_age = current_time - torrent.get("added_on", 0)
    last_activity_age = current_time - torrent.get("last_activity", 0)
    popularity = torrent.get("popularity", 1.0)
    is_audiobook = torrent.get("category") == "audiobooks"
    return (added_age > AGE_THRESHOLD_DAYS * SECONDS_PER_DAY and
            last_activity_age > LAST_ACTIVITY_THRESHOLD_DAYS * SECONDS_PER_DAY and
            popularity < 0.6 and not is_audiobook)


def run_qbit_cleanup(interactive=True):
    """
    Performs the qBittorrent cleanup logic once.
    """
    if not login():
        logger.info("qBit login failed.")
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

def schedule_qbit(run_time="02:00", sleep_interval=60):
    """
    Runs qBit cleanup daily at the specified run_time in non-interactive mode by default.
    """
    logger.info(f"Scheduling qBit cleanup daily at {run_time}")
    schedule.every().day.at(run_time).do(run_qbit_cleanup, interactive=False)
    while True:
        schedule.run_pending()
        time.sleep(sleep_interval)

import os
from dotenv import load_dotenv
import time
import argparse
from utils import print_torrent_details, logger
from api import login, list_torrents, delete_torrent
from dotenv import load_dotenv
load_dotenv(override=True)  

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


def process_torrents(filtered_torrents, interactive=True):
    """
    Process (delete) filtered torrents.
    
    :param filtered_torrents: List of torrent dictionaries to process.
    :param interactive: If True, prompt for each torrent; otherwise process automatically.
    """
    delete_all = False
    for torrent in filtered_torrents:
        print_torrent_details(torrent)
        torrent_name = torrent.get('name', 'Unknown Name')
        torrent_hash = torrent.get('hash')

        if delete_all:
            logger.info(f"Automatically deleting torrent: {torrent_name}")
            delete_torrent(torrent_name, torrent_hash, delete_files=True)
            continue

        if interactive:
            answer = input("Do you want to delete this torrent? (yes/no/deleteall/exit): ").strip().lower()
            if answer == "exit":
                logger.info("Exiting the processing loop.")
                break
            elif answer == "deleteall":
                delete_all = True
                logger.info(f"Deleting torrent {torrent_name} and all remaining torrents automatically.")
                delete_torrent(torrent_name, torrent_hash, delete_files=True)
            elif answer in ("yes", "y"):
                delete_torrent(torrent_name, torrent_hash, delete_files=True)
            elif answer in ("no", "n"):
                logger.info(f"Skipping torrent: {torrent_name}\n")
            else:
                logger.info("Unrecognized option; skipping torrent.\n")
        else:
            # Non-interactive mode: automatically delete each torrent.
            logger.info(f"Automatically deleting torrent: {torrent_name}")
            delete_torrent(torrent_name, torrent_hash, delete_files=True)


def main(interactive=True):
    torrents = list_torrents()
    if not torrents:
        logger.info("No torrents found.")
        return

    current_time = time.time()
    filtered_torrents = [torrent for torrent in torrents if is_ready_for_delete(torrent, current_time)]
    
    logger.info(f"Filtered torrents (older than {AGE_THRESHOLD_DAYS} days and last activity over {LAST_ACTIVITY_THRESHOLD_DAYS} days):")
    logger.info(f"Total torrents in the filtered list: {len(filtered_torrents)}\n")

    if not filtered_torrents:
        logger.info("No torrents are ready for deletion based on the filters.")
        return

    process_torrents(filtered_torrents, interactive)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="qBittorrent Cleanup Script")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Run in non-interactive mode (auto-delete filtered torrents)")
    args = parser.parse_args()

    if not all([os.getenv("USERNAME"), os.getenv("PASSWORD"), os.getenv("BASE_URL")]):
        logger.info("Please set USERNAME, PASSWORD, and BASE_URL in the .env file.")
        exit(1)

    logger.info("Starting qBittorrent cleanup script...")
    logger.info("Loading environment variables...")

    if not login():
        logger.info("Login failed. Exiting.")
        exit(1)

    if args.non_interactive:
        logger.info("Running in non-interactive mode...")
        main(interactive=False)
    else:
        logger.info("Running in interactive mode...")
        main(interactive=True)

    logger.info("Finished processing torrents.")
import os
from dotenv import load_dotenv
import time
from utils import print_torrent_details, logger
from api import login, list_torrents, delete_torrent
from dotenv import load_dotenv
load_dotenv()  

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


def interactive_deletion():
    torrents = list_torrents()
    if not torrents:
        return

    current_time = time.time()
    filtered_torrents = [torrent for torrent in torrents if is_ready_for_delete(torrent, current_time)]
    
    logger.info(f"Filtered torrents (older than {AGE_THRESHOLD_DAYS} days and last activity over {LAST_ACTIVITY_THRESHOLD_DAYS} days):")
    logger.info(f"\nTotal torrents in the filtered list: {len(filtered_torrents)}\n")

    if not filtered_torrents:
        logger.info("No torrents are ready for deletion based on the filters.")
        return

    delete_all = False
    for torrent in filtered_torrents:
        print_torrent_details(torrent) 
        torrent_name = torrent.get('name', 'Unknown Name')
        torrent_hash = torrent.get('hash')
        
        if delete_all:
            delete_torrent(torrent_name, torrent_hash, delete_files=True)
            continue

        answer = input("Do you want to delete this torrent? (yes/no/deleteall/exit): ").strip().lower()
        if answer == "deleteall":
            delete_all = True
            delete_torrent(torrent_name, torrent_hash, delete_files=True)
        elif answer in ("yes", "y"):
            delete_torrent(torrent_name, torrent_hash, delete_files=True)
        elif answer in ("no", "n"):
            logger.info(f"Skipping torrent: {torrent_name}\n")
        elif answer == "exit":
            logger.info("Exiting the program.")
            break

if __name__ == "__main__":
    if not all([os.getenv("USERNAME"), os.getenv("PASSWORD"), os.getenv("BASE_URL")]):
        logger.info("Please set USERNAME, PASSWORD, and BASE_URL in the .env file.")
        exit(1)
    logger.info("Starting qBittorrent cleanup script...")
    logger.info("Loading environment variables...")
    logger.info("Logging in to qBittorrent...")
    if not login():
        logger.info("Login failed. Exiting.")
    logger.info("Login successful.")
    logger.info("Listing torrents...")    
    interactive_deletion()
    logger.info("Finished processing torrents.")
import os
import argparse
import schedule
import time

from utils import logger
from services import QbitService, SonarrService, RadarrService
from dotenv import load_dotenv

load_dotenv(override=True)

def parse_args():
    """
    Parse command-line arguments and return the resulting namespace.
    Supported arguments:
        --non-interactive   Run in non-interactive mode (auto-delete).
        --schedule          Run on a daily schedule and never exit.
    :return: Namespace with parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Multi-Service Cleanup Script")
    # parser.add_argument("--service", choices=["qbit", "sonarr", "both"], default="qbit", help="Which service(s) to run: qbit, sonarr, or both.")
    parser.add_argument("--non-interactive", action="store_true", help="Run in non-interactive mode (auto-delete).")
    parser.add_argument("--schedule", action="store_true", help="Run on a daily schedule and never exit.")
    return parser.parse_args()

# Check what to run, is based on the .env file, for example, if qbitBaseurl, username and password are set, then run qbit.  if sonarrBaseurl, username and password are set, then run sonarr.  if both are set, then run both.
def check_services():
    """
    Check which services are enabled based on environment variables.
    :return: List of services to run.
    """
    services = []
    if os.getenv("QBIT_BASE_URL") and os.getenv("QBIT_USERNAME") and os.getenv("QBIT_PASSWORD"):
        services.append("qbit")
    if os.getenv("SONARR_BASE_URL") and os.getenv("SONARR_API_KEY"):
        services.append("sonarr")
    if os.getenv("RADARR_BASE_URL") and os.getenv("RADARR_API_KEY"):
        services.append("radarr")
    return services

def schedule_services():
    """
    Schedule all enabled services with their own run times.
    This function schedules each service's job and then enters one infinite loop.
    """
    services = check_services()
    logger.info(f"Services to schedule: {services}")

    if "qbit" in services:
        qbit_service = QbitService()
        qbit_service.qbit_scheduled_cleanup()

    if "sonarr" in services:
        sonarr_service = SonarrService()
        sonarr_service.sonarr_scheduled_cleanup()

    sleep_interval = int(os.getenv("SLEEP_INTERVAL", 60))
    logger.info("Entering scheduling loop. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(sleep_interval)

def run_services(non_interactive: bool):
    """
    Run each enabled service once.
    """
    services = check_services()
    logger.info(f"Services to run: {services}")

    if "qbit" in services:
        logger.info("Running qBit cleanup...")
        qbit_service = QbitService()

        logger.info("qBit cleanup will run once in interactive mode." if non_interactive else "qBit cleanup will run in non-interactive mode.")
        qbit_service.start(interactive=not non_interactive)
    elif "radarr" in services:
        logger.info("Running Radarr cleanup...")
        radarr_service = RadarrService()
        radarr_service.start()

    if "sonarr" in services:
        logger.info("Running Sonarr cleanup...")
        sonarr_service = SonarrService()
        sonarr_service.start()


def main():
    args = parse_args()
    logger.info(f"Starting with arguments: {args}")

    if args.schedule:
        schedule_services()
    else:
        run_services(non_interactive=args.non_interactive)

if __name__ == "__main__":
    main()


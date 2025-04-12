from src.api import RadarrAPI
from src.services.base_service import BaseService
from src.utils import logger
from dotenv import load_dotenv
import time


class RadarrService(BaseService):
    """
    A service class that encapsulates the Radarr cleanup logic.
    """

    def __init__(self, sleep_interval: int = 40):
        super().__init__()
        self.sonarr = RadarrAPI()
        self.sleep_interval = sleep_interval


    def start(self) -> None:
        """
        Main method to run the Radarr cleanup process.
        Iterates over the series and seasons, then issues rename commands when appropriate.
        """
        pass

    def run_job(self, *args, **kwargs):
        pass

    # Example usage:
if __name__ == "__main__":
    load_dotenv(override=True)
    service = RadarrService(sleep_interval=40)

from src.api import SonarrAPI
from src.utils import logger
import time
import schedule

class SonarrService:
    """
    A service class that encapsulates the Sonarr cleanup logic.
    """
    def __init__(self, sleep_interval: int = 40):
        self.sonarr = SonarrAPI(base_url='http://10.69.4.4:8989',api_key='8cf09f28bcb3419d8d125da5f0b8326f')
        self.sleep_interval = sleep_interval

    def get_rename(self, series_id: int, season_number: int) -> list[str]:
        """
        Retrieve a list of episodeFileId's for renaming for the specified series and season.
        """
        # Build the URL directly using the SonarrAPI attributes.
        url = f"{self.sonarr.BASE_URL}/api/v3/rename?apikey={self.sonarr.API_KEY}&seriesId={series_id}&seasonNumber={season_number}"
        response = self.sonarr.session.get(url)
        if response.ok:
            data = response.json()
            return [item["episodeFileId"] for item in data]
        else:
            logger.error(
                f"Failed to get rename info for series {series_id} season {season_number}: {response.text}")
            return []

    def get_dict_of_series(self) -> dict:
        """
        Retrieve series data and return a mapping of series IDs to a list of season numbers needing renaming.
        This is just an example; in production, use real logic to decide which seasons to process.
        """
        series_list = self.sonarr.get_all_series()
        data = {}
        for series in series_list:
            series_id = series.get("id")
            if series_id is not None:
                # For demonstration, assume each series has seasons 1 and 2.
                data[series_id] = [1, 2]
        return data

    def start(self):
        """
        Main method to run the Sonarr cleanup process.
        Iterates over the series and seasons, then issues rename commands when appropriate.
        """
        data = self.get_dict_of_series()
        total_series = len(data)
        logger.info(f"Found {total_series} series to process in Sonarr.")

        # for now just iterate through the first 10 series
        data = dict(list(data.items())[:10])

        for index, (series_id, seasons) in enumerate(data.items(), start=1):
            for season in seasons:
                rename_episodes = self.get_rename(series_id, season)
                if rename_episodes:
                    success = self.sonarr.rename_series_command(series_id, rename_episodes)
                    series_name = self.sonarr.get_series_name(series_id)
                    if success:
                        logger.info(
                            f"Checked {index} of {total_series} series - Renaming series {series_id} ({series_name}), episodes = {rename_episodes}"
                        )
                    else:
                        logger.error(
                            f"Checked {index} of {total_series} series - FAILED renaming series {series_id} ({series_name}), episodes = {rename_episodes}"
                        )
                    time.sleep(self.sleep_interval)
        logger.info("Finished Sonarr cleanup service.")

    def register_schedule(self, run_time: str = "03:00") -> None:
        """
        Register the cleanup process to run daily at the specified time.

        This method registers the cleanup job with the schedule library and does not enter
        its own infinite loop; a central scheduler will handle that.

        :param run_time: Time string in HH:MM (24-hour) format (default is "03:00").
        """
        logger.info("Registering Sonarr cleanup daily at %s.", run_time)
        schedule.every().day.at(run_time).do(self.start)

    # Example usage:
if __name__ == "__main__":
    service = SonarrService(sleep_interval=40)
    service.start()

    # Or run on a schedule:
    # service.schedule(run_time="03:00")

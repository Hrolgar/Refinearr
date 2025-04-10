import os
import requests
from src.utils import logger

class SonarrAPI:
    """
    A class to interact with the Sonarr API.
    """
    def __init__(self, base_url: str = None, api_key: str = None):
        """
        Initialize the SonarrAPI class with the base URL and API key.
        """

        self.session = requests.Session()
        self.API_KEY = api_key or os.environ.get("SONARR_API_KEY")
        self.BASE_URL = base_url or os.environ.get("SONARR_BASE_URL")


    def _build_url(self, endpoint):
        """
        Build the full URL for a given endpoint.
        :param endpoint: The API endpoint to call.
        :return: The full URL for the API call.
        """
        return f"{self.BASE_URL}/api/v3/{endpoint}?apikey={self.API_KEY}"


    def _get(self, path: str, params: dict = None) -> requests.Response:
        """
        Internal helper for GET requests.

        :param path: API endpoint path.
        :param params: Additional query parameters.
        :return: A Response object.
        """
        url = self._build_url(path)
        response = self.session.get(url, params=params)
        logger.debug(f"GET {url} with params {params} returned {response.status_code}")
        return response

    def _post(self, path: str, data: dict) -> requests.Response:
        """
        Internal helper for POST requests.

        :param path: API endpoint path.
        :param data: Dictionary payload to send as JSON.
        :return: A Response object.
        """
        url = self._build_url(path)
        response = self.session.post(url, json=data)
        logger.debug(f"POST {url} with payload {data} returned {response.status_code}")
        return response

    def get_all_series(self) -> list:
        """
        Retrieve all series from Sonarr.

        :return: A list of series dictionaries; an empty list if the request fails.
        """
        response = self._get("series")
        if response.ok:
            return response.json()
        else:
            logger.error(f"Error retrieving series: {response.text}")
            return []

    def get_series(self, series_id: int) -> dict:
        """
        Retrieve details for a single series by its ID.

        :param series_id: The unique ID of the series.
        :return: A dictionary with series details, or empty if there is an error.
        """
        path = f"series/{series_id}"
        # Option: includeSeasonImages can be disabled.
        response = self._get(path, params={"includeSeasonImages": "false"})
        if response.ok:
            return response.json()
        else:
            logger.error(f"Error retrieving series {series_id}: {response.text}")
            return {}

    def get_series_name(self, series_id: int) -> str:
        """
        Get the series title for a given series ID.

        :param series_id: The unique ID of the series.
        :return: The title of the series, or "no name" if not found.
        """
        series_data = self.get_series(series_id)
        return series_data.get("title", "no name")

    def rename_series_command(self, series_id: int, files: list) -> bool:
        """
        Issue a command to rename files for a series.

        :param series_id: The unique ID of the series.
        :param files: A list of file IDs (or similar identifiers) that should be renamed.
        :return: True if the command is successfully submitted, otherwise False.
        """
        payload = {
            "name": "RenameFiles",
            "seriesId": series_id,
            "files": files,
        }
        response = self._post("command", payload)
        if response.ok:
            logger.info(f"Rename command submitted for series {series_id}.")
            return True
        else:
            logger.error(f"Failed to submit rename command for series {series_id}: {response.text}")
            return False


if __name__ == "__main__":
    sonarr = SonarrAPI(
        base_url='http://10.69.4.4:8989',
        api_key='8cf09f28bcb3419d8d125da5f0b8326f'
    )
    all_series = sonarr.get_all_series()
    logger.info(f"Found {len(all_series)} series in Sonarr.")

    if all_series:
        example_series = all_series[0]
        local_series_id = example_series.get("id")
        series_name = sonarr.get_series_name(local_series_id)
        logger.info(f"Example series (ID: {local_series_id}) name: {series_name}")
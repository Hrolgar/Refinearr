import os
import requests
import logging
from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)

DEFAULT_PORTS = {
    "qbit": 8080,
    "sonarr": 8989,
    "radarr": 7878,
}

class BaseAPI:
    """
    A base class to interact with an API that follows the /api/<version>/<endpoint>?apikey=<apikey> convention.
    """
    def __init__(
        self,
        base_url: str = None,
        api_key: str = None,
        env_base_url: str = None,
        env_api_key: str = None,
        api_version: str = "v3",
        default_service: str = None
    ):
        """
        Initialize the BaseAPI class using provided arguments or environment variables.

        :param base_url: The base URL for the API.
        :param api_key: The API key to use.
        :param env_base_url: Environment variable name for the base URL.
        :param env_api_key: Environment variable name for the API key.
        :param api_version: The API version to use in URL building.
        """
        self.session = requests.Session()
        self.API_KEY = api_key or (os.environ.get(env_api_key) if env_api_key else None)
        self.BASE_URL = base_url or (os.environ.get(env_base_url) if env_base_url else None)
        self.api_version = api_version
        self.default_service = default_service

        # If BASE_URL is still missing, set it to a default based on service
        if not self.BASE_URL and default_service:
            default_port = DEFAULT_PORTS.get(default_service)
            self.BASE_URL = f"http://localhost:{default_port}"
            logger.info("No base URL provided. Defaulting to %s", self.BASE_URL)

        # Otherwise, if BASE_URL is provided, check whether it has a port and adjust if needed.
        elif self.BASE_URL:
            parsed_url = urlparse(self.BASE_URL)
            if not parsed_url.port and default_service:
                # If the port isn’t provided in the URL, we can add our default port.
                default_port = DEFAULT_PORTS.get(default_service)
                netloc = parsed_url.hostname + f":{default_port}"
                self.BASE_URL = urlunparse(parsed_url._replace(netloc=netloc))
                logger.info("Port not specified. Using default port %d. New BASE_URL: %s", default_port, self.BASE_URL)

        if not self.BASE_URL or default_service in ["sonarr", "radarr"] and not self.API_KEY:
            raise ValueError("Missing base URL or API key")


    def _build_url(self, endpoint: str) -> str:
        """
        Build the full URL for a given endpoint.
        """
        if self.default_service == "qbit":
            return f"{self.BASE_URL}/api/{self.api_version}/{endpoint}"
        elif self.default_service in ["sonarr", "radarr"]:
            return f"{self.BASE_URL}/api/{self.api_version}/{endpoint}?apikey={self.API_KEY}"

        else:
            raise ValueError(f"Unsupported service: {self.default_service}")


    # def _build_url(self, endpoint: str) -> str:
    #     """
    #     Build the full URL for a given endpoint.
    #
    #     :param endpoint: The API endpoint to call.
    #     :return: The full URL for the API call.
    #     """
    #     return f"{self.BASE_URL}/api/{self.api_version}/{endpoint}?apikey={self.API_KEY}"

    def _get(self, path: str, params: dict = None) -> requests.Response:
        """
        Helper method for GET requests.

        :param path: API endpoint path.
        :param params: Additional query parameters.
        :return: A Response object from the GET request.
        """
        url = self._build_url(path)
        response = self.session.get(url, params=params)
        logger.debug(f"GET {url} with params {params} returned {response.status_code}")
        return response

    def _post(self, path: str, data: dict) -> requests.Response:
        """
        Helper method for POST requests.

        :param path: API endpoint path.
        :param data: Dictionary payload to send as JSON.
        :return: A Response object from the POST request.
        """
        url = self._build_url(path)
        response = self.session.post(url, json=data)
        logger.debug(f"POST {url} with payload {data} returned {response.status_code}")
        return response
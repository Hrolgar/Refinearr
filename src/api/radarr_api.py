from src.api.base_api import BaseAPI
from src.utils import logger

class RadarrAPI(BaseAPI):
    """
    A class to interact with the Radarr API.
    """
    def __init__(self, base_url: str = None, api_key: str = None):
        """
        Initialize the RadarrAPI class with the base URL and API key.
        """
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            env_base_url="RADARR_BASE_URL",
            env_api_key="RADARR_API_KEY",
            api_version="v3",
            default_service="radarr"
        )

    def get_large_movies(self, min_size_gb: float = 2.0) -> list:
        """
        Fetch movies and return those with a sizeOnDisk greater than the specified GB.

        :param min_size_gb: Minimum size in GB (default is 2GB).
        :return: A list of movie records with sizeOnDisk larger than min_size_gb.
        """
        min_size_bytes = min_size_gb * (1024 ** 3)  # 2GB in bytes
        response = self._get("movie")
        if response.ok:
            movies = response.json()
            large_movies = [
                movie for movie in movies
                if movie.get("sizeOnDisk", 0) > min_size_bytes
            ]
            logger.info("Found %d movies larger than %.2f GB", len(large_movies), min_size_gb)
            return large_movies
        else:
            logger.error("Error fetching movies: %s", response.text)
            raise Exception(f"Error fetching movies: {response.text}")


if __name__ == "__main__":
    from src.api import RadarrAPI
    from src.utils import logger
    from dotenv import load_dotenv

    load_dotenv(override=True)
    radarr = RadarrAPI()

    try:
        threshold_gb = 2.0
        threshold_bytes = threshold_gb * (1024 ** 3)  # Convert 2GB to bytes
        local_large_movies = radarr.get_large_movies(min_size_gb=threshold_gb)

        # Count the number of movies larger than the threshold
        movie_count = len(local_large_movies)

        # Calculate the total potential savings by reducing each movie file to 2GB
        total_saved_bytes = sum(
            (movie.get("sizeOnDisk", 0) - threshold_bytes)
            for movie in local_large_movies
            if movie.get("sizeOnDisk", 0) > threshold_bytes
        )
        total_saved_gb = total_saved_bytes / (1024 ** 3)

        print(f"Radarr has {movie_count} movies that are bigger than {threshold_gb}GB.")
        print(
            f"If each movie file were exactly {threshold_gb}GB, you could potentially save {total_saved_gb:.2f}GB overall.")

    except Exception as e:
        logger.error("An error occurred: %s", e)

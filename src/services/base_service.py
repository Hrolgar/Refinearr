# base_service.py
from abc import ABC, abstractmethod
import logging
import schedule

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Abstract base class for service classes interacting with APIs.
    Forces subclasses to implement the register_schedule method.
    """

    @abstractmethod
    def run_job(self, *args, **kwargs):
        """
        The service-specific work that needs to be scheduled.
        Subclasses must implement this.
        """
        pass

    def register_schedule(self, run_time: str = None, interval_minutes: int = None) -> None:
        """
        Registers the service's job on a schedule, using either a fixed daily time or a periodic interval.
        Either `run_time` or `interval_minutes` must be provided (not both).

        :param run_time: Time string in HH:MM (24-hour) format for daily scheduling.
        :param interval_minutes: Interval in minutes between runs.
        :raises ValueError: If both parameters are provided.
        """
        if run_time and interval_minutes:
            raise ValueError("Cannot define both 'run_time' and 'interval_minutes' for scheduling.")

        if interval_minutes:
            logger.info(f"Registering {self.__class__.__name__} to run every {interval_minutes} minutes.")
            schedule.every(interval_minutes).minutes.do(self.run_job)
        elif run_time:
            logger.info(f"Registering {self.__class__.__name__} to run daily at {run_time}.")
            schedule.every().day.at(run_time).do(self.run_job)
        else:
            # Optionally provide a default schedule or raise an error.
            default_run_time = "02:00"
            logger.info(f"No scheduling configuration provided. Defaulting to daily at {default_run_time}.")
            schedule.every().day.at(default_run_time).do(self.run_job)

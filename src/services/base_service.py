# base_service.py
from abc import ABC, abstractmethod
import logging
import schedule
import threading
import time
from typing import Callable, Any, List
from concurrent.futures import ThreadPoolExecutor, Future

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Abstract base class for service classes interacting with APIs.
    Forces subclasses to implement the register_schedule method.
    """
    def __init__(self, max_workers: int = 5):
        self.schedule_job = None
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_futures: List[Future] = []


    @abstractmethod
    def run_job(self, *args, **kwargs):
        """
        The service-specific work that needs to be scheduled.
        Subclasses must implement this.
        """
        pass

    def run_threaded(self, job_func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """
        Submits the job function to a thread pool for concurrent execution.
        Wraps the function to catch exceptions and log appropriately.

        :param job_func: A callable that represents the job to run.
        :param args: Positional arguments to pass to the job function.
        :param kwargs: Keyword arguments to pass to the job function.
        """

        def wrapper() -> None:
            start_time = time.time()
            job_name = job_func.__name__
            thread_name = f"{job_name}-thread-{int(start_time)}"
            logger.info("Starting job '%s' on thread '%s'", job_name, thread_name)
            try:
                job_func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.info("Finished job '%s' on thread '%s' in %.2f seconds", job_name, thread_name, elapsed)
            except Exception as e:
                logger.exception("Exception occurred in job '%s' on thread '%s': %s", job_name, thread_name, e)

        future: Future = self.executor.submit(wrapper)
        self.active_futures.append(future)

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
            logger.info("Registering %s to run every %d minutes.", self.__class__.__name__, interval_minutes)
            job = schedule.every(interval_minutes).minutes.do(self.run_threaded, self.run_job)
            self.schedule_job = job
        elif run_time:
            logger.info("Registering %s to run daily at %s.", self.__class__.__name__, run_time)
            job = schedule.every().day.at(run_time).do(self.run_threaded, self.run_job)
            self.schedule_job = job
        else:
            # Optionally provide a default schedule if none is provided.
            default_run_time = "02:00"
            logger.info("No scheduling configuration provided. Defaulting %s to daily at %s.",
                        self.__class__.__name__, default_run_time)
            job = schedule.every().day.at(default_run_time).do(self.run_threaded, self.run_job)
            self.schedule_job = job

        if self.schedule_job and hasattr(self.schedule_job, 'next_run'):
            logger.info("Next scheduled run for %s at: %s", self.__class__.__name__, self.schedule_job.next_run)

    def unregister_schedule(self) -> None:
        """
        Unregisters the scheduled job, if any.
        Useful for dynamically stopping a service.
        """
        if self.schedule_job:
            schedule.cancel_job(self.schedule_job)
            logger.info("Unregistered scheduled job for %s.", self.__class__.__name__)
            self.schedule_job = None

    def shutdown(self, wait: bool = True) -> None:
        """
        Gracefully shutdown the executor and cancel any pending scheduled jobs.

        :param wait: Whether to wait for currently running jobs to finish.
        """
        logger.info("Shutting down service %s.", self.__class__.__name__)
        if self.schedule_job:
            schedule.cancel_job(self.schedule_job)
            self.schedule_job = None
        self.executor.shutdown(wait=wait)
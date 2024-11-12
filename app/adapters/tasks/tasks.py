from abc import ABC, abstractmethod


class AbstractBackgroundTask(ABC):

    """
    Abstract class for background task processing
    With this class, we can define a common interface
    for different background processing systems like Celery.
    """

    @abstractmethod
    def add_task(self, task_func, *args, **kwargs):
        """Add a task to the background processing system."""
        pass

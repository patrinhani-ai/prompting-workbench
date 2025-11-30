import threading
from typing import Generic, TypeVar, cast

TSingleton = TypeVar("TSingleton", bound="ThreadSafeSingleton")


class ThreadSafeSingleton(Generic[TSingleton]):
    """
    A generic, thread-safe base class that implements the Singleton pattern.
    """

    # A class-level dictionary to hold instances of derived singletons
    _instances: dict[type, object] = {}
    # A class-level lock for thread synchronization during creation
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # First check (without lock)
        if cls not in cls._instances:
            # Acquire lock only if instance might need creation
            with cls._lock:
                # Second check (inside lock) to ensure another thread hasn't created it
                if cls not in cls._instances:
                    instance = super(ThreadSafeSingleton, cls).__new__(cls)
                    cls._instances[cls] = instance
                    # Add a flag to manage initialization state for the first time
                    instance._initialized = False
        return cls._instances[cls]

    def __init__(self):
        # Prevent __init__ logic from running every time the class is called
        if not self._initialized:
            self._initialized = True
            # Place actual initialization logic here (optional)
            # print(f"Initializing {self.__class__.__name__} only once.")

    @classmethod
    def instance(cls: type[TSingleton]) -> TSingleton:
        """
        Provides a single, thread-safe point of access to the singleton instance.
        """
        # Calling the class constructor triggers the thread-safe __new__ logic
        return cast(TSingleton, cls())

"""
    Module to define SingletonMeta Meta Class
"""
from threading import Lock
from weakref import WeakValueDictionary


class SingletonMeta(type):
    """
    This is a thread-safe implementation of SingletonMeta.
    """

    _instances = WeakValueDictionary()

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the SingletonMeta.
    """

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

#!/usr/bin/env python3
"""logger.py

Log messages using the python standard library logging module.
"""
import sys
import logging
import config


class Logger(object):
    """
    Simple logging class

    Attributes
        logger (object):    Python logging object

    Methods
        shutdown_logs()
            To prevent duplicate filehandlers and system handlers close and
            remove all handlers for all log files with a python logging object
        _get_file_handler()
            Returns the FileHandler associated with the logging object
        _get_logging_formatter()
            Get formatter for logging. This is script mode-dependent
        _get_stream_handler()
            Returns the StreamHandler associated with the logging object
        get_logger()
            Return a Python logging object
    """

    def __init__(self, logger_name: str, logfile_path: str):
        """
        Constructor for the Logger class
            :param logger_name (str):   Name for logger
            :param logfile_path (str):  Logfile path
        """
        self.logger = self.get_logger(logger_name, logfile_path)

    def shutdown_logs(self) -> None:
        """
        To prevent duplicate filehandlers and system handlers close and
        remove all handlers for all log files that have a python logging object
            :return None:
        """
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()

    def _get_file_handler(self, filepath: str) -> logging.FileHandler:
        """
        Returns the FileHandler associated with the logging object
            :return file_handler (obj):   FileHandler object
        """
        file_handler = logging.FileHandler(filepath, mode="a", delay=True)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self._get_logging_formatter())
        file_handler.name = "file_handler"
        return file_handler

    def _get_logging_formatter(self) -> str:
        """
        Get formatter for logging. This is script mode-dependent
            :return (str):  Logging formatter string
        """
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def _get_stream_handler(self) -> logging.StreamHandler:
        """
        Returns the StreamHandler associated with the logging object
            :return stream_handler (obj):   StreamHandler object
        """
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(self._get_logging_formatter())
        stream_handler.name = "stream_handler"
        return stream_handler

    def get_logger(self, name: str, filepath: str) -> logging.Logger:
        """
        Return a Python logging object
            :param name (str):      Logger name
            :param filepath (str):  Logfile path
            :return logger (obj):   Python logging object
        """
        logger = logging.getLogger(name)
        logger.filepath = filepath
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self._get_file_handler(filepath))
        logger.addHandler(self._get_stream_handler())
        logger.timestamp = config.TIMESTAMP
        return logger

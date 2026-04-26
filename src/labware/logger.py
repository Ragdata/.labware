#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			19/04/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import logging

from pathlib import Path
from typing import TextIO, Any

from logging.handlers import RotatingFileHandler

from labware import __pkg_name__

from .config import x_config as config
from .console import *

LOG_LEVEL: int   = config.getint("logging", "level")
LOG_DIR: Path    = Path.home() / config.get("logging", "logdir")
LOG_SIZE: int    = config.getint("logging", "size")
LOG_COUNT: int   = config.getint("logging", "count")
LOG_FORMAT: str  = config.get("logging", "format")
CON_FORMAT: str  = config.get("log_formats", "console", raw=True)
DATE_FORMAT: str = config.get("log_formats", "date", raw=True)

LOG_FORMATS = {
    "std": config.get("log_formats", "std", raw=True),
    "short": config.get("log_formats", "short", raw=True),
    "long": config.get("log_formats", "long", raw=True),
    "console": config.get("log_formats", "console", raw=True),
}


#-------------------------------------------------------------------
# Logger Class
#-------------------------------------------------------------------
class Logger(logging.Logger):
    """Custom labware logger class"""

    def __init__(self, name: str, level: int = LOG_LEVEL, **kwargs) -> None:
        """
        Initialize the logger with a name and level

        Args:
            name (str):     Name of the logger
            level (int):    Logging level. (Defaults to logging.INFO)
            **kwargs:       Additional keyword arguments for logging config
        """
        super().__init__(name, level)
        self.setLevel(level)

    def critical(self, msg:str, *args, **kwargs) -> None:
        """
        Log a CRITICAL message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.CRITICAL, msg, *args, **kwargs)

    def debug(self, msg:str, *args, **kwargs) -> None:
        """
        Log a DEBUG message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def error(self, msg:str, *args, **kwargs) -> None:
        """
        Log an ERROR message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg:str, *args, **kwargs) -> None:
        """
        Log an ERROR message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.ERROR, msg, *args, exc_info=True, **kwargs)

    def fatal(self, msg:str, *args, **kwargs) -> None:
        """
        Log a FATAL message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.FATAL, msg, *args, **kwargs)

    def info(self, msg:str, *args, **kwargs) -> None:
        """
        Log an INFO message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg:str, *args, **kwargs) -> None:
        """
        Log a WARNING message

        Args:
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.WARNING, msg, *args, **kwargs)

    def log(self, level: int, msg: str, *args, **kwargs) -> None:
        """
        Write a message to the log with a specified level

        Args:
            level (int):    The logging level
            msg (str):      The message to log
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)


#-------------------------------------------------------------------
# OutLog Class
#-------------------------------------------------------------------
class Outlog(object):
    """
    A class to handle console message with concurrent logging
    """

    _logger = None

    def __init__(self, logger):
        """
        Initialize the OutLog instance.

        Args:
        	logger: An optional logger instance for logging messages.
        """
        self._logger = logger

    def logMessage(self, msg: str, level: int = config.get("logging", "level"), style: Optional[str] = None, **kwargs) -> None:
        """
        Log and print a message with an optional style.

        Args:
        	msg (str):      The message to log and print.
        	level (int):    The level of the message to log and print.
        	style (str):    The style to apply to the message. (Optional)
        	**kwargs:       Arbitrary keyword arguments.
        """
        if self._logger.isEnabledFor(level):
            self._logger.log(level, msg)
        else:
            return
        symbol = None
        match style:
            case "debug":
                symbol = config.get("symbols", "debug")
            case "info":
                symbol = config.get("symbols", "info")
            case "warning":
                symbol = config.get("symbols", "warning")
            case "error":
                symbol = config.get("symbols", "error")
            case "success":
                symbol = config.get("symbols", "success")
            case "tip":
                symbol = config.get("symbols", "tip")
            case "important":
                symbol = config.get("symbols", "important")
            case "head":
                symbol = config.get("symbols", "head")
            case "dot":
                symbol = config.get("symbols", "dot")
        if symbol is not None:
            msg = f"{symbol} " + msg
        printMessage(msg, style=style, **kwargs)

    def logDebug(self, msg: str, **kwargs) -> None:
        """
        Log a DEBUG message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.DEBUG, style="debug", **kwargs)

    def logInfo(self, msg: str, **kwargs) -> None:
        """
        Log an INFO message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.INFO, style="info", **kwargs)

    def logWarning(self, msg: str, **kwargs) -> None:
        """
        Log a WARNING message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.WARNING, style="warning", **kwargs)

    def logError(self, msg: str, **kwargs) -> None:
        """
        Log an ERROR message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.ERROR, style="error", **kwargs)

    def logSuccess(self, msg: str, **kwargs) -> None:
        """
        Log a SUCCESS message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.INFO, style="success", **kwargs)

    def logCritical(self, msg: str, **kwargs) -> None:
        """
        Log an ERROR message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.CRITICAL, style="error", **kwargs)

    def logFatal(self, msg: str, **kwargs) -> None:
        """
        Log an ERROR message.

        Args:
        	msg (str): The message to log.
        	**kwargs: Arbitrary keyword arguments.
        """
        self.logMessage(msg, level=logging.FATAL, style="error", **kwargs)


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def initRotatingFileHandler(name: str, path: Path = LOG_DIR, maxSize: int = LOG_SIZE, backups: int = LOG_COUNT) -> RotatingFileHandler:
    """
    Initialize and return a RotatingFileHandler.

    Args:
    	name (str):     Name of the logger.
    	level (int):    Logging level for the file handler (default is LOG_LEVEL_FILE).
    	path (Path):    Directory where the log file will be stored (default is DOT_LOG).
    	maxSize (int):  Maximum size of the log file before rotation (default is 5 MB).
    	backups (int):  Number of backup files to keep (default is 5).

    Returns:
    	RotatingFileHandler: Configured file handler instance.
    """
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True, mode=0o755)
    logFile = path / f"{name}.log"
    return RotatingFileHandler(logFile, maxBytes = maxSize, backupCount = backups, encoding='utf-8', delay=False)

def initStreamHandler(stream: TextIO | Any = sys.stdout, level: int = LOG_LEVEL, style: str = CON_FORMAT) -> logging.StreamHandler:
    """
    Initialize and return a StreamHandler.

    Args:
    	stream (TextIO | Any): The stream to which the log messages will be sent (default is sys.stdout).
    	level (int): Logging level for the stream handler (default is LOG_LEVEL_STREAM).
    	style (str): Log format string (default is CON_FORMAT).

    Returns:
    	logging.StreamHandler: Configured stream handler instance.
    """
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    return handler

def getFileLogger(name: str, level: int = LOG_LEVEL, fmt: str = LOG_FORMAT) -> Logger:
    """ Retrieve or create a logger instance """
    formatter = getFormatter(fmt)
    handler = initRotatingFileHandler(name, maxSize=LOG_SIZE, backups=LOG_COUNT)
    handler.setFormatter(formatter)
    log = Logger(name, level=level)
    log.addHandler(handler)
    return log

def getFormatter(name: str = LOG_FORMAT) -> logging.Formatter:
    msgFormat = LOG_FORMATS.get(name, LOG_FORMATS["std"])
    return logging.Formatter(msgFormat, datefmt=DATE_FORMAT)


#-------------------------------------------------------------------
# MODULE OBJECTS
#-------------------------------------------------------------------
logger = getFileLogger(__pkg_name__, LOG_LEVEL, LOG_FORMAT)

outlog = Outlog(logger)

x_logger = logger

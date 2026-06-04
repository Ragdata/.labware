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
import logging, sys

sys.path.append(".")

from pathlib import Path
from typing import TextIO, Any
from logging.handlers import RotatingFileHandler

from labware.output import *

BASEDIR = Path(config.get("paths", "base"))

LOG_LEVEL: int   = config.getint("logging", "level")
LOG_DIR: Path    = Path.home() / config.get("logging", "logdir")
LOG_SIZE: int    = config.getint("logging", "size")
LOG_COUNT: int   = config.getint("logging", "count")
LOG_FORMAT: str  = config.get("logging", "format")
# Request interpolation so escaped percent sequences (%%) become single '%' for strftime
CON_FORMAT: str  = config.get("log_formats", "console")
DATE_FORMAT: str = config.get("log_formats", "date")

LOG_FORMATS = {
    "std": config.get("log_formats", "std"),
    "short": config.get("log_formats", "short"),
    "long": config.get("log_formats", "long"),
    "console": config.get("log_formats", "console"),
}

#-------------------------------------------------------------------
# Logger Class
#-------------------------------------------------------------------
class Logger(logging.Logger):
    """Custom labware logger class"""

    def __init__(self, name: str, level: int = LOG_LEVEL, **kwargs) -> None:
        """
        Initialise the logger with a name and level

        Args:
            name (str):     Name of the logger
            level (int):    Logging level. (Defaults to logging.INFO)
            **kwargs:       Additional keyword arguments for logging config
        """
        super().__init__(name, level)
        self.setLevel(level)

    def critical(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log a CRITICAL message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.CRITICAL, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "error")
        if xit:
            exit(xit)

    def debug(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log a DEBUG message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.DEBUG, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "debug")
        if xit:
            exit(xit)

    def default(self, msg: str, out: bool = True, xit: int = 0, *args, **kwargs) -> None:
        """
        Log a DEFAULT message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.INFO, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "default")
        if xit:
            exit(xit)

    def error(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log an ERROR message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.ERROR, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "error")
        if xit:
            exit(xit)

    def exception(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log an ERROR message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.ERROR, msg, *args, exc_info=True, **kwargs)
        if out:
            self.outlog(msg, "error")
        if xit:
            exit(xit)

    def fatal(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log a FATAL message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.FATAL, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "error")
        if xit:
            exit(xit)

    def important(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log an IMPORTANT message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.INFO, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "important")
        if xit:
            exit(xit)

    def info(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log an INFO message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.INFO, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "info")
        if xit:
            exit(xit)

    def success(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log a SUCCESS message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.INFO, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "success")
        if xit:
            exit(xit)

    def tip(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log a TIP message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.INFO, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "tip")
        if xit:
            exit(xit)

    def warning(self, msg:str, out: bool = False, xit: int = 0, *args, **kwargs) -> None:
        """
        Log a WARNING message

        Args:
            msg (str):      The message to log
            out (bool):     Print the message to console (Defaults to False)
            xit (int):      Exit the program with this code after logging (Defaults to 0)
            *args:          Variable length argument list
            **kwargs:       Arbitrary keyword arguments
        """
        self.log(logging.WARNING, msg, *args, **kwargs)
        if out:
            self.outlog(msg, "warning")
        if xit:
            exit(xit)

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

    @staticmethod
    def outlog(msg: str, style: Optional[str] = None) -> None:
        """
        Print a message to the console with an optional style.

        Args:
        	msg (str):      The message to log and print.
        	style (str):    The style to apply to the message. (Optional)
        """
        if style is not None:
            symbol = config.get("symbols", style)
            msg = f"{symbol} {msg}"
        else:
            style = "default"
        printMessage(msg, style=style)

#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def initRotatingFileHandler(name: str, path: Path = LOG_DIR, maxSize: int = LOG_SIZE, backups: int = LOG_COUNT) -> RotatingFileHandler:
    """
    Initialise and return a RotatingFileHandler.

    Args:
    	name (str):     Name of the logger.
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
    Initialise and return a StreamHandler.

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
# noinspection PyProtectedMember
def get_logger(name: str, level: int = LOG_LEVEL, fmt: str = LOG_FORMAT) -> Logger:
    """
    Get or create a global logger instance with the specified name, level, and format.

    Args:
    	name (str):     Name of the logger.
    	level (int):    Logging level for the logger (default is LOG_LEVEL).
    	fmt (str):      Log format string (default is LOG_FORMAT).

    Returns:
    	Logger: Configured singleton logger instance.
    """
    try:
        if not hasattr(get_logger, "_instances"):
            get_logger._instances = dict()
        if name not in get_logger._instances:
            get_logger._instances[name] = getFileLogger(name, level=level, fmt=fmt)
    except Exception as e:
        console.print(f"Could not instantiate logger: {e}", style="error", highlight=False)
        exit(1)

    return get_logger._instances[name]

logger: Logger = ""

if not isinstance(logger, Logger):
    logger = get_logger("labware")

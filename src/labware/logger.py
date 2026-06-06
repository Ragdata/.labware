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

LOGGER MODULE

This module provides a flexible logging system for use within the labware
package and by external modules/packages.

Key Features:
    - Supports multiple named logger instances simultaneously
    - Lazy initialization - loggers created on-demand
    - Graceful fallback to defaults if config unavailable
    - Optional console output via Rich library
    - Rotating file handlers for log persistence
    - Easy external usage: from labware.logger import get_logger

Usage Examples:
    # Within labware package:
    from labware.logger import get_logger
    logger = get_logger("my_module")
    logger.info("message", out=True)

    # From external package:
    from labware.logger import get_logger
    logger = get_logger("external_app")
    logger.warning("something happened")
"""
import sys, logging

sys.path.append(".")

from pathlib import Path
from typing import TextIO, Any, Optional
from logging.handlers import RotatingFileHandler

# Default logging configuration - used when config module is unavailable
DEFAULT_LOG_CONFIG = {
    "level": logging.INFO,
    "size": 1048576,  # 1 MB
    "count": 3,
    "format": "std",
    "logdir": ".labware/log",
    "formats": {
        "std": "%(asctime)s :: %(levelname)s :: %(message)s",
        "short": "%(levelname)s :: %(message)s",
        "long": "%(asctime)s :: %(levelname)s :: %(message)s in %(filename)s\n%(pathname)s [ %(funcName)s line %(lineno)s ]",
        "console": "%(message)s",
    },
    "date": "%Y-%m-%d %H:%M:%S",
}

# Try to import config and output modules - these are optional
try:
    from labware.output import printMessage, config as cfg
    HAS_OUTPUT = True
except ImportError:
    HAS_OUTPUT = False
    cfg = None

# Initialise logging configuration with a lazy-load approach
_log_config = None

def _get_config():
    """
    Lazily load and cache the logging configuration.
    Falls back to default if the config module is unavailable.
    """
    global _log_config
    if _log_config is not None:
        return _log_config

    _log_config = DEFAULT_LOG_CONFIG.copy()

    try:
        if HAS_OUTPUT and cfg is not None:
            _log_config["level"] = cfg.getint("logging", "level")
            _log_config["size"] = cfg.getint("logging", "size")
            _log_config["count"] = cfg.getint("logging", "count")
            _log_config["format"] = cfg.get("logging", "format")
            _log_config["logdir"] = cfg.get("logging", "logdir")
            _log_config["formats"]["std"] = cfg.get("log_formats", "std")
            _log_config["formats"]["short"] = cfg.get("log_formats", "short")
            _log_config["formats"]["long"] = cfg.get("log_formats", "long")
            _log_config["formats"]["console"] = cfg.get("log_formats", "console")
            _log_config["date"] = cfg.get("log_formats", "date")
    except Exception:
        # If config fails for any reason, we continue with defaults
        pass

    return _log_config

# Convenience functions to get config values
def get_log_level():
    """Get the configured logging level"""
    return _get_config()["level"]

def get_log_dir():
    """Get the configured log directory"""
    return Path.home() / str(_get_config()["logdir"])

def get_log_size():
    """Get the configured max log file size"""
    return _get_config()["size"]

def get_log_count():
    """Get the configured number of backup log files"""
    return _get_config()["count"]

def get_log_format():
    """Get the configured default log format style name"""
    return _get_config()["format"]

def get_date_format():
    """Get the configured date format string"""
    return _get_config()["date"]

def get_log_formats():
    """Get the log format strings dictionary"""
    return _get_config()["formats"]

#-------------------------------------------------------------------
# Logger Class
#-------------------------------------------------------------------
class Logger(logging.Logger):
    """
    Custom labware logger class with enhanced functionality.

    Supports both standard Python logging and optional rich console output.
    Multiple instances can be created with different names for different modules.
    """

    def __init__(self, name: str, level: Optional[int] = None, **kwargs) -> None:
        """
        Initialise the logger with a name and level

        Args:
            name (str):         Name of the logger
            level (int):        Logging level (defaults to config value or logging.INFO)
            **kwargs:           Additional keyword arguments for logging config
        """
        if level is None:
            level = _get_config()["level"]
        super().__init__(name, str(level))
        self.setLevel(str(level))

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

        Uses the Rich library for styled output if available.
        Falls back to plain print if Rich is not available.

        Args:
        	msg (str):      The message to log and print.
        	style (str):    The style to apply to the message. (Optional)
        """
        if HAS_OUTPUT and cfg is not None:
            try:
                if style is not None:
                    symbol = cfg.get("symbols", style)
                    msg = f"{symbol} {msg}"
                printMessage(msg, style=style)
            except Exception:
                # Fallback if config access fails
                print(msg)
        else:
            # No Rich output available, use standard print
            print(msg)

#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def initRotatingFileHandler(name: str, path: Optional[Path] = None, maxSize: Optional[int] = None, backups: Optional[int] = None) -> RotatingFileHandler:
    """
    Initialise and return a RotatingFileHandler.

    Args:
    	name (str):         Name of the logger (used for filename).
    	path (Path):        Directory where the log file will be stored
                           (default from config or ~/.labware/log).
    	maxSize (int):      Maximum size of the log file before rotation
                           (default from config or 1 MB).
    	backups (int):      Number of backup files to keep
                           (default from config or 3).

    Returns:
    	RotatingFileHandler: Configured file handler instance.
    """
    cfg = _get_config()
    if path is None:
        path = Path.home() / str(cfg["logdir"])
    if maxSize is None:
        maxSize = cfg["size"]
    if backups is None:
        backups = cfg["count"]

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True, mode=0o755)

    logFile = path / f"{name}.log"
    return RotatingFileHandler(logFile, maxBytes=int(str(maxSize)), backupCount=int(str(backups)), encoding='utf-8', delay=False)

def initStreamHandler(stream: Optional[TextIO | Any] = None, level: Optional[int] = None, style: str = "console") -> logging.StreamHandler:
    """
    Initialise and return a StreamHandler for console output.

    Args:
    	stream (TextIO | Any):  The stream (default is sys.stdout).
    	level (int):            Logging level (default from config).
    	style (str):            Log format style name (default "console").

    Returns:
    	logging.StreamHandler: Configured stream handler instance.
    """
    if stream is None:
        stream = sys.stdout
    if level is None:
        level = _get_config()["level"]

    handler = logging.StreamHandler(stream)
    handler.setLevel(str(level))
    return handler

def getFileLogger(name: str, level: Optional[int] = None, fmt: str = "std", add_stream: bool = False) -> Logger:
    """
    Create a file logger with an optional console handler.

    Args:
        name (str):         Name of the logger
        level (int):        Logging level (default from config)
        fmt (str):          Log format style name (default "std")
        add_stream (bool):  Also add a stream handler (default False)

    Returns:
        Logger: Configured logger instance
    """
    if level is None:
        level = _get_config()["level"]

    log = Logger(name, level=int(str(level)))

    # Add file handler
    formatter = getFormatter(fmt)
    file_handler = initRotatingFileHandler(name)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    # Optionally add stream handler
    if add_stream:
        stream_handler = initStreamHandler(level=int(str(level)))
        console_formatter = getFormatter("console")
        stream_handler.setFormatter(console_formatter)
        log.addHandler(stream_handler)

    return log

def getFormatter(name: str = "std") -> logging.Formatter:
    """
    Get a logging formatter with the specified format style.

    Args:
        name (str): Format style name (default "std")

    Returns:
        logging.Formatter: Configured formatter instance
    """
    formats = get_log_formats()
    cfg = _get_config()
    msgFormat = formats.get(name, formats["std"])
    return logging.Formatter(msgFormat, datefmt=str(cfg["date"]))

#-------------------------------------------------------------------
# MODULE OBJECTS
#-------------------------------------------------------------------
# noinspection PyProtectedMember
def get_logger(name: str, level: Optional[int] = None, fmt: str = "std", add_stream: bool = False) -> Logger:
    """
    Get or create a logger instance.

    This is the primary function for getting loggers. It maintains
    a global registry of logger instances, keyed by name. Multiple calls
    with the same name return the same logger instance (singleton per name).

    Supports usage from:
        - labware package modules
        - External scripts and packages

    The logger will automatically fall back to defaults if the config
    module is not available, making it suitable for use in any context.

    Args:
    	name (str):             Name of the logger (e.g., "myapp", "myapp.module")
    	level (int):            Logging level (default from config or logging.INFO)
    	fmt (str):              Log format style name: "std", "short", "long", "console"
                               (default "std")
    	add_stream (bool):       Also add console output via stream handler (default False)

    Returns:
    	Logger: Configured logger instance. Same instance returned for same name.

    Raises:
    	Exception: Only if logger creation catastrophically fails (very rare).

    Examples:
        # Basic usage - file logging only
        logger = get_logger("myapp")
        logger.info("Application started")

        # With console output
        logger = get_logger("myapp", add_stream=True)
        logger.info("message", out=True)

        # Custom log level
        logger = get_logger("debug_logger", level=logging.DEBUG)
        logger.debug("Detailed debug info")

        # From external package
        from labware.logger import get_logger
        log = get_logger("external_app")
    """
    try:
        if not hasattr(get_logger, "_instances"):
            get_logger._instances = {}
        if name not in get_logger._instances:
            get_logger._instances[name] = getFileLogger(name, level=level, fmt=fmt, add_stream=add_stream)
    except Exception as e:
        # Last resort: try to output error and fall back to basic logger
        try:
            print(f"Error instantiating logger '{name}': {e}", file=sys.stderr)
        except Exception:
            pass

        # Return a minimal functional logger
        basic_logger = Logger(name)
        basic_logger.addHandler(logging.StreamHandler(sys.stderr))
        return basic_logger

    return get_logger._instances[name]


#-------------------------------------------------------------------
# INITIALIZATION
#-------------------------------------------------------------------
# Create a module-level logger for the labware package
logger: Logger = get_logger("labware")

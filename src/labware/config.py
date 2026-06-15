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

Configuration Management Module

This module provides a centralized configuration system that:
    - Defines sensible defaults for all modules
    - Allows external configuration file overrides
    - Provides a singleton config object accessible globally
    - Handles missing files gracefully with fallback defaults
"""
from __future__ import annotations

from pathlib import Path
from configparser import ConfigParser
from typing import Any, Dict, Optional

# ------------------------------------------------------------------
# DEFAULTS - Used by output module
# ------------------------------------------------------------------
DEFAULT_CONFIG: Dict[str, Dict[str, Any]] = {
    "symbols": {
        "info": "✚",
        "success": "🗸",
        "warning": "🛆",
        "error": "✘",
        "tip": "★",
        "important": "⚑",
        "debug": "⚙",
        "head": "➤",
        "dot": "⦁",
    },
    "styles": {
        "info": "dodger_blue1",
        "success": "bright_green",
        "warning": "dark_orange",
        "error": "bright_red",
        "tip": "cyan3",
        "important": "purple3",
        "debug": "white",
        "head": "dark_goldenrod",
        "dot": "green",
    },
    "colors": {
        "red": "dark_red",
        "bright_red": "red3",
        "green": "green4",
        "bright_green": "green3",
        "yellow": "gold3",
        "bright_yellow": "yellow1",
        "blue": "dodger_blue3",
        "bright_blue": "dodger_blue1",
        "magenta": "dark_magenta",
        "bright_magenta": "purple",
        "cyan": "cyan3",
        "bright_cyan": "cyan1",
        "white": "white",
        "bright_white": "bright_white",
        "black": "black",
        "bright_black": "bright_black",
        "accent1": "purple4",
        "accent2": "sky_blue2",
    },
    "logging": {
        "level": "20",
        "size": "1048576",
        "count": "3",
        "format": "std",
        "logdir": ".labware/log",
    },
    "log_formats": {
        "std": "%%(asctime)s :: %%(levelname)s :: %%(message)s",
        "short": "%%(levelname)s :: %%(message)s",
        "long": "%%(asctime)s :: %%(levelname)s :: %%(message)s in %%(filename)s\\n%%(pathname)s [ %%(funcName)s line %%(lineno)s ]",
        "console": "%%(message)s",
        "date": "%%Y-%%m-%%d %%H:%%M:%%S",
    },
    "paths": {
        "base": "/opt/labware"
    },
    "setup": {
        "chceked": "False"
    }
}

# ------------------------------------------------------------------
# Config Class
# ------------------------------------------------------------------
# noinspection PyMethodOverriding
class Config(ConfigParser):
    """
    Enhanced configuration parser with defaults and overrides.

    This class extends ConfigParser to provide:
        - Automatic defaults from code-defined DEFAULT_CONFIG
        - Optional external config file overrides
        - Graceful fallback when files are missing
        - Type-safe get operations (get, getint, getbool)
    """

    def __init__(self, config_file: Optional[str | Path] = None, defaults: Optional[Dict[str, Dict[str, Any]]] = None):
        """
        Initialise the configuration.

        Args:
            config_file: Path to an external configuration file (optional)
            defaults: Dictionary of default values to set (optional)
                     If not provided, uses DEFAULT_CONFIG
        """
        # Disable interpolation to allow % characters in values (like datetime formats)
        # super().__init__(interpolation=None)
        super().__init__()
        if defaults is None:
            defaults = DEFAULT_CONFIG
        # Populate sections/options from defaults
        self._set_defaults(defaults)

        # If an explicit config_file is provided, attempt to load it
        if config_file is not None:
            self._load_config_file(config_file)

    def _set_defaults(self, defaults: Dict[str, Dict[str, Any]]) -> None:
        """
        Set default configuration values from a dictionary.

        Args:
            defaults: Dictionary with structure {section: {option: value}}
        """
        for section, options in defaults.items():
            if not self.has_section(section):
                self.add_section(section)
            for option, value in options.items():
                # Only set if not already set
                if not self.has_option(section, option):
                    self.set(section, option, str(value))

    def _load_config_file(self, config_file: str | Path) -> None:
        """
        Load configuration from an external file.

        Args:
            config_file: Path to a configuration file

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        if not isinstance(config_file, Path):
            config_file = Path(config_file)

        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: '{config_file}'")

        self.read(config_file)

    def _exists(self, section: str, option: str) -> bool:
        return self.has_section(section) and self.has_option(section, option)

    def get(self, section: str, option: str, fallback: Optional[Any] = None, **kwargs) -> str:
        """
        Get a configuration value with fallback support.

        Args:
            section: Configuration section
            option: Configuration option/key
            fallback: Fallback value if not found

        Returns:
            Configuration value as string
        """
        try:
            return super().get(section, option, **kwargs)
        except Exception:
            if fallback is not None:
                return str(fallback)
            # Try DEFAULT_CONFIG for final fallback
            try:
                if DEFAULT_CONFIG[section][option]:
                    return str(DEFAULT_CONFIG[section][option])
                else:
                    raise KeyError(f"Option '{option}' not found in section '{section}'")
            except Exception:
                return ""

    def getint(self, section: str, option: str, fallback: Optional[int] = None) -> int:
        """
        Get a configuration value as an integer.

        Args:
            section: Configuration section
            option: Configuration option/key
            fallback: Fallback value if not found

        Returns:
            Configuration value as integer
        """
        try:
            return super().getint(section, option)
        except Exception:
            if fallback is not None:
                return fallback
            # Try DEFAULT_CONFIG as final fallback
            try:
                return int(DEFAULT_CONFIG[section][option])
            except Exception:
                return 0

    def getbool(self, section: str, option: str, fallback: Optional[bool] = None) -> bool:
        """
        Get a configuration value as a boolean.

        Args:
            section: Configuration section
            option: Configuration option/key
            fallback: Fallback value if not found

        Returns:
            Configuration value as boolean
        """
        try:
            return super().getboolean(section, option)
        except Exception:
            if fallback is not None:
                return fallback
            # Try DEFAULT_CONFIG as final fallback
            try:
                val = DEFAULT_CONFIG[section][option]
                if isinstance(val, bool):
                    return val
                if isinstance(val, str):
                    return val.lower() in ('true', '1', 'yes', 'on')
                return bool(val)
            except Exception:
                return False

# ------------------------------------------------------------------
# SINGLETON ACCESSOR
# ------------------------------------------------------------------
# noinspection PyProtectedMember
def get_config(config_file: Optional[str | Path] = None) -> Config:
    """
    Get or create the global config instance.

    Args:
        config_file: Optional path to an external config file
                    (only used on the first call)

    Returns:
        Config: The singleton configuration instance
    """
    if not hasattr(get_config, '_instance'):
        # Try to find config file in standard locations
        if config_file is None:
            home = Path.home()
            standard_locations = [
                home / '.labware.cfg',
                home / '.labware' / '.labware.cfg',
                Path('/opt/labware/.labware.cfg'),
                Path('/usr/share/labware/.labware.cfg'),
            ]

            for location in standard_locations:
                if location.exists():
                    config_file = location
                    break

        # Create instance with or without file
        if config_file:
            try:
                get_config._instance = Config(config_file=config_file)
            except FileNotFoundError:
                # File specified but not found, use defaults
                get_config._instance = Config()
        else:
            # No file found, use defaults only
            get_config._instance = Config()
    elif config_file is not None:
        # Instance already exists, but a new config_file is provided
        # Attempt to load it as an override
        try:
            get_config._instance._load_config_file(config_file)
        except FileNotFoundError:
            pass  # Ignore if file not found, keep existing config

    return get_config._instance

# Create module-level singleton for backward compatibility
config: Config = get_config()

__all__ = ['Config', 'get_config', 'config', 'DEFAULT_CONFIG']

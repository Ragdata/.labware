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
from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.read(str(Path(__file__).parent / "config" / ".default.cfg"))

user_dir = Path.home()
user_cfg = user_dir / ".labware.cfg"
if user_cfg.exists():
	config.read(str(user_cfg))

x_config = config

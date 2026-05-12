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
import sys

sys.path.append('.')

from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.read('./config/.default.cfg')

userDir = Path.home()
userCfg = userDir / ".labware.cfg"
if userCfg.exists():
	config.read(str(userCfg))

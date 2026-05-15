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

BASEDIR = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT = BASEDIR / "scr" / "setup" / ".default.cfg"

if not DEFAULT.exists():
    raise FileNotFoundError(f"Config file not found: '{DEFAULT}'")

config = ConfigParser()
config.read(str(DEFAULT))

config.add_section('paths')

config["paths"]["base"] = str(BASEDIR)

userDir = Path.home()
userCfg = userDir / ".labware.cfg"
if userCfg.exists():
	config.read(str(userCfg))

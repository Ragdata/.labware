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
from pathlib import Path

__pkg_name__ = 'labware'
__version__  = '0.1.0'

#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def version(output: bool = True):
	"""Print the package version"""
	if output:
		# Print version to console
		print(f"{__pkg_name__.capitalize()} version {__version__}")
	else:
		# Return the version string
		return f"{__version__}"
	return None


#-------------------------------------------------------------------
# MODULE OBJECTS
#-------------------------------------------------------------------
register = Path.home() / ".labware/reg/registry"
regisdir = register.parent

if not register.exists():
	regisdir.mkdir(parents=True, exist_ok=True)

registry = 

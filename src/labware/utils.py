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
import shutil

from pathlib import Path
from datetime import datetime


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def backup(filepath: Path = Path("."), backupdir: Path = Path(".")) -> bool:
	"""Backup a file to the specified directory"""
	if not filepath.exists():
		raise FileNotFoundError(f"{filepath} does not exist")
	if not backupdir.exists():
		backupdir.mkdir(parents=True, exist_ok=True, mode=0o755)

	now = datetime.now()
	backupfile = backupdir / f"{filepath.name}_{now.strftime('%Y%m%d_%H%M%S')}.bak"

	try:
		if shutil.copy2(filepath, backupfile):
			return True
	except Exception as e:
		raise RuntimeError(f"Failed to backup file {filepath}: {e}")

	return False

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
import shutil, sys, os, subprocess

sys.path.append('.')

from typing import List
from datetime import datetime

from logger import *


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def backup(filepath: Path = Path("."), backupdir: Path = Path(".")) -> bool:
    """Backup a file to the specified directory"""
    if not filepath.exists():
        raise FileNotFoundError(f"{filepath} does not exist")
    if not backupdir.exists():
        backupdir.mkdir(parents=True, exist_ok=True, mode=0o755)

    suffix = '.'.join(filepath.suffixes)
    now = datetime.now()
    backupfile = backupdir / f"{filepath.name}.{suffix}_{now.strftime('%Y%m%d-%H%M%S')}.bak"

    try:
        if shutil.copy2(filepath, backupfile):
            return True
    except Exception as e:
        raise RuntimeError(f"Failed to backup file {filepath}: {e}")

    return False

def checkPython() -> None:
    if sys.version_info < (3, 12):
        errorExit(f"Requires Python 3.12 or later")
    else:
        printSuccess("Python 3.12 or later confirmed")

def checkRoot() -> None:
    if os.geteuid() != 0:
        errorExit(f"Root privileges required")
    else:
        printSuccess("Root privileges confirmed")

def checkUbuntu() -> None:
    version = run("lsb_release -rs", capture=True).stdout.strip()
    if version != "24.04":
        errorExit(f"Expected Ubuntu 24.04, found '{version}'")
    else:
        printSuccess("Ubuntu 24.04 confirmed")

def copy(src: Path, dst: Path, bkp: bool = False, mode: str = '0o644', owner: str = None) -> bool:
    pass

def getList(filepath: Path) -> list:
    if not filepath.exists:
        raise FileNotFoundError(f"{filepath} does not exist")
    try:
        with open(str(filepath), 'r') as f:
            lines = [l.strip() for l in f]
            return lines
    except Exception as e:
        raise e

def installAPT(packages: list):
    try:
        for pkg in packages:
            if pkg[0] == "#":
                continue
            result = run(f"dpkg -s {pkg}", check=False, capture=True)
            if result.returncode != 0:
                run(f"DEBIAN_FRONTEND=noninteractive apt install -y {pkg}")
                printDot(f"Installed package: {pkg}")
                logger.info(f"Installed package: {pkg}")
            else:
                printDot(f"Package already installed: {pkg}")
                logger.debug(f"Package already installed: {pkg}")
    except Exception as e:
        raise e

def installPIP(packages: list):
    try:
        for pkg in packages:
            if pkg[0] == "#":
                continue
            result = run(f"pip show {pkg}", check=False, capture=True)
            if result.returncode != 0:
                run(f"pip install {pkg} --break-system-packages")
                printDot(f"Installed python package: {pkg}")
                logger.info(f"Installed python package: {pkg}")
            else:
                printDot(f"Package already installed: {pkg}")
                logger.debug(f"Package already installed: {pkg}")
    except Exception as e:
        raise e

def run(command: str, check: bool = True, capture: bool = False, input_txt = None) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[Any] :
    """Execute shell command with error handling"""
    try:
        if not capture:
            printDot(f"{command}")
        result = subprocess.run(command, shell=True, check=check, text=True, capture_output=capture, input=input_txt)
        return result
    except subprocess.CalledProcessError as e:
        outlog.logError(f"Command failed: {command}\n{e.stderr.strip()}")
        if check:
            sys.exit(1)
        raise e

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
import os, subprocess, pwd, sys

from pathlib import Path

BASEDIR = Path(__file__).parents[2]

sys.path.append(str(BASEDIR))

from labware.logger import *

#-------------------------------------------------------------------
# MODULE VARIABLES
#-------------------------------------------------------------------
# BASEDIR = Path(config.get("paths", "base"))
#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def checkPython() -> None:
    if sys.version_info < (3, 12):
        logger.error(f"Requires Python 3.14 or later", True, 1)
    else:
        printSuccess("Python 3.14 or later confirmed")

def checkRoot() -> None:
    if os.geteuid() != 0:
        logger.error(f"Root privileges required", True, 1)
    else:
        printSuccess("Root privileges confirmed")

def checkUbuntu() -> None:
    version = run("lsb_release -rs", capture=True).stdout.strip()
    if version != "24.04":
        logger.error(f"Expected Ubuntu 24.04, found '{version}'", True, 1)
    else:
        printSuccess("Ubuntu 24.04 confirmed")

def getIP() -> str:
    if run("resolvectl status >/dev/null 2>&1").returncode == 0:
        ip = run('ip route get "$(resolvectl status | grep -E \'DNS (Server:|Servers:)\' | tail -n1 | awk \'{print $NF}\')" | grep -Eo \'[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+\' | tail -n1', capture=True).stdout.strip()
    else:
        ip = run('ip route get "$(grep \'^nameserver\' /etc/resolv.conf | tail -n1 | awk \'{print $NF}\')" | grep -Eo \'[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+\' | tail -n1', capture=True).stdout.strip()
    return ip

def getUserIP() -> str:
    ip = run("who | awk '{print $NF}' | tr -d '()' | grep -E '^[0-9]' | head -n1").stdout.strip()
    return ip

def installAPT(packages: list):
    try:
        for pkg in packages:
            if pkg[0] == "#":
                continue
            if run(f"dpkg -s {pkg}", check=False, capture=True).returncode != 0:
                run(f"DEBIAN_FRONTEND=noninteractive apt install -y {pkg}")
                printSuccess(f"Installed package: {pkg}")
                logger.info(f"Installed package: {pkg}")
            else:
                printDot(f"Package already installed: {pkg}")
                logger.debug(f"Package already installed: {pkg}")
    except Exception as e:
        reason = str(e)
        logger.error(f"Install package failed: {reason}", True)
        raise

def installPIP(packages: list):
    try:
        for pkg in packages:
            if pkg[0] == "#":
                continue
            if run(f"pip show {pkg}", check=False, capture=True).returncode != 0:
                run(f"pip install --user {pkg} --break-system-packages")
                printSuccess(f"Installed python package: {pkg}")
                logger.info(f"Installed python package: {pkg}")
            else:
                printDot(f"Package already installed: {pkg}")
                logger.debug(f"Package already installed: {pkg}")
    except Exception as e:
        reason = str(e)
        logger.error(f"Install failed: {reason}", True)
        raise

def isLXC() -> bool:
    ret = True if run("grep -qE 'container=lxc|container=lxd' /proc/1/environ").returncode == 0 else False
    return ret

def removeAPT(packages: list):
    try:
        for pkg in packages:
            if pkg[0] == "#":
                continue
            if run(f"dpkg -s {pkg}", check=False, capture=True).returncode == 0:
                run(f"apt autopurge -y {pkg}")
                printSuccess(f"Removed package: {pkg}")
                logger.info(f"Removed package: {pkg}")
            else:
                printError(f"Package not installed: {pkg}")
                logger.debug(f"Package not installed: {pkg}")
    except Exception as e:
        reason = str(e)
        logger.error(f"Remove package failed: {reason}", True)
        raise

def removeUsers(users: list) -> bool:
    try:
        for user in users:
            if run(f"id {user}").returncode == 0:
                run(f"pkill -u {user}")
                if run(f"userdel -r {user}").returncode == 0:
                    printSuccess(f"Removed user: {user}")
                    logger.info(f"Removed user: {user}")
                else:
                    logger.error(f"Failed to remove user: {user}", True)
            else:
                logger.warning(f"User not found: {user}", True)
        return True
    except Exception as e:
        reason = str(e)
        logger.error(f"Remove user failed: {reason}", True)
        raise

def run(command: str, check: bool = True, capture: bool = False, input_txt = None) -> subprocess.CompletedProcess[Any] :
    """Execute shell command with error handling"""
    try:
        logger.info(f"Executing BASH: {command}")
        result = subprocess.run(command, shell=True, check=check, text=True, capture_output=capture, input=input_txt)
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}\n{e.stderr.strip()}", True)
        if check:
            sys.exit(1)
        raise

def userExists(uname) -> bool:
    try:
        pwd.getpwnam(uname)
        return True
    except KeyError:
        return False

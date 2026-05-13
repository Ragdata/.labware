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
import shutil, sys, os, subprocess, getpass, pwd, grp

sys.path.append('.')

from datetime import datetime

from logger import *


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def backup(filepath: Path, backupdir: Path = Path.home() / ".backup") -> bool:
    """Backup a file to the specified directory"""
    try:
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath} does not exist")
        if not backupdir.exists():
            backupdir.mkdir(parents=True, exist_ok=True, mode=0o755)

        # suffix = '.'.join(filepath.suffixes)
        now = datetime.now()
        backupfile = backupdir / f"{filepath.name}.{now.strftime('%Y%m%d-%H%M.%S')}"

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

def chmod(tgt: Path, mode: int = 0o644) -> None:
    """Smart / Recursive chmod"""
    if tgt.exists():
        os.chmod(tgt, mode)
        if tgt.is_dir():
            for root, dirs, files in os.walk(tgt):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o755)
                for f in files:
                    os.chmod(os.path.join(root, f), mode)

def chown(tgt: Path, user: str, group: str) -> None:
    """Smart / Recursive chown"""
    if tgt.exists():
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
        os.chown(tgt, uid, gid)
        if tgt.is_dir():
            for root, dirs, files in os.walk(tgt):
                for name in dirs + files:
                    os.chown(os.path.join(root, name), uid, gid)

def copyFiles(src: Path, dst: Path, bkp: bool = False, mode: int = 0o644, user: str = "", group: str = "") -> None:
    try:
        if not user:
            user = os.environ.get('USER')
        printDot(f"{user}")
        exit
        if not group:
            group = user
        if not userExists(user):
            raise RuntimeError(f"User '{user}' does not exist")
        if not src.exists():
            raise FileNotFoundError(f"{src} does not exist")
        if not dst.exists():
            dst.mkdir(parents=True, mode=0o755)
        if src.is_file():
            if dst.is_file() and bkp:
                backup(src, dst.parent)
            shutil.copy(src, dst)
            chown(dst, user, group)
            chmod(dst, mode)
            printDot(f"Copied {src.name}")
            logger.debug(f"Copied {src.name}")
        elif src.is_dir() and dst.is_dir():
            for item in os.scandir(src):
                dest = dst / item.name
                if item.is_file():
                    if shutil.copy(item, dest):
                        chown(dest, user, group)
                        chmod(dest, mode)
                        printDot(f"Copied '{item.name}'")
                        logger.debug(f"Copied '{item.name}'")
                    else:
                        printWarning(f"Copy Failed '{item.name}'")
                        logger.debug(f"Copy Failed '{item.name}'")
                elif item.is_dir():
                    if shutil.copytree(item, dest, dirs_exist_ok=True):
                        chown(dest, user, group)
                        chmod(dest, mode)
                        printDot(f"Copied Tree '{item.name}'")
                        logger.debug(f"Copied Tree '{item.name}'")
                    else:
                        printWarning(f"Copy Tree Failed '{item.name}'")
                        logger.debug(f"Copy Tree Failed '{item.name}'")
                else:
                    pass
        else:
            raise TypeError(f"Invalid type copying {src} -> {dst}")
    except Exception as e:
        raise e

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
                run(f"pip install --user {pkg} --break-system-packages")
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

def userExists(uname) -> bool:
    try:
        pwd.getpwnam(uname)
        return True
    except KeyError:
        return False

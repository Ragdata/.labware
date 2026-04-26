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
import os
import shutil
import subprocess
import typer

from .logger import *

app = typer.Typer(name="install", rich_markup_mode="rich", no_args_is_help=True)


#-------------------------------------------------------------------
# MODULE VARIABLES
#-------------------------------------------------------------------
NEW_USER: str = ""
SCR_PATH: Path = Path(__file__).resolve()
REPO_PATH: Path = SCR_PATH.parent.parent.parent


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def appBanner() -> None:
    logger.info("Labware Installer Started")
    line()
    rule("[bold yellow]Labware Installer")
    line()

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

def copyFiles(debug: Optional[bool] = False) -> bool:
    try:
        printHead("Copying Files")
        line()
        logger.info("Copying Files")
		
        # for name, stub in config['dirs'].items():
        #     repodir = REPO_PATH / stub
        #     userdir = Path.home() / '.labware' / stub
        #     if not userdir.exists():
        #         userdir.mkdir(parents=True, exist_ok=True)
        #         if debug:
        #             outlog.logDebug(f"Created Directory '{userdir}'")
        #     if repodir.exists():
        #         for filename in os.scandir(repodir):
        #             filepath = filename.path
        #             userpath = userdir / filename.name
        #             if filename.is_file():
        #                 shutil.copy2(filepath, userpath)
        #             elif filename.is_dir() and not userpath.exists():
        #                 shutil.copytree(filepath, userpath)
        #             outlog.logSuccess(f"Copied '{filepath}' to '{userpath}'")
        #     else:
        #         outlog.logWarning(f"Source directory '{repodir}' does not exist")
    except Exception as e:
        outlog.logError(f"File Copy Error: {e}")
        return False
    line()
    printSuccess("DONE!")
    return True

def installDotfiles(debug: Optional[bool] = False, homedir: Optional[Path] = None) -> bool:
    try:
        printHead("Installing Dotfiles")
        line()
        logger.info("Installing Dotfiles")
        dotdir = Path.home() / '.labware' / config.get("dirs", "dot")
        if not dotdir.exists():
            errorExit(f"Unexpected fault - unable to find '{dotdir}'")

    except Exception as e:
        errorExit(f"Error installing Dotfiles: {e}")
        return False
    return True

def run(command: str, check=True, capture=False, input_txt=None):
    """ Execute shell command with error handling """
    try:
        if not capture:
            printDot(f"{command}")
        result = subprocess.run(command, shell=True, check=check, text=True, capture_output=capture, input=input_txt)
        return result
    except subprocess.CalledProcessError as e:
        outlog.logError(f"Command failed: {command}\n{e.stderr.strip()}")
        if check:
            sys.exit(1)
        return e

def getSudoUsers():
    """ Get list of users in sudo group """
    result = run("getent group sudo | cut -d: -f4", capture=True)
    return result.stdout.strip().split(',') if result.stdout.strip() else []

def promptUsername():
    """ Smart Username Prompt """
    global NEW_USER
    existing_users = getSudoUsers()
    if existing_users and existing_users != ['']:
        printSuccess(f"Found existing sudo users: {', '.join(existing_users)}")
        use_existing = input("Use an existing sudo user? (y/N): ").lower()
        if use_existing == 'y':
            while True:
                user = input("Enter existing username: ").strip().lower()
                if user in existing_users:
                    NEW_USER = user
                    printSuccess(f"Using existing sudo user: {NEW_USER}")
                    return
                printError(f"User '{user}' not found or not in sudo group.")
        while True:
            user = input("New sudo username: ").strip().lower()
            if user.isalnum() and len(user) <= 32:
                NEW_USER = user
                break
            printError(f"Use lowercase alphanumeric, max 32 chars")

def userExists():
    return run(f"id {NEW_USER}", check=False, capture=True).returncode == 0

#-------------------------------------------------------------------
# MODULE COMMANDS
#-------------------------------------------------------------------
def cmd(debug: Optional[bool] = False) -> None:
    """ Installer Entrypoint """
    homedir = Path.home()
    run("clear")
    appBanner()
    checkRoot()
    checkUbuntu()

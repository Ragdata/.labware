#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			12/05/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
from labware.filesys import *

BASEDIR = Path(__file__).parents[3].resolve() if not BASEDIR else BASEDIR

sys.path.append(str(BASEDIR))

CONFIG_FILE = BASEDIR / "scr" / "lab" / "cfg" / ".labware.cfg"

config = get_config(CONFIG_FILE)

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
SETUPDIR = BASEDIR / config.get("src", "setup")
REPODOT  = BASEDIR / config.get("src", "dot")
REPOLIB  = BASEDIR / config.get("src", "lib")
REPOSCR  = BASEDIR / "scr"
SERVSVC  = Path(config.get("paths", "opt")) / "svc"
# EXECUSR  = pwd.getpwuid(os.geteuid()).pw_name
# REALUSR  = getpass.getuser()
# SERVRIP  = getIP()
# USERSIP  = getUserIP()
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        run("clear")
        rule(f"[yellow]── USERS MODULE [/yellow]", style="yellow", align="left")
        line()
        # ----------------------------------------------------------
        # GATHER INFORMATION
        # ----------------------------------------------------------
        users = []
        while True:
            data = getData("[cyan]Enter list of sudo users to setup (space delimited): [/cyan]")
            if data != "":
                users = data.split(" ")
                for user in users:
                    if not userExists(user):
                        logger.error(f"User '{user}' does not exist", True, 1)
                break
            else:
                continue
        # ----------------------------------------------------------
        # COPY FILES TO USER DIR
        # ----------------------------------------------------------
        for user in users:
            USERDIR = Path(f"/home/{user}") if user != "root" else Path("/root")
            WARELIB = USERDIR / ".labware" / "lib"
            WARESCR = USERDIR / ".labware" / "scr"
            run("clear")
            rule(f"[yellow]── USERS MODULE [/yellow]", style="yellow", align="left")
            line()
            printWhite(f"COPYING FILES FOR USER '{user}'")
            if not WARELIB.exists():
                WARELIB.mkdir(parents=True, exist_ok=True)
            # Library Files
            line()
            printHead("Installing Library Files ...")
            copyFiles(REPOLIB, WARELIB, user=user)
            # Backup Dotfiles
            line()
            printHead("Backup Dotfiles ...")
            printSuccess("Backup '.bashrc'") if backup(USERDIR / ".bashrc") else printWarning("Failed to backup '.bashrc'")
            printSuccess("Backup '.profile'") if backup(USERDIR / ".profile") else printWarning("Failed to backup '.profile'")
            # Install Dotfiles
            line()
            printHead("Installing Dotfiles ...")
            copyFiles(REPODOT, USERDIR, user=user)
            line()
            if user == "root":
                if not WARESCR.exists():
                    WARESCR.mkdir(parents=True, exist_ok=True)
                if not SERVSVC.exists():
                    SERVSVC.mkdir(parents=True, exist_ok=True)
                line()
                printHead("Installing Labfiles ...")
                copyFiles(REPOSCR / "lab", WARESCR / "lab", user=user)
                line()
                printHead("Installing Packages ...")
                copyFiles(REPOSCR / "pkg", WARESCR / "pkg", user=user)
                line()
                printHead("Installing Services ...")
                copyFiles(BASEDIR / "svc", SERVSVC, user=user)
                line()
                printHead("Setting Permissions ...")
                for item in os.scandir(WARESCR / "lab"):
                    if item.is_file():
                        chmod(Path(item.path), mode=0o755)
                for item in os.scandir(WARESCR / "pkg"):
                    if item.is_file():
                        chmod(Path(item.path), mode=0o755)
                for item in os.scandir(WARESCR / "pkg" / "pve"):
                    if item.is_file():
                        chmod(Path(item.path), mode=0o755)
            line()
            getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
        # ----------------------------------------------------------
        # CONFIGURE USERS
        # ----------------------------------------------------------
        for user in users:
            USERDIR = Path(f"/home/{user}") if user != "root" else Path("/root")
            WAREDIR = USERDIR / ".labware"
            run("clear")
            rule(f"[yellow]── USERS MODULE [/yellow]", style="yellow", align="left")
            line()
            printWhite(f"CONFIGURING USER '{user}'")
            # SUDO NOPASSWD
            if user != "root":
                line()
                printDot("SUDO NOPASSWD")
                nopasswd = getData(f"[cyan]Allow user {user} to use sudo without a password?[/cyan] (y/N): ").lower()
                if nopasswd == "y":
                    data = f"{user} ALL=(ALL) NOPASSWD: ALL"
                    writeFile(Path(f"/etc/sudoers.d/{user}"), data, user=user)
            # ADD PGP KEY
            line()
            printDot("ADD PGP KEY")
            printCyan("Paste SECRET key (Ctrl+D to end/bypass):")
            gpgkey = sys.stdin.read()
            if gpgkey:
                file = Path(f"{USERDIR}/.ssh/{user}_SECRET.asc")
                writeFile(file, gpgkey, mode=0o600, user=user)
                if user == "root":
                    printSuccess(f"Imported gpg key from {file}") if not run(f"gpg --import {file}") else printWarning(f"Could not import gpg key from {file}")
                else:
                    printSuccess(f"Imported gpg key from {file}") if not run(f"runuser -u {user} -- gpg --import {file}") else printWarning(f"Could not import gpg key from {file}")
            # GNUPG CONFIG
            line()
            printDot("GNUPG CONFIG")
            gpgcfg = getData(f"[cyan]Default Key ID for {user}[/cyan] (ENTER to bypass): ")
            if not gpgcfg == False:
                tmpl = BASEDIR / "cfg/gnupg/gpg.conf"
                dest = USERDIR / ".gnupg/gpg.conf"
                data = {"signing_key": gpgcfg}
                if not writeTemplate(tmpl, dest, data, user=user):
                    printWarning(f"Could not write GNUPG2 config for user '{user}'")
                file = BASEDIR / "cfg/gnupg/gpg-agent.conf"
                dest = USERDIR / ".gnupg/gpg-agent.conf"
                if not copyFiles(file, dest, user=user):
                    printWarning(f"Could not copy gpg-agent.conf to {dest}")
            # GITCONFIG
            line()
            printDot("GIT CONFIG")
            git_user = getData(f"[cyan]Enter git username for {user}[/cyan] (ENTER to bypass): ")
            if not git_user == False:
                git_email = getData(f"[cyan]Enter git email for {user}[/cyan]: ")
                git_key = getData(f"[cyan]Enter signing key for {user}[/cyan]: ")
                tmpl = BASEDIR / "cfg/git/.gitconfig"
                dest = USERDIR / ".gitconfig"
                data = {"user_name": git_user, "user_email": git_email, "signing_key": git_key}
                if not writeTemplate(tmpl, dest, data, user=user):
                    printWarning(f"Could not write .gitconfig for {user}")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
        # ----------------------------------------------------------
        # REMOVE REDUNDANT USER ACCOUNTS
        # ----------------------------------------------------------
        filename = SETUPDIR / "cfg/usr-remove.cfg"
        if not filename.exists():
            raise FileNotFoundError(f"{filename} not found")
        users = getList(filename)
        removeUsers(users)
        line()
        getData("[yellow]MODULE COMPLETE :: Press [ENTER] to continue ...[/yellow] ")
    except Exception as e:
        logger.error(f"Failed executing script 'users': {e}", True, 1)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()

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
import sys

sys.path.append(".")

import banner

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
CHECKED: bool = config.getbool("setup", "checked", fallback=False)
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = Path(config.get("paths", "setup"))
DOTSDIR  = Path(config.get("paths", "sys")) / "dots"
LIBDIR   = Path(config.get("paths", "sys")) / "lib"
PKGDIR   = Path(config.get("paths", "scr")) / "pkg"
SVCDIR   = Path(config.get("paths", "opt")) / "svc"
# EXECUSR  = pwd.getpwuid(os.geteuid()).pw_name
# REALUSR  = getpass.getuser()
# SERVRIP  = getIP()
# USERSIP  = getUserIP()
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - USERS MODULE [/{yellow}]", style=yellow, align="left")
        line()
        global CHECKED
        if not CHECKED:
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # GATHER INFORMATION
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        users = []
        line()
        while True:
            data = getData(f"[{cyan}]Enter list of sudo users to setup[/{cyan}] (space delimited): ")
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
            clear()
            banner.execute()
            rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - USERS MODULE [/{yellow}]", style=yellow, align="left")
            line()
            printWhite(f"COPYING FILES FOR USER '{user}'")
            if not WARELIB.exists():
                WARELIB.mkdir(mode=0o755, parents=True, exist_ok=True)
            # Library Files
            line()
            printHead("Installing Library Files ...")
            copyFiles(LIBDIR, WARELIB, user=user)
            run(f"chown -R {user}:{user} {WARELIB}/*")
            run(f"chmod 0755 {WARELIB}/*")
            # Backup Dotfiles
            line()
            printHead("Backup Dotfiles ...")
            printSuccess("Backup '.bashrc'") if backup(USERDIR / ".bashrc") else printWarning("Failed to backup '.bashrc'")
            printSuccess("Backup '.profile'") if backup(USERDIR / ".profile") else printWarning("Failed to backup '.profile'")
            # Install Dotfiles
            line()
            printHead("Installing Dotfiles ...")
            copyFiles(DOTSDIR, USERDIR, user=user)
            run(f"chown -R {user}:{user} {USERDIR}/*")
            line()
            getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
        # ----------------------------------------------------------
        # CONFIGURE USERS
        # ----------------------------------------------------------
        for user in users:
            USERDIR = Path(f"/home/{user}") if user != "root" else Path("/root")
            clear()
            banner.execute()
            rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - USERS MODULE [/{yellow}]", style=yellow, align="left")
            line()
            printWhite(f"CONFIGURING USER '{user}'")
            # SUDO NOPASSWD
            if user != "root":
                line()
                printDot("SUDO NOPASSWD")
                line()
                nopasswd = getData(f"[{cyan}]Allow user {user} to use sudo without a password?[/{cyan}] (y/N): ").lower()
                if nopasswd == "y":
                    line()
                    data = f"{user} ALL=(ALL) NOPASSWD: ALL"
                    writeFile(Path(f"/etc/sudoers.d/{user}"), data)
            # ADD PGP KEY
            line()
            printDot("ADD PGP KEY")
            line()
            printMessage(f"[{cyan}]Paste SECRET key[/{cyan}] (Ctrl+D to end/bypass):")
            gpgkey = sys.stdin.read()
            if gpgkey:
                line()
                file = Path(f"{USERDIR}/.ssh/{user}_SECRET.asc")
                writeFile(file, gpgkey, mode=0o600, user=user)
                line()
                if user == "root":
                    printSuccess(f"\nImported gpg key from {file}") if run(f"gpg --import {file}").returncode == 0 else printWarning(f"\nCould not import gpg key from {file}")
                else:
                    printSuccess(f"\nImported gpg key from {file}") if run(f"runuser -u {user} -- gpg --import {file}").returncode == 0 else printWarning(f"\nCould not import gpg key from {file}")
            # GNUPG CONFIG
            line()
            printDot("GNUPG CONFIG")
            line()
            gpgcfg = getData(f"[{cyan}]Default Key ID for {user}[/{cyan}] (ENTER to bypass): ")
            if gpgcfg:
                line()
                tmpl = SETUPDIR / "cfg/gnupg/gpg.conf.jinja"
                dest = USERDIR / ".gnupg/gpg.conf"
                data = {"signing_key": gpgcfg}
                if not writeTemplate(tmpl, dest, data, user=user):
                    printWarning(f"Could not write GNUPG2 config for user '{user}'")
                line()
                file = SETUPDIR / "cfg/gnupg/gpg-agent.conf"
                dest = USERDIR / ".gnupg/gpg-agent.conf"
                if not copyFiles(file, dest, user=user):
                    printWarning(f"Could not copy gpg-agent.conf to {dest}")
            # GITCONFIG
            line()
            printDot("GIT CONFIG")
            line()
            git_user = getData(f"[{cyan}]Enter git username for {user}[/{cyan}] (ENTER to bypass): ")
            if git_user:
                line()
                git_email = getData(f"[{cyan}]Enter git email for {user}[/{cyan}]: ")
                line()
                git_key = getData(f"[{cyan}]Enter signing key for {user}[/{cyan}]: ")
                tmpl = SETUPDIR / "cfg/git/.gitconfig.jinja"
                dest = USERDIR / ".gitconfig"
                data = {"user_name": git_user, "user_email": git_email, "signing_key": git_key}
                if not writeTemplate(tmpl, dest, data, user=user):
                    printWarning(f"Could not write .gitconfig for {user}")
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
        line()
        # ----------------------------------------------------------
        # REMOVE REDUNDANT USER ACCOUNTS
        # ----------------------------------------------------------
        filename = SETUPDIR / "cfg/usr-remove.cfg"
        if not filename.exists():
            raise FileNotFoundError(f"{filename} not found")
        users = getList(filename)
        removeUsers(users)
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        logger.error(f"Failed executing script 'users': {e}", True, False, 1)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()

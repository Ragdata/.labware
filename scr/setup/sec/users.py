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

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = BASEDIR / "scr/setup"
REPOLIB  = BASEDIR / "sys/lib"
REPODOT  = BASEDIR / "sys/dots"
# REPOETC  = BASEDIR / "sys/etc"
# EXECUSR  = pwd.getpwuid(os.geteuid()).pw_name
# REALUSR  = getpass.getuser()
# SERVRIP  = getIP()
# USERSIP  = getUserIP()
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
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
                        errorExit(f"User '{user}' does not exist")
                break
            else:
                continue
        # ----------------------------------------------------------
        # COPY FILES TO USER DIR
        # ----------------------------------------------------------
        for user in users:
            USERDIR = Path(f"/home/{user}") if user != "root" else Path("/root")
            WAREDIR = USERDIR / ".labware"
            run("clear")
            rule(f"[yellow]── USERS MODULE [/yellow]", style="yellow", align="left")
            line()
            printWhite(f"COPYING FILES FOR USER '{user}'")
            # Library Files
            line()
            printHead("Installing Library Files ...")
            copyFiles(REPOLIB, WAREDIR / "lib", user=user)
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
            gpgkey = getData(f"[cyan]Paste SECRET key[/cyan] (ENTER to bypass): ")
            if not gpgkey == False:
                file = Path(f"{USERDIR}/.ssh/{user}_SECRET.asc")
                writeFile(file, gpgkey, mode=0o600, user=user)
                if user == "root":
                    printSuccess(f"Imported gpg key from {file}") if not run(f"gpg --import {file}") else printWarning(f"Could not import gpg key from {file}")
                else:
                    printSuccess(f"Imported gpg key from {file}") if not run(f"runuser -u {user} -- gpg --import {file}") else printWarning(f"Could not import gpg key from {file}")
            # GNUPG CONFIG
            line()
            printDot("GNUPG CONFIG")
            gpgcfg = getData(f"[cyan]Default Key for {user}[/cyan] (ENTER to bypass): ")
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
        outlog.logError(f"An error occurred in sec.users.py: {e}")
        raise e

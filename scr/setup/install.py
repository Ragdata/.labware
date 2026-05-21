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
import sys, getpass

sys.path.append('modules')

from modules.utils import *


#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR = Path(config.get("paths", "base"))
REPOLIB = BASEDIR / "sys" / "lib"
REPODOT = BASEDIR / "sys" / "dots"
REPOETC = BASEDIR / "sys" / "etc"
EXECUSR = pwd.getpwuid(os.geteuid()).pw_name
REALUSR = getpass.getuser()
SERVRIP = getIP()
print(f"{SERVRIP} - {REALUSR}")
exit(0)
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        checkRoot()
        checkPython()
        checkUbuntu()
        run("clear")
        ############################################################
        # Gather Information
        ############################################################
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
        ############################################################
        # COPY FILES TO USER DIR
        ############################################################
        for user in users:
            USERDIR = Path(f"/home/{user}") if user != "root" else Path("/root")
            WAREDIR = USERDIR / ".labware"
            run("clear")
            rule(f"[yellow]── Copying Files for User '{user}'[/yellow]", style="yellow", align="left")
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
            if user == EXECUSR:
                line()
                printHead("Installing Configs ...")
                copyFiles(REPOETC, WAREDIR / "etc", user=user)
            line()
            CONT = getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
        ############################################################
        # USER CONFIGURATION
        ############################################################
        for user in users:
            USERDIR = Path(f"/home/{user}") if user != "root" else Path("/root")
            WAREDIR = USERDIR / ".labware"
            run("clear")
            rule(f"[yellow]── Configuring User '{user}'[/yellow]")
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
                tmpl = BASEDIR / "cfg" / "gnupg" / "gpg.conf"
                dest = USERDIR / ".gnupg" / "gpg.conf"
                data = {"signing_key": gpgcfg}
                if not writeTemplate(tmpl, dest, data, user=user):
                    printWarning(f"Could not write GNUPG2 config for user '{user}'")
                file = BASEDIR / "cfg" / "gnupg" / "gpg-agent.conf"
                dest = USERDIR / ".gnupg" / "gpg-agent.conf"
                if not copyFiles(file, dest, user=user):
                    printWarning(f"Could not copy gpg-agent.conf to {dest}")
            # GITCONFIG
            line()
            printDot("GIT CONFIG")
            git_user = getData(f"[cyan]Enter git username for {user}[/cyan] (ENTER to bypass): ")
            if not git_user == False:
                git_email = getData(f"[cyan]Enter git email for {user}[/cyan]: ")
                git_key = getData(f"[cyan]Enter signing key for {user}[/cyan]: ")
                tmpl = BASEDIR / "cfg" / "git" / ".gitconfig"
                dest = USERDIR / ".gitconfig"
                data = {"user_name": git_user, "user_email": git_email, "signing_key": git_key}
                if not writeTemplate(tmpl, dest, data, user=user):
                    printWarning(f"Could not write .gitconfig for {user}")
            # if user == "root":
            #     line()
            #     printDot("INSTALL CUSTOM GIT COMMANDS")
        ############################################################
        # INSTALL BASIC TOOLS / UNINSTALL UNWANTED TOOLS VIA APT
        ############################################################
        run("clear")
        printHead("Installing Basic Tools ...")
        basic = BASEDIR / "src" / "setup" / "config" / "apt-basic.cfg"
        if not basic.exists():
            raise FileNotFoundError(f"File not found: '{basic}'")
        pkgs = getList(basic)
        installAPT(pkgs)
        line()
        printHead("Uninstalling Unwanted Tools ...")
        remove = BASEDIR / "src" / "setup" / "config" / "apt-remove.cfg"
        if not remove.exists():
            raise FileNotFoundError(f"File not found: '{remove}'")
        pkgs = getList(remove)
        removeAPT(pkgs)
        ############################################################
        # INSTALL SECURITY TOOLS VIA APT
        ############################################################
        line()
        printHead("Installing Security Tools ...")
        secure = BASEDIR / "src" / "setup" / "config" / "apt-secure.cfg"
        if not secure.exists():
            raise FileNotFoundError(f"File not found: '{secure}'")
        pkgs = getList(secure)
        installAPT(pkgs)
        ############################################################
        # CONFIGURE SECURITY TOOLS / HARDEN
        ############################################################

        ############################################################
        # INSTALL PRIMARY PACKAGES
        ############################################################
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Installer failed: {reason}")
        raise e

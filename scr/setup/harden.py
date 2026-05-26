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
import sys, runpy

sys.path.append('mod')

from mod.filesys import *


#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = BASEDIR / "scr/setup"
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        checkRoot()
        checkPython()
        checkUbuntu()
        run("clear")
        rule(f"[yellow]── CIS Benchmarking Level 1 Server Hardening[/yellow]")
        # ----------------------------------------------------------
        # Section 1.1 - Remove Unnecessary Filesystems
        # ----------------------------------------------------------
        line()
        printHead("Section 1.1 - Remove Unnecessary Filesystems")
        filesys = BASEDIR / "src/setup/cfg/apt-filesys.cfg"
        fs = getList(filesys)
        removeAPT(fs)
        run("systemctl mask autofs")
        # ----------------------------------------------------------
        # Section 1.2 - Secure Bootloader
        # ----------------------------------------------------------
        line()
        printHead("Section 1.2 - Secure Bootloader")
        chown(Path("/boot/grub/grub.cfg"), "root", "root")
        run("chmod og-rwx /boot/grub/grub.cfg")
        # ----------------------------------------------------------
        # Section 1.3 - Enable AppArmor
        # ----------------------------------------------------------
        line()
        printHead("Section 1.3 - Enable AppArmor")
        runpy.run_path("sec/apparmor.py")
        runpy.run_path("sec/kernel.py")
        # ----------------------------------------------------------
        # Section 1.4 - Coredumps
        # ----------------------------------------------------------
        line()
        printHead("Section 1.4 - Coredumps")
        runpy.run_path("sec/core.py")
        # ----------------------------------------------------------
        # Section 1.5 - Unattended Upgrades
        # ----------------------------------------------------------
        line()
        printHead("Section 1.5 - Unattended Upgrades")
        filepath = "/etc/apt/apt.conf.d/50unattended-upgrades"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        # ----------------------------------------------------------
        # Section 1.6 - Legal Banners
        # ----------------------------------------------------------
        line()
        printHead("Section 1.6 - Legal Banners")
        files = ["issue.net", "issue", "motd"]
        for file in files:
            filepath = f"/etc/{file}"
            template = SETUPDIR / filepath
            filedest = Path(filepath)
            copyFiles(template, filedest, True)
        run("chmod -x /etc/update-motd.d/*")
        # ----------------------------------------------------------
        # Section 1.8 - Detect Mounted Critical Paths
        # ----------------------------------------------------------
        line()
        printHead("Section 1.8 - Detect Mounted Critical Paths")
        MOUNTS = ["/home", "/tmp", "/var", "/var/log", "/var/log/audit", "/var/tmp", "/dev/shm"]
        for mnt in MOUNTS:
            if run(f"mount | grep -q 'on {mnt}'").returncode == 0:
                outlog.logSuccess(f"{mnt} is on a dedicated partition")
            else:
                outlog.logWarning(f"{mnt} is NOT on a dedicated partition")
        # ----------------------------------------------------------
        # Section 2.1 - Remove Unused Services
        # ----------------------------------------------------------
        line()
        printHead("Section 2.1 - Remove Unused Services")
        remove = BASEDIR / "src/setup/cfg/apt-remove.cfg"
        if not remove.exists():
            raise FileNotFoundError(f"File not found: '{remove}'")
        pkgs = getList(remove)
        removeAPT(pkgs)
        # ----------------------------------------------------------
        # Section 2.2 - Remove X Window System
        # ----------------------------------------------------------
        line()
        printHead("Section 2.2 - Remove X Window System")
        # ----------------------------------------------------------
        # Section 2.3 - Disable Avahi, AutoFS
        # ----------------------------------------------------------
        line()
        printHead("Section 2.3 - Disable Avahi, AutoFS")
        # ----------------------------------------------------------
        # Section 2.4 - NTP
        # ----------------------------------------------------------
        line()
        printHead("Section 2.4 - NTP")
        filepath = "/etc/systemd/timesyncd.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        run("systemctl restart systemd-timesyncd")
        run("systemctl enable systemd-timesyncd")
        # ----------------------------------------------------------
        # Section 2.5 - Secure 'cron' and 'at'
        # ----------------------------------------------------------
        line()
        printHead("Section 2.5 - Secure 'cron' and 'at'")
        run("chown root:root /etc/crontab /etc/cron.hourly /etc/cron.daily /etc/cron.weekly /etc/cron.monthly /etc/cron.d")
        run("chmod og-rwx /etc/crontab /etc/cron.hourly /etc/cron.daily /etc/cron.weekly /etc/cron.monthly /etc/cron.d")
        # ----------------------------------------------------------
        # Section 3 - Network Stack Hardening
        # ----------------------------------------------------------
        line()
        printHead("Section 3 - Network Stack Hardening")
        filepath = "/etc/sysctl.d/60-ipv6.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        run(f"sysctl -p {filepath}")
        filepath = "/etc/modprobe.d/disable.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        modules = ["dccp", "tipc", "rds", "sctp"]
        for mod in modules:
            run(f"modprobe -r {mod} 2>/dev/null")
        filepath = "/etc/sysctl.d/60-net.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        run(f"sysctl -p {filepath}")
        # ----------------------------------------------------------
        # Section 4 - FirewallD with Sane Defaults
        # ----------------------------------------------------------
        line()
        printHead("Section 4 - FirewallD with Sane Defaults")
        run("apt install -y firewalld")
        run("systemctl enable firewalld")
        run("systemctl start firewalld")
        ports = getList(BASEDIR / "scr" / "setup" / "cfg" / "app-firewalld.conf")
        for port in ports:
            if port[0].isdigit():
                command = f"firewall-cmd --permanent --zone=public --add-port={port}/tcp"
            else:
                command = f"firewall-cmd --permanent --zone=public --add-service={port}"
            run(command)
        run("firewall-cmd --reload")
        # ----------------------------------------------------------
        # Section 5.1 - SSH Hardening
        # ----------------------------------------------------------
        line()
        printHead("Section 5.1 - SSH Hardening")
        filepath = "/etc/ssh/sshd_config"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        labusers = getData("[cyan]Restrict SSH logins to the following users[/cyan] (ENTER for none): ")
        address  = getData("[cyan]Internal IP granted root access[/cyan] (ENTER for none): ")
        data = {"labuser": labusers, "internal_address": address}
        if not writeTemplate(template, filedest, data):
            outlog.logError(f"Could not write template to {filedest}", 1)
        run("systemctl enable ssh")
        run("systemctl restart ssh")
        # ----------------------------------------------------------
        # Section 5.2 - Secure SUDO
        # ----------------------------------------------------------
        line()
        printHead("Section 5.2 - Secure SUDO")
        filepath = "/etc/sudoers.d/01_base"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        chmod(filedest, 0o440)
        if run(f"visudo -c -f {filedest}").returncode != 0:
            outlog.logError(f"SUDO config failed validation", 1)
        # ----------------------------------------------------------
        # Section 5.4 - Password Policy
        # ----------------------------------------------------------
        line()
        printHead("Section 5.4 - Password Policy")
        # Set login parameters
        filepath = "/etc/login.defs"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        # Set inactive account lock to 30 days
        run(f"useradd -D -f 30")
        # Set shell timeout to 30 secs
        filepath = "/etc/profile.d/timeout.sh"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        run(f"chmod +x {filedest}")
        # Lock root account
        run("passwd -l root")
        # Set bash defaults
        filepath = "/etc/bash.bashrc"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        # Set default root umask in .profile
        dotfile = Path.home() / ".bash_profile"
        if not dotfile.exists():
            dotfile = Path.home() / ".profile"
        if not dotfile.exists():
            raise FileNotFoundError(f"File not found '{dotfile}'")
        if not findFileString(dotfile, "umask 027"):
            with open(dotfile, "a") as f:
                f.write("umask 027")
        # Set default root umask in .bashrc
        dotfile = Path.home() / ".bashrc"
        if not dotfile.exists():
            raise FileNotFoundError(f"File not found '{dotfile}'")
        if not findFileString(dotfile, "umask 027"):
            with open(dotfile, "a") as f:
                f.write("umask 027")
        # ----------------------------------------------------------
        # Section 5.5 - Account Auditing
        # ----------------------------------------------------------
        line()
        printHead("Section 5.5 - Account Auditing")
        # 5.5.2 Audit legacy NIS entries
        if run('grep "^+:" /etc/passwd | tee /var/log/legacy_passwd_entries.log').returncode != 0:
            outlog.logWarning("Encountered problem auditing legacy NIS files")
        # 5.5.3 Audit duplicate UID 0 accounts
        if run('awk -F: \'($3 == 0) { print $1 }\' /etc/passwd | grep -v "^root$" | tee /var/log/uid0_accounts.log').returncode != 0:
            outlog.logWarning("Encountered problem auditing duplicate UID 0 accounts (UID)")
        # 5.5.4 Audit duplicate UID 0 accounts
        if run('awk -F: \'$3=="0"{print $1":"$3}\' /etc/group | tee /var/log/gid0_accounts.log').returncode != 0:
            outlog.logWarning("Encountered problem auditing duplicate GID 0 accounts (GID)")
        # # 5.5.5 Audit duplicate UID 0 accounts
        # if run('awk -F: \'($3 == 0) { print $1 }\' /etc/passwd | grep -v "^root$" | tee /var/log/uid0_accounts.log').returncode != 0:
        #     outlog.logWarning("Encountered problem auditing duplicate UID 0 accounts (UID)")
        # 5.5.6 Lock empty password accounts
        if run('awk -F: \'($2 == "") { print $1 }\' /etc/shadow | xargs -r -n 1 passwd -l').returncode != 0:
            outlog.logWarning("Encountered problem locking empty password accounts")
        # ----------------------------------------------------------
        # Section 6.1 - 'auditd' Logging & Audit Rules
        # ----------------------------------------------------------
        line()
        printHead("Section 6.1 - 'auditd' Logging & Audit Rules")
        runpy.run_path("sec/auditd.py")
        # ----------------------------------------------------------
        # Section 6.2 - Secure 'rsyslog'
        # ----------------------------------------------------------
        line()
        printHead("Section 6.2 - Secure 'rsyslog'")
        runpy.run_path("sec/rsyslog.py")
        # ----------------------------------------------------------
        # Section 6.3 - Log Rotation & JournalD
        # ----------------------------------------------------------
        line()
        printHead("Section 6.3 - Log Rotation & JournalD")
        filepath = "/etc/logrotate.d/sudo"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        filepath = "/etc/systemd/journald.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        run("systemctl restart systemd-journald")
        # ----------------------------------------------------------
        # Section 6.4 - Enable 'acct' & Process Tracking
        # ----------------------------------------------------------
        line()
        printHead("Section 6.4 - Enable 'acct' & Process Tracking")
        runpy.run_path("sec/acct.py")
        # ----------------------------------------------------------
        # Section 6.5 - Secure Password Files
        # ----------------------------------------------------------
        line()
        printHead("Section 6.5 - Secure Password Files")
        chmod(Path("/etc/passwd"), 0o644)
        chown(Path("/etc/passwd"), "root", "root")
        chmod(Path("/etc/shadow"), 0o000)
        chown(Path("/etc/shadow"), "root", "shadow")
        chmod(Path("/etc/group"), 0o644)
        chown(Path("/etc/group"), "root", "root")
        chmod(Path("/etc/gshadow"), 0o000)
        chown(Path("/etc/gshadow"), "root", "shadow")
        chmod(Path("/etc/passwd-"), 0o600)
        chown(Path("/etc/passwd-"), "root", "root")
        chmod(Path("/etc/shadow-"), 0o600)
        chown(Path("/etc/shadow-"), "root", "shadow")
        chmod(Path("/etc/group-"), 0o600)
        chown(Path("/etc/group-"), "root", "root")
        chmod(Path("/etc/gshadow-"), 0o600)
        chown(Path("/etc/gshadow-"), "root", "shadow")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"System hardening failed: {reason}")
        raise e

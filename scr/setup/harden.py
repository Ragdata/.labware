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
SERVRIP  = getIP()
USERSIP  = getUserIP()
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
        files = ["/etc/apt/apt.conf.d/50unattended-upgrades", "/etc/apt/apt.conf.d/98-hardening"]
        copyRepoFiles(SETUPDIR, files, True)
        # ----------------------------------------------------------
        # Section 1.6 - Legal Banners
        # ----------------------------------------------------------
        line()
        printHead("Section 1.6 - Legal Banners")
        files = ["/etc/issue.net", "/etc/issue", "/etc/motd"]
        copyRepoFiles(SETUPDIR, files, True)
        run("chmod -x /etc/update-motd.d/*")
        run("systemctl stop motd-news.timer")
        run("systemctl mask motd-news.timer")
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
        copyRepoFile(SETUPDIR, "/etc/systemd/timesync.conf", True)
        run("systemctl restart systemd-timesyncd")
        run("systemctl enable systemd-timesyncd")
        # ----------------------------------------------------------
        # Section 2.5 - Secure 'cron' and 'at'
        # ----------------------------------------------------------
        line()
        printHead("Section 2.5 - Secure 'cron' and 'at'")
        files = ["/etc/cron.allow", "/etc/at.allow"]
        copyRepoFiles(SETUPDIR, files, True)
        run("chown root:root /etc/cron*")
        run("chmod og-rwx /etc/cron*")
        run("chown root:root /etc/at*")
        run("chmod og-rwx /etc/at*")
        run("systemctl mask atd.service")
        run("systemctl stop atd.service")
        run("systemctl daemon-reload")
        # ----------------------------------------------------------
        # Section 3 - Network Stack Hardening
        # ----------------------------------------------------------
        line()
        printHead("Section 3 - Network Stack Hardening")
        files = ["/etc/sysctl.d/60-ipv6.conf", "/etc/sysctl.d/60-net.conf", "/etc/modprobe.d/disable.conf", "/etc/systemd/logind.conf", "/etc/hosts.allow", "/etc/hosts.deny"]
        copyRepoFiles(SETUPDIR, files, True)
        run(f"sysctl -p /etc/sysctl.d/60-ipv6.conf")
        run(f"sysctl -p /etc/sysctl.d/60-net.conf")
        run("systemctl restart systemd-sysctl")
        modules = ["dccp", "tipc", "rds", "sctp"]
        for mod in modules:
            run(f"modprobe -r {mod} 2>/dev/null")
        # ----------------------------------------------------------
        # Section 4 - FirewallD with Sane Defaults
        # ----------------------------------------------------------
        line()
        printHead("Section 4 - FirewallD with Sane Defaults")
        run("apt install -y firewalld")
        run("systemctl enable firewalld")
        run("systemctl start firewalld")
        ports = getList(BASEDIR / "scr/setup/cfg/app-firewalld.conf")
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
        data = {"labusers": labusers, "internal_address": address}
        if not writeTemplate(template, filedest, data, 0o600, "root", "root"):
            outlog.logError(f"Could not write template to {filedest}", 1)
        filepath = "/etc/security/access.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        if not writeTemplate(template, filedest, data):
            outlog.logError(f"Could not write template to {filedest}", 1)
        run("systemctl enable ssh")
        run("systemctl restart ssh")
        run("systemctl mask debug-shell.service")
        run("systemctl stop debug-shell.service")
        run("systemctl daemon-reload")
        # ----------------------------------------------------------
        # Section 5.2 - Secure SUDO
        # ----------------------------------------------------------
        line()
        printHead("Section 5.2 - Secure SUDO")
        copyRepoFile(SETUPDIR, "/etc/sudoers.d/01_base", True, mode=0o440)
        copyRepoFile(SETUPDIR, "/etc/pam.d/su", True)
        if run(f"visudo -c -f {filedest}").returncode != 0:
            outlog.logError(f"SUDO config failed validation", 1)
        # ----------------------------------------------------------
        # Section 5.4 - Password Policy
        # ----------------------------------------------------------
        line()
        printHead("Section 5.4 - Password Policy")
        files = ["/etc/login.defs", "/etc/profile.d/timeout.sh", "/etc/bash.bashrc", "/usr/share/dict/passwords"]
        copyRepoFiles(SETUPDIR, files, True)
        run(f"useradd -D -f 30")
        run(f"chmod +x /etc/profile.d/timeout.sh")
        run("passwd -l root")
        run(f"grep -v '^$' {SETUPDIR}usr/share/dict/passwords | strings > /usr/share/dict/passwords_text")
        run("update-cracklib")
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
        files = ["/etc/logrotate.conf", "/etc/logrotate.d/sudo", "/etc/systemd/journald.conf"]
        copyRepoFiles(SETUPDIR, files, True)
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
        data = {
            "/etc/passwd":   [0o644, "root", "root"],
            "/etc/shadow":   [0o000, "root", "shadow"],
            "/etc/group":    [0o644, "root", "root"],
            "/etc/gshadow":  [0o000, "root", "shadow"],
            "/etc/passwd-":  [0o600, "root", "root"],
            "/etc/shadow-":  [0o600, "root", "shadow"],
            "/etc/group-":   [0o600, "root", "root"],
            "/etc/gshadow-": [0o600, "root", "shadow"]
        }
        perms(data)
        # ----------------------------------------------------------
        # EXTRAS
        # ----------------------------------------------------------
        line()
        printHead("EXTRAS")
        # Enable 'sysstat'
        copyRepoFile(SETUPDIR, "/etc/default/sysstat", True)
        run("systemctl enable sysstat")
        # Install 'psad'
        runpy.run_path("sec/psad.py")
        # Install 'usbguard'
        runpy.run_path("sec/usbguard.py")
        # Install 'rkhunter'
        runpy.run_path("sec/rkhunter.py")
        # Install 'aide'
        runpy.run_path("sec/aide.py")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"System hardening failed: {reason}")
        raise e

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

sys.path.append("../mod")

from mod.filesys import *

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
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
        # 5.5.6 Lock empty password accounts
        if run('awk -F: \'($2 == "") { print $1 }\' /etc/shadow | xargs -r -n 1 passwd -l').returncode != 0:
            outlog.logWarning("Encountered problem locking empty password accounts")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        outlog.logError(f"An error occurred: {e}")
        raise e

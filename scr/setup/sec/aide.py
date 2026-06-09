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
CHECKED: bool = config.getboolean("setup", "checked", fallback=False)
SETUPDIR = Path(config.get("paths", "setup"))
#-------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------
def configMetrics() -> bool:
    line()
    printHead("Metrics Configuration")
    line()
    metrics = getData(f"[{cyan}]Enable Prometheus metrics export?[/{cyan}] (Y/n): ")
    if metrics.lower() != 'n':
        return True
    return False

def configWorkers() -> int:
    cores = run("nproc").stdout.strip()
    workers = int(cores) // 2
    line()
    printHead("Worker Configuration")
    line()
    printMessage(f"CPU Cores detected: {cores}")
    printMessage(f"Recommended workers: {workers}")
    line()
    response = getData(f"[{cyan}]Set how many workers?[/{cyan}] (default: {workers}): ")
    if response:
        workers = int(response)
    return workers

def configTelegram() -> dict[str, str] | None:
    line()
    printHead("Telegram Bot Configuration")
    bot_id = getData(f"[{cyan}]Enter Telegram Bot ID[/{cyan}] (ENTER to skip): ")
    if bot_id:
        bot_token = getData(f"[{cyan}]Enter Telegram Bot Token[/{cyan}]: ")
        return {"BOT_ID": bot_id, "BOT_TOKEN": bot_token}
    return None

def getDropIns() -> list:
    dropins = [
        "/etc/aide/aide.conf.d/15-monitoring-rules.conf",
        "/etc/aide/aide.conf.d/16-backup-rules.conf",
        "/etc/aide/aide.conf.d/40-systemd-rules.conf",
        "/etc/aide/aide.conf.d/50-network-rules.conf"
    ]
    if run("command -v docker >/dev/null 2>&1").returncode == 0:
        line()
        printWarning("Docker detected")
        dropDocker = getData(f"[{cyan}]Enable Docker drop-ins?[/{cyan}] (Y/n): ")
        if dropDocker.lower() != 'n':
            dropins.append("/etc/aide/aide.conf.d/10-docker-rules.conf")
    if run("command -v psql >/dev/null 2>&1").returncode == 0:
        line()
        printWarning("PostgreSQL detected")
        dropPostgres = getData(f"[{cyan}]Enable PostgreSQL drop-ins?[/{cyan}] (Y/n): ")
        if dropPostgres.lower() != 'n':
            dropins.append("/etc/aide/aide.conf.d/20-postgres-rules.conf")
    if Path("/var/www/nexttcloud").exists() or Path("/var/www/html/nextcloud").exists():
        line()
        printWarning("Nextcloud detected")
        dropNextcloud = getData(f"[{cyan}]Enable Nextcloud drop-ins?[/{cyan}] (Y/n): ")
        if dropNextcloud.lower() != 'n':
            dropins.append("/etc/aide/aide.conf.d/30-nextcloud-rules.conf")
    return dropins

def install():
    """
    Install AIDE (Advanced Intrusion Detection Environment) on the system.
    """
    pkgs = ["aide", "aide-common"]
    installAPT(pkgs)

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - EXTRAS [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # EXTRAS - Advanced Intrusion Detection Environment ('aide')
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Install Advanced Intrusion Detection Environment ('aide')")
        line()
        ENABLE_METRICS = configMetrics()
        install()
        copyRepoFiles(SETUPDIR, getDropIns())
        # ── Simple Config Files ───────────────────────────────────
        files = ["/etc/systemd/system/aide-check.service", "/etc/systemd/system/aide-check.timer",
                 "/etc/systemd/system/aide-update.timer", "/etc/default/aide"]
        copyRepoFiles(SETUPDIR, files, True)
        # ── /etc/aide/aide.conf ───────────────────────────────────
        tmpl = SETUPDIR / "etc" / "aide" / "aide.conf"
        dest = Path("/etc/aide/aide.conf")
        data = {"NUM_WORKERS": configWorkers()}
        if not writeTemplate(tmpl, dest, data):
            logger.error(f"Could not write template to {dest}", True, 1)
        # ── /etc/systemd/system/aide-update.service ───────────────
        tmpl = SETUPDIR / "etc" / "systemd" / "system" / "aide-update.service"
        dest = Path("/etc/systemd/system/aide-update.service")
        data = {
            "SCRIPT_PATH": "/usr/local/bin",
            "METRICS_SCRIPT": "/usr/local/bin",
            "TIMEOUT": "90",
            "LOG_DIR": "/var/log/aide",
            "TIMEOUT_SECONDS": "5400"
        }
        if not writeTemplate(tmpl, dest, data):
            logger.error(f"Could not write template to {dest}", True, 1)
        # ── /etc/aide/telegram.conf ───────────────────────────────
        data = configTelegram()
        if data is not None:
            tmpl = SETUPDIR / "etc" / "aide" / "telegram.conf"
            dest = Path("/etc/aide/telegram.conf")
            if not writeTemplate(tmpl, dest, data):
                logger.error(f"Could not write template to {dest}", True, 1)
            # ── /etc/systemd/system/aide-alert.service ────────────
            tmpl = SETUPDIR / "etc" / "systemd" / "system" / "aide-alert.service"
            dest = Path("/etc/systemd/system/aide-alert.service")
            data = {
                "BASH_TOOLKIT_PATH": "/usr/local/lib/bash-production-toolkit",
                "BOT_ID": data["BOT_ID"],
                "BOT_TOKEN": data["BOT_TOKEN"],
                "RATE_LIMIT_SECONDS": "10",
                "SCRIPT_PATH": "/usr/local/bin",
                "TELEGRAM_PREFIX": "[AIDE ALERT] "
            }
            if not writeTemplate(tmpl, dest, data):
                logger.error(f"Could not write template to {dest}", True, 1)
        # copyRepoFile(SETUPDIR, "/etc/aide/aide.conf", True)




        # run("aideinit --yes")
        # db = Path("/var/lib/aide/aide.db.new")
        # if db.exists():
        #     mv = Path("/var/lib/aide/aide.db")
        #     db.replace(mv)
        # copyConfigs()
        # run("systemctl enable aide-check.timer")
        # run("systemctl start aide-check.timer")
        # run("systemctl daemon-reload")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        logger.error(f"Failed to install 'aide': {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()

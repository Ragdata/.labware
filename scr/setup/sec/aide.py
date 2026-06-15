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
SETUPDIR = Path(config.get("paths", "setup"))
dropins: list = [
    "/etc/aide/aide.conf.d/15-monitoring-rules.conf",
    "/etc/aide/aide.conf.d/16-backup-rules.conf",
    "/etc/aide/aide.conf.d/40-systemd-rules.conf",
    "/etc/aide/aide.conf.d/50-network-rules.conf"
]
#-------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------
def configMetrics() -> bool:
    printDot("Metrics Configuration")
    line()
    metrics = getData(f"[{cyan}]Enable Prometheus metrics export?[/{cyan}] (Y/n): ")
    if metrics.lower() != 'n':
        return True
    return False

def configWorkers() -> int:
    cores = run("nproc").stdout.strip()
    workers = int(cores) // 2
    printDot("Worker Configuration")
    line()
    printMessage(f"CPU Cores detected: {cores}")
    printMessage(f"Recommended workers: {workers}")
    line()
    response = getData(f"[{cyan}]Set how many workers?[/{cyan}] (default: {workers}): ")
    if response:
        workers = int(response)
    return workers

def configTelegram() -> dict[str, str] | None:
    printDot("Telegram Bot Configuration")
    line()
    bot_id = getData(f"[{cyan}]Enter Telegram Bot ID[/{cyan}] (ENTER to skip): ")
    if bot_id:
        bot_token = getData(f"[{cyan}]Enter Telegram Bot Token[/{cyan}]: ")
        return {"BOT_ID": bot_id, "BOT_TOKEN": bot_token}
    return None

def deployMetrics() -> None:
    if run("systemctl status node_exporter > /dev/null 2>&1").returncode != 0:
        logger.warning("Node Exporter is not installed. Skipping metrics deployment.", True)
        return
    printDot("Installing 'node_exporter'")
    line()
    url = "https://github.com/prometheus/node_exporter/releases/latest"
    response = requests.get(url).json()
    _version = response["tag_name"].replace("v", "")
    node_exporter_url = f"https://github.com/prometheus/node_exporter/releases/download/{response['tag_name']}/node_exporter-{_version}.linux-amd64.tar.gz"
    downloadFile(node_exporter_url, "/tmp/node_exporter.tar.gz")
    run("tar -xzf /tmp/node_exporter.tar.gz -C /tmp")
    run("mv /tmp/node_exporter-* /opt/node_exporter")
    run("rm -rf /tmp/node_exporter.tar.gz /tmp/node_exporter-*")
    run("ln -s /opt/node_exporter/node_exporter /usr/local/bin/node_exporter")
    line()
    printDot("Enabling 'node_exporter' service")
    line()
    run("systemctl daemon-reload")
    run("systemctl enable node_exporter")
    run("systemctl start node_exporter")
    line()
    printDot("Setting up AIDE metrics exporter")
    collect = Path("/var/lib/node_exporter/textfile_collector")
    if not collect.exists():
        collect.mkdir(mode=0o755, parents=True, exist_ok=True)
    run("/usr/local/bin/aide-metrics-exporter.sh")

def getDropIns() -> None:
    global dropins
    printDot("Detecting installed applications")
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

def install() -> None:
    """
    Install AIDE (Advanced Intrusion Detection Environment) on the system.
    """
    printDot("Installing AIDE")
    line()
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
        # ── Install AIDE ──────────────────────────────────────────
        install()
        copyRepoFiles(SETUPDIR, dropins)
        getDropIns()
        if configMetrics():
            deployMetrics()
        # ── /etc/aide/aide.conf ───────────────────────────────────
        tmpl = SETUPDIR / "etc/aide/aide.conf"
        dest = Path("/etc/aide/aide.conf")
        data = {"NUM_WORKERS": configWorkers()}
        if not writeTemplate(tmpl, dest, data):
            logger.error(f"Could not write template to {dest}", True, False, 1)
        # ── /etc/aide/telegram.conf ───────────────────────────────
        tele = configTelegram()
        if tele is not None:
            tmpl = SETUPDIR / "etc/aide/telegram.conf"
            dest = Path("/etc/aide/telegram.conf")
            if not writeTemplate(tmpl, dest, tele):
                logger.error(f"Could not write template to {dest}", True, False, 1)
            # ── /etc/systemd/system/aide-alert.service ────────────
            tmpl = SETUPDIR / "etc/systemd/system/aide-alert.service.jinja"
            dest = Path("/etc/systemd/system/aide-alert.service")
            data = {
                "BASH_TOOLKIT_PATH": "/usr/local/lib/bash-production-toolkit",
                "BOT_ID": tele["BOT_ID"],
                "BOT_TOKEN": tele["BOT_TOKEN"],
                "RATE_LIMIT_SECONDS": "10",
                "SCRIPT_PATH": "/usr/local/bin",
                "TELEGRAM_PREFIX": "[AIDE ALERT] "
            }
            if not writeTemplate(tmpl, dest, data):
                logger.error(f"Could not write template to {dest}", True, False, 1)
        # ── Systemd Config Files ──────────────────────────────────
        files = ["/etc/systemd/system/aide-check.service", "/etc/systemd/system/aide-check.timer",
                 "/etc/systemd/system/aide-update.timer", "/etc/default/aide", "/etc/tmpfiles.d/aide-common.conf"]
        copyRepoFiles(SETUPDIR, files, True)
        # Activate AIDE tmpfiles.d configuration
        run("systemd-tmpfiles --create /etc/tmpfiles.d/aide-common.conf")
        # ── /etc/systemd/system/aide-update.service ───────────────
        tmpl = SETUPDIR / "etc/systemd/system/aide-update.service.jinja"
        dest = Path("/etc/systemd/system/aide-update.service")
        data = {
            "SCRIPT_PATH": "/usr/local/bin",
            "METRICS_SCRIPT": "/usr/local/bin",
            "TIMEOUT": "240",
            "LOG_DIR": "/var/log/aide",
            "TIMEOUT_SECONDS": "5400"
        }
        if not writeTemplate(tmpl, dest, data):
            logger.error(f"Could not write template to {dest}", True, False, 1)
        # ── Enable and Start Services ─────────────────────────────
        run("systemctl daemon-reload")
        run("systemctl enable aide-check.timer")
        run("systemctl enable aide-update.timer")
        run("systemctl start aide-check.timer")
        run("systemctl start aide-update.timer")
        if tele is not None:
            run("systemctl enable aide-alert.service")
            run("systemctl start aide-alert.service")
        # ── Initial AIDE Database Creation ────────────────────────
        if run("aideinit").returncode != 0:
            logger.error(f"Failed to initialise AIDE database", True, False, 1)
        new = Path("/var/lib/aide/aide.db.new")
        if not new.exists():
            logger.error(f"Failed to create AIDE database", True, False, 1)
        new.rename("/var/lib/aide/aide.db")
        # ── Set non-root permissions ──────────────────────────────
        run("groupadd --system _aide 2>/dev/null || true")
        mon_user = getData(f"[{cyan}]Enter the username of the user to monitor AIDE changes:[/{cyan}] ")
        if mon_user:
            run(f"usermod -aG _aide {mon_user}")
        #run("chown -R root:_aide /var/lib/aide")
        files = {"/var/lib/aide/aide.db": ["0o640", "root", "_aide"], "/var/lib/aide": ["0o750", "root", "_aide"]}
        perms(files)
        # ── Set immutable flags ───────────────────────────────────
        run("chattr +i /usr/bin/aide")
        run("chattr +i /etc/aide/aide.conf")
        # ----------------------------------------------------------
        # REPORT
        # ----------------------------------------------------------
        now = datetime.now()
        tmpl = SETUPDIR / "sec/reports/aide.jinja"
        dest = Path.home() / f".labware/reports/aide.{now.strftime('%Y%m%d%H%M%S')}.md"
        title1 = printYellow("─────────────────────────────────────────────────────────────────────────────", save=True)
        title2 = printYellow("AIDE DEPLOYMENT COMPLETE", save=True)
        title3 = printYellow("─────────────────────────────────────────────────────────────────────────────", save=True)
        data = {
            "divider": f"{title1}",
            "title": f"{title1}\n{title2}\n{title3}",
            "version": run("aide --version").stdout.strip(),
            "entry_count": run("aide --check 2>&1 | grep \"^Total number of entries:\" | awk '{print $5}'").stdout.strip(),
            "db_size": run("du -sh /var/lib/aide/aide.db | awk '{print $1}'").stdout.strip(),
            "group_valid": printSuccess("Group '_aide' verified", save=True) if run("getent group _aide").returncode == 0 else logger.error("Group '_aide' failed verification", True, True),
            "tmpfile_override": printSuccess("AIDE tmpfiles.d override verified", save=True) if run("ls -ld /var/lib/aide/ | awk '{print $1, $3, $4}'").stdout.strip() == "drwxr-x--- _aide _aide" else logger.error("AIDE tmpfiles.d override failed verification", True, True),
            "main_config": printSuccess("Main config syntax verified", save=True) if run("aide --config=/etc/aide/aide.conf").returncode == 0 else logger.error("Main config syntax invalid", True, True),
            "mon_user_test": printSuccess("Monitoring user verified", save=True) if run(f"sudo -u {mon_user} test -r /var/lib/aide/aide.db").returncode == 0 else logger.error("Monitoring user failed verification", True, True),
            "crit_perms": run("ls -ld /var/lib/aide").stdout.strip(),
            "crit_perms_db": run("ls -l /var/lib/aide/aide.db").stdout.strip(),
            "immutable_flag_test": printSuccess("Immutable flags set", save=True) if run("lsattr /usr/bin/aide").stdout.strip().endswith("+i") and run("lsattr /etc/aide/aide.conf").stdout.strip().endswith("+i") else logger.error("Immutable flags not set", True, True),
            "update_script_test": run("/usr/local/bin/update-aide-db.sh --check").stdout.strip(),
            "check_timer_status": run("systemctl status aide-check.timer").stdout.strip(),
            "check_timer_list": run("systemctl list-timers aide-check.timer").stdout.strip(),
            "update_timer_status": run("systemctl status aide-update.timer").stdout.strip(),
            "update_timer_list": run("systemctl list-timers aide-update.timer").stdout.strip(),
        }
        if not writeTemplate(tmpl, dest, data):
            logger.error(f"Could not write template to {dest}", True, False, 1)
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        logger.error(f"Failed to install 'aide': {e}", True, False, 1)
        raise

def report():
    try:
        pass
    except Exception as e:
        logger.error(f"Failed to report 'aide': {e}", True, False, 1)
        raise
# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()

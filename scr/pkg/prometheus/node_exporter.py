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

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        logger.info(f"Executing {__file__}")
        clear()
        rule(f"[{yellow}]── Install Node Exporter [/{yellow}]", style=yellow, align="left")
        line()
        # ----------------------------------------------------------
        # INSTALL NODE EXPORTER
        # ----------------------------------------------------------
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
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()

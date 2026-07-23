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

sys.path.append(".")

import banner

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
CHECKED: bool = config.getbool("setup", "checked", fallback=False)
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── PACKAGES MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # INSTALL PACKAGES
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Installing Primary Packages ...")
        line()
        webmin = getData(f"[{cyan}]Install Webmin?[/{cyan}] (Y/n): ").lower()
        if webmin != 'n':
            path = Path(config.get("paths", "pkg")) / "webmin.py"
            if not path.exists():
                logger.error(f"Webmin package script not found at: {path}", True, False, 1)
            runpy.run_path(str(path))
        else:
            virtualmin = getData(f"[{cyan}]Install Virtualmin[/{cyan}] (Y/n): ").lower()
            if virtualmin != 'n':
                path = Path(config.get("paths", "pkg")) / "virtualmin.py"
                if not path.exists():
                    logger.error(f"Virtualmin package script not found at: {path}", True, False, 1)
                runpy.run_path(str(path))
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
        line()
        docker = getData(f"[{cyan}]Install Docker[/{cyan}] (Y/n): ").lower()
        if docker != 'n':
            path = Path(config.get("paths", "pkg")) / "docker.py"
            if not path.exists():
                logger.error(f"Docker package script not found at: {path}", True, False, 1)
            runpy.run_path(str(path))
            lazydocker = getData(f"[{cyan}]Install LazyDocker[/{cyan}] (Y/n): ").lower()
            if lazydocker != 'n':
                path = Path(config.get("paths", "pkg")) / "lazydocker.py"
                if not path.exists():
                    logger.error(f"LazyDocker package script not found at: {path}", True, False, 1)
                runpy.run_path(str(path))
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

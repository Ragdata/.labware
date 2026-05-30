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
import tempfile, argparse, requests

from pathlib import Path
from urllib.parse import urlparse

from labware.config import *

BASEDIR = Path(__file__).resolve().parent.parent.parent

config: Config = Config(config_file=BASEDIR / "scr" / "lab" / "cfg" / ".labware.cfg")

config.set("paths", "base", str(BASEDIR))

from labware.logger import *

logger: Logger = get_logger("password")

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
DEFAULT_FILE = BASEDIR / config.get("src", "lab") / "cfg" / "pwd-sources.cfg"
LAB_SHARE = Path(config.get("paths", "share"))
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", dest="file", nargs="?", default=str(DEFAULT_FILE), help="Path to the password sources configuration file")

        args = parser.parse_args()

        file = Path(args.file)

        if not file.exists():
            raise FileNotFoundError(f"File not found: {file}")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

        files = []

        with open(file, "r") as f:
            for url in f:
                url = url.strip()
                if url:
                    logger.default(f"Processing URL: {url}", True)
                    purl = Path(urlparse(url).path)
                    filename = purl.name
                    filepath = Path(tmpdir) / filename
                    with requests.get(url, stream=True) as r:
                        r.raise_for_status()
                        with open(filepath, "wb") as w:
                            for chunk in r.iter_content(chunk_size=8192):
                                w.write(chunk)
                    files.append(str(filepath))
                    logger.success(f"Downloaded to {filepath}", True)

        logger.default(f"Merging Files ...")

        if not mergeFiles(files, str(LAB_SHARE / "passwords.txt")):
            logger.error(f"Failed to merge password files", True, 1)

        logger.success(f"Password list generated at {str(LAB_SHARE / 'passwords.txt')}", True)

    except Exception as e:
        logger.error(f"Script encountered an error: {e}", True)
        raise

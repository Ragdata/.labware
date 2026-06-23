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
import tempfile, argparse, sys

from pathlib import Path

sys.path.append(".")

from urllib.parse import urlparse

from labware.logger import *

logger: Logger = get_logger("password")

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR = Path(config.get("paths", "base"))
LABDIR = Path(config.get("paths", "lab"))
DEFAULT_FILE = LABDIR / "cfg" / "pwd-sources.cfg"
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute(filepath: Path = DEFAULT_FILE):
    try:

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

        files = []

        with open(filepath, "r") as f:
            for url in f:
                url = url.strip()
                if url:
                    logger.default(f"Processing URL: {url}", True)
                    purl = Path(urlparse(url).path)
                    filename = purl.name
                    filetemp = Path(tmpdir) / filename
                    with requests.get(url, stream=True) as r:
                        r.raise_for_status()
                        with open(filetemp, "wb") as w:
                            for chunk in r.iter_content(chunk_size=8192):
                                w.write(chunk)
                    files.append(str(filetemp))
                    logger.success(f"Downloaded to {filetemp}", True)

        logger.default(f"Merging Files ...")

        if not mergeFiles(files, str(LABDIR / "passwords.txt")):
            logger.error(f"Failed to merge password files", True, False, 1)

        logger.success(f"Password list generated at {str(LABDIR / 'passwords.txt')}", True)

    except Exception as e:
        logger.error(f"Script encountered an error: {e}", True)
        raise


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file", nargs="?", default=str(DEFAULT_FILE),
                        help="Path to the password sources configuration file")

    args = parser.parse_args()

    file = Path(args.file)

    execute(file)

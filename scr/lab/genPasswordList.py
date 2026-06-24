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
import tempfile
import argparse
import sys

sys.path.append(".")

from urllib import request
from urllib.parse import urlparse

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR = Path(config.get("paths", "base"))
LABDIR = Path(config.get("paths", "lab"))
DEFAULT_FILE = LABDIR / "cfg" / "pwd-sources.cfg"
DEFAULT_DEST = Path("/usr/share/dict/passwords")
TMPDIR = tempfile.mkdtemp()
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute(configfile: Path = DEFAULT_FILE, destfile: Path = DEFAULT_DEST):
    try:

        logger.info(f"Temporary directory: {TMPDIR}")

        if not configfile.exists():
            raise FileNotFoundError(f"File not found: {configfile}")

        # with tempfile.TemporaryDirectory() as tmp:
        #     tmpdir = Path(tmp)

        files = []

        with open(configfile, "r") as f:
            for url in f:
                url = url.strip()
                if url:
                    logger.default(f"Processing URL: {url}", True)
                    purl = Path(urlparse(url).path)
                    filename = purl.name
                    filetemp = Path(TMPDIR) / filename
                    request.urlretrieve(url, str(filetemp))
                    logger.success(f"Downloaded to {filetemp}", True)
                    files.append(str(filetemp))

        logger.default(f"Merging Files ...")

        if not mergeFiles(files, str(destfile)):
            logger.error(f"Failed to merge password files", True, False, 1)

        logger.success(f"Password list generated at {str(destfile)}", True)

    except Exception as e:
        logger.error(f"Script encountered an error: {e}", True)
        raise
    finally:
        shutil.rmtree(TMPDIR)


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file", nargs="?", default=str(DEFAULT_FILE),
                        help="Path to the password sources configuration file")
    parser.add_argument("-d", "--dest", dest="dest", nargs="?", default=str(DEFAULT_DEST),
                        help="Path to the destination file")

    args = parser.parse_args()

    file = Path(args.file)
    dest = Path(args.dest)

    logger: Logger = get_logger("password")

    execute(file, dest)

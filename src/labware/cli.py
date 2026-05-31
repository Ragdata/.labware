#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			19/04/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================

Command Line Module
"""
import typer, rich, sys

from pathlib import Path

BASEDIR = Path(__file__).parents[2]

sys.path.append(str(BASEDIR))

from labware.config import *

config: Config = Config(config_file=BASEDIR / "scr" / "lab" / "cfg" / ".labware.cfg")

sys.path.append(str(BASEDIR / config.get("src", "setup")))

from typing import Annotated

from labware import __version__
from scr.setup import setup


app = typer.Typer(rich_markup_mode="rich", invoke_without_command=True, suggest_commands=True)


@app.callback()
def callback() -> None:
    """LabWare CLI for Homelab Management"""


#--------------------------------------------------------------
# Commands
#--------------------------------------------------------------
@app.command()
def setup() -> None:
    """Setup LabWare"""
    setup.execute()


@app.command()
def version() -> None:
    """Display the version of the LabWare CLI"""
    typer.echo(f"LabWare CLI v{__version__}")


if __name__ == "__main__":
    app()


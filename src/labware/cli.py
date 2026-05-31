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
import typer, rich, os

from typing_extensions import Annotated

from labware import __version__


app = typer.Typer(rich_markup_mode="rich", invoke_without_command=True, suggest_commands=True)


@app.callback()
def callback() -> None:
    """LabWare CLI for Homelab Management"""


#--------------------------------------------------------------
# Commands
#--------------------------------------------------------------
@app.command()
def version(verbose: Annotated[bool, typer.Option(False, "--verbose", "-v", is_flag=True)] = False) -> None:
    """Display the version of the LabWare CLI"""
    typer.echo(f"LabWare CLI v{__version__}")


if __name__ == "__main__":
    app()


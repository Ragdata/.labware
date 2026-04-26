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
"""
import typer, os

from typing import Annotated

from .console import *
from .install import app as installApp

from . import install as installer

from labware import __version__, __pkg_name__


#-------------------------------------------------------------------
# Initialization
#-------------------------------------------------------------------
app = typer.Typer(rich_markup_mode="rich", invoke_without_command=True)

app.add_typer(installApp, name="installer", help="Installer", rich_help_panel="Labware Subcommands")


@app.callback()
def callback() -> None:
    pass

#-------------------------------------------------------------------
# CLI Functions
#-------------------------------------------------------------------
@app.command()
def env() -> None:
    """ Print current environment variables. """
    printInfo("Current Environment Variables:")
    for key, value in os.environ.items():
        printMessage(f"{key}: {value}")

@app.command()
def install() -> None:
    """ Install the package. """
    printInfo("Starting installation process...")
    installer.cmd()

@app.command()
def uninstall():
    pass

@app.command()
def version(
    silent: Annotated[bool, typer.Option("--silent", "-s", help="Return version as variable", rich_help_panel="Output Panel")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Print package name & version", rich_help_panel="Output Panel")] = False,
    vverbose: Annotated[bool, typer.Option("--very-verbose", "-vv", help="Print version data with copyright information", rich_help_panel="Output Panel")] = False
) -> Union[str, None]:
    """ Print the package version information. """
    if silent:
        return __version__
    elif verbose:
        printMessage(f"{__pkg_name__.capitalize()} v{__version__}")
    elif vverbose:
        printMessage(f"{__pkg_name__.capitalize()} v{__version__} ~ Copyright © 2026 Redeyed Technologies", style="yellow")
    else:
        printMessage(f"{__version__}")
    return None


if __name__ == "__main__":
    app()

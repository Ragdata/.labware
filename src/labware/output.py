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
import sys, io

from pathlib import Path

sys.path.append(".")

from rich.text import Text
from rich.theme import Theme
from rich.measure import Measurement
from rich.console import Console, ConsoleOptions, RenderableType

from typing import Optional, Union

from labware.config import *

BASEDIR = Path(config.get("paths", "base"))

_theme = Theme({
    "info": config.get("styles", "info"),
    "success": config.get("styles", "success"),
    "warning": config.get("styles", "warning"),
    "error": config.get("styles", "error"),
    "tip": config.get("styles", "tip"),
    "important": config.get("styles", "important"),
    "debug": config.get("styles", "debug"),
    "head": config.get("styles", "head"),
    "dot": config.get("styles", "dot"),
})

string_io = io.StringIO()

console = Console(theme=_theme)
capture = Console(theme=_theme, file=string_io, force_terminal=True)

red = config.get("colors", "red")
green = config.get("colors", "green")
yellow = config.get("colors", "yellow")
blue = config.get("colors", "blue")
magenta = config.get("colors", "magenta")
cyan = config.get("colors", "cyan")
white = config.get("colors", "white")
black = config.get("colors", "black")

accent1 = config.get("colors", "accent1")
accent2 = config.get("colors", "accent2")

bright_red = config.get("colors", "bright_red")
bright_green = config.get("colors", "bright_green")
bright_yellow = config.get("colors", "bright_yellow")
bright_blue = config.get("colors", "bright_blue")
bright_magenta = config.get("colors", "bright_magenta")
bright_cyan = config.get("colors", "bright_cyan")
bright_white = config.get("colors", "bright_white")
bright_black = config.get("colors", "bright_black")

#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def clear(home=True) -> None:
    """
    Clear the console.

    Args:
    	home (bool): If True, clear the console and move the cursor to the home position.
    """
    console.clear(home)

def getData(prompt: Union[str, Text], **kwargs) -> str:
    """
    Get user input from the console.

    Args:
    	prompt (Union[str, Text]): The prompt to display to the user.
    	**kwargs: Arbitrary keyword arguments.

    Returns:
    	str: The user input.
    """
    return console.input(prompt, **kwargs)

def measure(renderable: RenderableType, options: Optional[ConsoleOptions] = None) -> Measurement:
    """
	Measure the size of a renderable object.

	Args:
		renderable (RenderableType): The object to measure.
		options (Optional[ConsoleOptions]): Console options for measurement.

	Returns:
		Measurement: The measured size of the renderable.
	"""
    return console.measure(renderable, options=options)

def pager(renderable: RenderableType, **kwargs) -> None:
    """
	Display a renderable object in a pager.

	Args:
		renderable (RenderableType): The object to display.
		**kwargs: Arbitrary keyword arguments.
	"""
    with console.pager(**kwargs):
        console.print(renderable)

def printHeader(**kwargs) -> str | None:
    """
	Print the dotfiles banner and copyright information.
	"""
    msg = ""
    if kwargs.get("banner"):
        banner = kwargs["banner"]
        kwargs.pop("banner")
        if not isinstance(banner, Path):
            banner = Path(banner)
        if banner.is_file():
            with open(banner, 'r') as f:
                for lne in f:
                    msg += lne
    if msg:
        if kwargs.get("save"):
            kwargs.pop("save")
            capture.print(msg, **kwargs)
            return string_io.getvalue()
        else:
            console.print(msg, **kwargs)

    return None

def printMessage(msg: str, **kwargs) -> str | None:
    """
	Print a message with an optional style.

	Args:
		msg (str): 	    The message to print.
		**kwargs: 	    Arbitrary keyword arguments. (Optional)
	"""
    if kwargs.get("save"):
        kwargs.pop("save")
        capture.print(msg, **kwargs)
        return string_io.getvalue()
    else:
        console.print(msg, **kwargs)
        return None

def printInfo(msg: str, **kwargs) -> str | None:
    """
    Print an INFO message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "info")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="info", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="info", **kwargs)
        return None

def printSuccess(msg: str, **kwargs) -> str | None:
    """
    Print a SUCCESS message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "success")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="success", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="success", **kwargs)
        return None

def printWarning(msg: str, **kwargs) -> str | None:
    """
    Print a WARNING message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "warning")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="warning", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="warning", **kwargs)
        return None

def printError(msg: str, **kwargs) -> str | None:
    """
    Print an ERROR message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "error")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="error", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="error", **kwargs)
        return None

def printTip(msg: str, **kwargs) -> str | None:
    """
    Print a TIP message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "tip")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="tip", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="tip", **kwargs)
        return None

def printImportant(msg: str, **kwargs) -> str | None:
    """
    Print an IMPORTANT message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "important")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="important", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="important", **kwargs)
        return None

def printDebug(msg: str, **kwargs) -> str | None:
    """
    Print a DEBUG message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "debug")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="debug", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="debug", **kwargs)
        return None

def printHead(msg: str, **kwargs) -> str | None:
    """
    Print a HEAD message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "head")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="head", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="head", **kwargs)
        return None

def printDot(msg: str, **kwargs) -> str | None:
    """
    Print a DOT message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "dot")
    if kwargs.get("save"):
        return printMessage(f"{symbol} " + msg, style="dot", **kwargs)
    else:
        printMessage(f"{symbol} " + msg, style="dot", **kwargs)
        return None

def printDefault(msg: str, **kwargs) -> str | None:
    """
    Print a message in DEFAULT colour

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("save"):
        return printMessage(msg, style="default", **kwargs)
    else:
        printMessage(msg, style="default", **kwargs)
        return None

def printRed(msg: str, **kwargs) -> str | None:
    """
    Print a message in RED

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("save"):
        if kwargs.get("lt"):
            kwargs.pop("lt")
            return printMessage(msg, style=bright_red, **kwargs)
        else:
            return printMessage(msg, style=red, **kwargs)
    else:
        if kwargs.get("lt"):
            kwargs.pop("lt")
            printMessage(msg, style=bright_red, **kwargs)
            return None
        else:
            printMessage(msg, style=red, **kwargs)
            return None

def printGreen(msg: str, **kwargs) -> str | None:
    """
    Print a message in GREEN

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("save"):
        if kwargs.get("lt"):
            kwargs.pop("lt")
            return printMessage(msg, style=bright_green, **kwargs)
        else:
            return printMessage(msg, style=green, **kwargs)
    else:
        if kwargs.get("lt"):
            kwargs.pop("lt")
            printMessage(msg, style=bright_green, **kwargs)
            return None
        else:
            printMessage(msg, style=green, **kwargs)
            return None

def printBlue(msg: str, **kwargs) -> str | None:
    """
    Print a message in BLUE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("save"):
        if kwargs.get("lt"):
            kwargs.pop("lt")
            return printMessage(msg, style=bright_blue, **kwargs)
        else:
            return printMessage(msg, style=blue, **kwargs)
    else:
        if kwargs.get("lt"):
            kwargs.pop("lt")
            printMessage(msg, style=bright_blue, **kwargs)
            return None
        else:
            printMessage(msg, style=blue, **kwargs)
            return None

def printYellow(msg: str, **kwargs) -> str | None:
    """
    Print a message in YELLOW

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("save"):
        if kwargs.get("lt"):
            kwargs.pop("lt")
            return printMessage(msg, style=bright_yellow, **kwargs)
        else:
            return printMessage(msg, style=yellow, **kwargs)
    else:
        if kwargs.get("lt"):
            kwargs.pop("lt")
            printMessage(msg, style=bright_yellow, **kwargs)
            return None
        else:
            printMessage(msg, style=yellow, **kwargs)
            return None

def printPurple(msg: str, **kwargs) -> str | None:
    """
    Print a message in PURPLE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("save"):
        if kwargs.get("lt"):
            kwargs.pop("lt")
            return printMessage(msg, style=bright_magenta, **kwargs)
        else:
            return printMessage(msg, style=magenta, **kwargs)
    else:
        if kwargs.get("lt"):
            kwargs.pop("lt")
            printMessage(msg, style=bright_magenta, **kwargs)
            return None
        else:
            printMessage(msg, style=magenta, **kwargs)
            return None

def printCyan(msg: str, **kwargs) -> str | None:
    """
    Print a message in CYAN

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("save"):
        if kwargs.get("lt"):
            kwargs.pop("lt")
            return printMessage(msg, style=bright_cyan, **kwargs)
        else:
            return printMessage(msg, style=cyan, **kwargs)
    else:
        if kwargs.get("lt"):
            kwargs.pop("lt")
            printMessage(msg, style=bright_cyan, **kwargs)
            return None
        else:
            printMessage(msg, style=cyan, **kwargs)
            return None

def printWhite(msg: str, **kwargs) -> str | None:
    """
    Print a message in WHITE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("save"):
        if kwargs.get("lt"):
            kwargs.pop("lt")
            return printMessage(msg, style=bright_white, **kwargs)
        else:
            return printMessage(msg, style=white, **kwargs)
    else:
        if kwargs.get("lt"):
            kwargs.pop("lt")
            printMessage(msg, style=bright_white, **kwargs)
            return None
        else:
            printMessage(msg, style=white, **kwargs)
            return None

def line(count=1, save: bool = False) -> str | None:
    """
    Add a newline in the console.

    Args:
    	count (int): The number of newlines to add (default: 1).
    	save (bool): If True, save the output to a string buffer.
    """
    if save:
        capture.line(count)
        return string_io.getvalue()
    else:
        console.line(count)
        return None

def rule(*args, **kwargs) -> str | None:
    """
	Draw a line with an optional title
	"""
    if kwargs.get("save"):
        kwargs.pop("save")
        capture.rule(*args, **kwargs)
        return string_io.getvalue()
    else:
        console.rule(*args, **kwargs)
        return None

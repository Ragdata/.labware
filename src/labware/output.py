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
import sys

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

console = Console(theme=_theme)

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

def printHeader(style: Optional[str] = None, banner: Optional[Path] = None, **kwargs) -> None:
    """
	Print the dotfiles banner and copyright information.
	"""
    msg = ""
    if banner and banner.exists():
        with open(banner, 'r') as f:
            for lne in f:
                msg += lne
    if msg:
        console.print(msg, style=style, highlight=False, **kwargs)

def printMessage(msg: str, style: Optional[str] = None, **kwargs) -> None:
    """
	Print a message with an optional style.

	Args:
		msg (str): 	    The message to print.
		style (str):    The style to apply to the message. (Optional)
		**kwargs: 	    Arbitrary keyword arguments. (Optional)
	"""
    if style:
        console.print(msg, style=style, highlight=False, **kwargs)
    else:
        console.print(msg, highlight=False, **kwargs)

def printInfo(msg: str, **kwargs) -> None:
    """
    Print an INFO message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "info")
    printMessage(f"{symbol} " + msg, style="info", **kwargs)

def printSuccess(msg: str, **kwargs) -> None:
    """
    Print a SUCCESS message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "success")
    printMessage(f"{symbol} " + msg, style="success", **kwargs)

def printWarning(msg: str, **kwargs) -> None:
    """
    Print a WARNING message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "warning")
    printMessage(f"{symbol} " + msg, style="warning", **kwargs)

def printError(msg: str, **kwargs) -> None:
    """
    Print an ERROR message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "error")
    printMessage(f"{symbol} " + msg, style="error", **kwargs)

def printTip(msg: str, **kwargs) -> None:
    """
    Print a TIP message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "tip")
    printMessage(f"{symbol} " + msg, style="tip", **kwargs)

def printImportant(msg: str, **kwargs) -> None:
    """
    Print an IMPORTANT message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "important")
    printMessage(f"{symbol} " + msg, style="important", **kwargs)

def printDebug(msg: str, **kwargs) -> None:
    """
    Print a DEBUG message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "debug")
    printMessage(f"{symbol} " + msg, style="debug", **kwargs)

def printHead(msg: str, **kwargs) -> None:
    """
    Print a HEAD message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "head")
    printMessage(f"{symbol} " + msg, style="head", **kwargs)

def printDot(msg: str, **kwargs) -> None:
    """
    Print a DOT message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "dot")
    printMessage(f"{symbol} " + msg, style="dot", **kwargs)

def printDefault(msg: str, **kwargs) -> None:
    """
    Print a message in DEFAULT colour

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    printMessage(msg, style="default", **kwargs)

def printRed(msg: str, **kwargs) -> None:
    """
    Print a message in RED

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        kwargs.pop("lt")
        printMessage(msg, style=bright_red, **kwargs)
    else:
        printMessage(msg, style=red, **kwargs)

def printGreen(msg: str, **kwargs) -> None:
    """
    Print a message in GREEN

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        kwargs.pop("lt")
        printMessage(msg, style=bright_green, **kwargs)
    else:
        printMessage(msg, style=green, **kwargs)

def printBlue(msg: str, **kwargs) -> None:
    """
    Print a message in BLUE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        kwargs.pop("lt")
        printMessage(msg, style=bright_blue, **kwargs)
    else:
        printMessage(msg, style=blue, **kwargs)

def printYellow(msg: str, **kwargs) -> None:
    """
    Print a message in YELLOW

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        kwargs.pop("lt")
        printMessage(msg, style=bright_yellow, **kwargs)
    else:
        printMessage(msg, style=yellow, **kwargs)

def printPurple(msg: str, **kwargs) -> None:
    """
    Print a message in PURPLE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        kwargs.pop("lt")
        printMessage(msg, style=bright_magenta, **kwargs)
    else:
        printMessage(msg, style=magenta, **kwargs)

def printCyan(msg: str, **kwargs) -> None:
    """
    Print a message in CYAN

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        kwargs.pop("lt")
        printMessage(msg, style=bright_cyan, **kwargs)
    else:
        printMessage(msg, style=cyan, **kwargs)

def printWhite(msg: str, **kwargs) -> None:
    """
    Print a message in WHITE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        kwargs.pop("lt")
        printMessage(msg, style=bright_white, **kwargs)
    else:
        printMessage(msg, style=white, **kwargs)

def line(count=1) -> None:
    """
    Add a newline in the console.

    Args:
    	count (int): The number of newlines to add (default: 1).
    """
    console.line(count)

def rule(*args, **kwargs) -> None:
    """
	Draw a line with an optional title
	"""
    console.rule(*args, **kwargs)

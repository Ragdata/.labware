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

from rich.text import Text
from rich.theme import Theme
from rich.measure import Measurement
from rich.console import Console, ConsoleOptions, RenderableType

from typing import Optional, Union
from pathlib import Path

from .config import config
from .logger import outlog


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
    msg = f"{symbol} " + msg
    printMessage(msg, style="info", **kwargs)

def printSuccess(msg: str, **kwargs) -> None:
    """
    Print a SUCCESS message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "success")
    msg = f"{symbol} " + msg
    printMessage(msg, style="success", **kwargs)

def printWarning(msg: str, **kwargs) -> None:
    """
    Print a WARNING message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "warning")
    msg = f"{symbol} " + msg
    printMessage(msg, style="warning", **kwargs)

def printError(msg: str, **kwargs) -> None:
    """
    Print an ERROR message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "error")
    msg = f"{symbol} " + msg
    printMessage(msg, style="error", **kwargs)

def printTip(msg: str, **kwargs) -> None:
    """
    Print a TIP message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "tip")
    msg = f"{symbol} " + msg
    printMessage(msg, style="tip", **kwargs)

def printImportant(msg: str, **kwargs) -> None:
    """
    Print an IMPORTANT message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "important")
    msg = f"{symbol} " + msg
    printMessage(msg, style="important", **kwargs)

def printDebug(msg: str, **kwargs) -> None:
    """
    Print a DEBUG message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "debug")
    msg = f"{symbol} " + msg
    printMessage(msg, style="debug", **kwargs)

def printHead(msg: str, **kwargs) -> None:
    """
    Print a HEAD message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "head")
    msg = f"{symbol} " + msg
    printMessage(msg, style="head", **kwargs)

def printDot(msg: str, **kwargs) -> None:
    """
    Print a DOT message.

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    symbol = config.get("symbols", "dot")
    msg = f"{symbol} " + msg
    printMessage(msg, style="dot", **kwargs)

def printRed(msg: str, **kwargs) -> None:
    """
    Print a message in RED

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_red", **kwargs)
    else:
        printMessage(msg, style="red", **kwargs)

def printGreen(msg: str, **kwargs) -> None:
    """
    Print a message in GREEN

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_green", **kwargs)
    else:
        printMessage(msg, style="green", **kwargs)

def printBlue(msg: str, **kwargs) -> None:
    """
    Print a message in BLUE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_blue", **kwargs)
    else:
        printMessage(msg, style="blue", **kwargs)

def printYellow(msg: str, **kwargs) -> None:
    """
    Print a message in YELLOW

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_yellow", **kwargs)
    else:
        printMessage(msg, style="yellow", **kwargs)

def printPurple(msg: str, **kwargs) -> None:
    """
    Print a message in PURPLE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_magenta", **kwargs)
    else:
        printMessage(msg, style="magenta", **kwargs)

def printCyan(msg: str, **kwargs) -> None:
    """
    Print a message in CYAN

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_cyan", **kwargs)
    else:
        printMessage(msg, style="cyan", **kwargs)

def printWhite(msg: str, **kwargs) -> None:
    """
    Print a message in WHITE

    Args:
    	msg (str): 	The message to print.
    	**kwargs: 	Arbitrary keyword arguments.
    """
    if kwargs.get("lt"):
        printMessage(msg, style="bright_white", **kwargs)
    else:
        printMessage(msg, style="white", **kwargs)

def line(count=1) -> None:
    """
    Add a newline in the console.

    Args:
    	count (int): The number of newlines to add (default: 1).
    """
    console.line(count)

def rule(*args) -> None:
    """
	Draw a line with optional title
	"""
    console.rule(*args)

def errorExit(msg: str, code: int = 1, exc: Exception | None = None) -> None:
    """ Log an error message and exit the program """
    outlog.logError(msg)
    if exc is not None:
        raise exc
    else:
        sys.exit(code)


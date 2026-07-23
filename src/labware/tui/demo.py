#!/usr/bin/env python3
"""
====================================================================
Package: labware.tui
====================================================================
Author:			Ragdata
Date:			16/07/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
Demo App
"""
import os

from fsspec.gui import FileSelector
from textual.app import App
from textual.containers import Grid, Vertical, VerticalScroll
from textual.geometry import Offset
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Log, Static

from labware.tui import icons
from labware.tui.widgets.menu import Menu, MenuBar, MenuHeader, MenuItem, MenuScreen
from labware.tui.dialogs import directory, message, open_file, quit, save, single_choice, single_color_picker, text_entry


about_dialog = message.MessageDialog(
    "Labware TUI Demo",
    icon=icons.ICON_INFORMATION,
    title="About"
)

def toggle_dark_mode(theme: str) -> str:
    if theme == "textual-dark":
        return "textual-light"
    else:
        return "textual-dark"


class Main(Screen):

    CSS_PATH = "demo.tcss"

    BINDINGS = []

    DEFAULT_CSS = """"""

    AUTO_FOCUS = ""

    menu_bar: MenuBar = None
    log_widget: Log = None

    def action_about(self) -> None:
        self.app.push_screen(about_dialog)

    async def on_mount(self) -> None:
        self.menu_bar = MenuBar(MenuHeader(name="TestApp", menu_id="app_menu"))

        self.mount(self.menu_bar)
        self.mount(Footer())

        self.t1 = Label("A simple test application for Labware TUI Widgets")
        self.t2 = Label("https://github.com/Ragdata/.labware")
        await self.mount(Grid(Vertical(self.t1, self.t2)))
        self.t1.parent.move_child(self.t1, after=self.t2)

        menu_screen = self.app.get_screen("menu")



class TestMenuScreen(MenuScreen):
    pass


class TestScreen(Screen):
    pass


class TestApp(App):

    SCREENS = {
        "main": Main,
        "test": TestScreen,
        "menu": TestMenuScreen
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_mount(self) -> None:
        self.push_screen("main")


if __name__ == "__main__":
    app = TestApp()
    app.run

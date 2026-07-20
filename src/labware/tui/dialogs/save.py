#!/usr/bin/env python3
"""
====================================================================
Package: labware.tui.dialogs
====================================================================
Author:			Ragdata
Date:			16/07/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
Save Dialog
"""
import os

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Header, Input, Label

from labware.tui import labels


class SaveFileDialog(ModalScreen[str | bool]):
    DEFAULT_CSS = """"""

    def __init__(self, root: Path = Path("/"), name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.title = "Save File"
        self.root = root
        self.folder = root

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(),
            Label(f"Folder name: {self.root}", id="folder"),
            DirectoryTree(self.root, id="directory"),
            Input(placeholder="filename.txt", id="filename"),
            Horizontal(
                Button(labels.SAVE, variant="primary", id="save_file"),
                Button(labels.CANCEL, variant="error", id="cancel_file"),
                id="save_btn_row"
            ),
            id="save_dialog"
        )

    def on_mount(self) -> None:
        self.query_one("#filename", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()
        if event.button.id == "save_file":
            filename = self.query_one("#filename", Input).value.strip()
            full_path = os.path.join(self.folder, filename)
            self.dismiss(full_path)
        elif event.button.id == "cancel_file":
            self.dismiss(False)

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selection(self, event: DirectoryTree.DirectorySelected) -> None:
        self.folder = str(event.path)
        self.query_one("#folder", Label).update(f"Folder name: {self.folder}")

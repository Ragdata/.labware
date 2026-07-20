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
DirectoryTree Dialog
"""
import platform

from pathlib import Path
from collections.abc import Iterable

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, DirectoryTree, Label, Tree

from labware.tui import labels
from labware.tui.dialogs.text_entry import TextEntryDialog


class DirectoryOnlyTree(DirectoryTree):

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        """Filter the paths to only include directories."""
        return (path for path in paths if path.is_dir())


class DirectoryDialog(ModalScreen[bool | None]):
    DEFAULT_CSS = """"""

    def __init__(
        self,
        root_dir: str = "/",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None
    ):
        super().__init__(name, id, classes)
        self.root_dir = root_dir
        self.folder = root_dir

    def compose(self) -> ComposeResult:
        if "Windows" in platform.platform():
            path_label = "C:\\"
        else:
            path_label = "/"
        yield Vertical(
            Header(),
            DirectoryOnlyTree(self.root_dir, id="directory-tree"),
            Label(f"Folder: {path_label}", id="directory-label"),
            Horizontal(
                Button(labels.NEW_FOLDER, id="make-new-folder", variant="warning"),
                Button(labels.OK, id="directory-ok", variant="primary"),
                Button(labels.CANCEL, id="directory-cancel", variant="error"),
                id="button-container"
            ),
            id="directory-dialog"
        )

    def on_mount(self) -> None:
        self.title = "Choose a Directory"

    def _set_folder(self, path: str) -> None:
        if path == "/" and "Windows" in platform.platform():
            path = "C:\\"
        else:
            path = str(path)

        self.folder = path
        self.query_one("#directory-label", Label).update(f"Folder: {self.folder}")

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        self._set_folder(str(event.path))

    @on(Tree.NodeHighlighted, "#directory-tree")
    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        if event.node.is_root:
            self._set_folder(self.root_dir)

    @on(Button.Pressed, "#directory-ok")
    def on_ok_button(self, event: Button.Pressed) -> None:
        tree = self.query_one("#directory-tree", DirectoryOnlyTree)
        if tree.cursor_node is not None and tree.cursor_node.is_root:
            self._set_folder(self.root_dir)
        self.dismiss(self.folder)

    @on(Button.Pressed, "#directory-cancel")
    def on_cancel_button(self, event: Button.Pressed) -> None:
        self.dismiss(False)

    @on(Button.Pressed, "#make-new-folder")
    def on_make_new_folder(self, event: Button.Pressed) -> None:
        self.app.push_screen(TextEntryDialog("Enter new folder name:", "New Folder"), self.create_new_folder)

    def create_new_folder(self, folder_path: str) -> None:
        if folder_path:
            full_path = Path(self.folder) / folder_path
            self.notify(f"Creating folder: {full_path}")
            Path(full_path).mkdir(parents=True, exist_ok=True)
            tree = self.query_one("#directory-tree", DirectoryOnlyTree)
            tree.reload()

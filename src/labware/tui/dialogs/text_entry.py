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
Text Entry
"""
from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Input, Label

from labware.tui import labels


class TextEntryDialog(ModalScreen[str | bool]):

    DEFAULT_CSS = """
    TextEntryDialog {
        align: center middle;
        background: $primary-lighten-1 30%;
    }

    #text-entry-dlg {
        width: 80;
        height: 14;
        border: thick $background 70%;
        content-align: center middle;
        margin: 1;
    }

    #text-entry-label {
        margin: 1;
    }

    Button {
        width: 50%;
        margin: 1;
    }
    """

    def __init__(self, message: str, title: str, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.message = message
        self.title = title

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(),
            Center(Label(self.message, id="label")),
            Input(placeholder="", id="answer"),
            Center(
                Horizontal(
                    Button(labels.OK, variant="primary", id="ok-btn"),
                    Button(labels.CANCEL, variant="error", id="cancel-btn"),
                    id="buttons",
                )
            ),
            id="text-entry-dlg",
        )

    def on_mount(self) -> None:
        self.query_one("#answer").focus()

    @on(Button.Pressed, "#ok-btn")
    def on_ok(self, event: Button.Pressed) -> None:
        answer = self.query_one("#answer", Input).value.strip()
        self.dismiss(answer)

    @on(Button.Pressed, "#cancel-btn")
    def on_cancel(self, event: Button.Pressed) -> None:
        self.dismiss(False)

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
Message Dialog
"""
from labware.tui import labels

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Label


class MessageDialog(ModalScreen[bool | None]):

    DEFAULT_CSS = """
    MessageDialog {
        align: center middle;
        background: $primary-lighten-1 30%;
    }
    #msg-dlg {
        width: 80;
        height: 12;
        border: thick $background 70%;
        content-align: center middle;
    }
    #message-lbl {
        margin-top: 1;
    }
    #msg-dlg-buttons {
        align: center middle;
    }
    Button {
        margin: 1;
        margin-top: 0
    }
    """

    def __init__(self, message: str, title: str = "", flags: list[str] | None = None, icon: str | Text = "", name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.message = message
        self.title = title
        if flags is None:
            self.flags: list[str] = []
        else:
            self.flags = flags
        self.buttons: list[str] = []
        self.icon = icon

        self.verifyFlags()

    def compose(self) -> ComposeResult:
        buttons = []
        if self.icon:
            message_label = Label(f"{self.icon} {self.message}", id="message-lbl")
        else:
            message_label = Label(self.message, id="message-lbl")
        if "OK" in self.buttons:
            buttons.append(Button("OK", id="ok-btn", variant="primary"))
        if "Cancel" in self.buttons:
            buttons.append(Button("Cancel", id="cancel-btn", variant="error"))
        if "Yes" in self.buttons:
            buttons.append(Button("Yes", id="yes-btn", variant="success"))
        if "No" in self.buttons:
            buttons.append(Button("No", id="no-btn", variant="error"))

        yield Vertical(Header(), Center(message_label), Center(Horizontal(*buttons, id="msg-dlg-buttons")), id="msg-dlg")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "ok-btn":
            self.dismiss(None)
        elif button_id in ["cancel-btn", "no-btn"]:
            self.dismiss(False)
        else:
            self.dismiss(True)

    def verify_flags(self) -> None:
        self.buttons = [btn for btn in self.flags]
        button_count = len(self.buttons)

        if button_count > 2:
            raise ValueError("Only two buttons are allowed")
        elif "OK" in self.buttons and button_count == 2:
            if "Cancel" not in self.buttons:
                raise ValueError("Cancel button is required")
        elif "Yes" in self.buttons and button_count == 2:
            if "No" not in self.buttons:
                raise ValueError("No button is required")
        elif button_count == 0:
            self.buttons.append(labels.OK)

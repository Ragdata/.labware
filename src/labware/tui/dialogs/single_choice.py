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
Single Choice Dialog
"""
from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.visual import VisualType
from textual.widgets import Button, Header, Label, OptionList

from labware.tui import labels


class SingleChoiceDialog(ModalScreen[bool]):

    DEFAULT_CSS = """
    SingleChoiceDialog {
        align: center middle;
        background: $primary 30%;

        #single-choice-dlg {
            width: 85;
            height: 18;
            border: thick $background 70%;
            content-align: center middle;
            margin: 1;
        }

        #single-choice-label {
            margin: 1;
        }

        Button {
            width: 50%;
            margin: 1;
        }
    }
    """

    def __init__(self, message: str, title: str, choices: list[str], name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.message = message
        self.title = title
        self.choices = choices
        self.current_option: VisualType | None = None

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(),
            Center(Label(self.message, id="label")),
            OptionList(*self.choices, id="answer"),
            Center(
                Horizontal(
                    Button(labels.OK, variant="primary", id="ok"),
                    Button(labels.CANCEL, variant="error", id="cancel"),
                    id="button_row"
                )
            ),
            id="single_choice_dlg"
        )

    @on(OptionList.OptionSelected)
    @on(OptionList.OptionHighlighted)
    def on_option_selected(self, event: OptionList.OptionHighlighted | OptionList.OptionSelected) -> None:
        self.current_option = event.option.prompt

    @on(Button.Pressed, "#ok")
    def on_ok(self, event: Button.Pressed) -> None:
        self.dismiss(self.current_option)

    @on(Button.Pressed, "#cancel")
    def on_cancel(self, event: Button.Pressed) -> None:
        self.dismiss(False)

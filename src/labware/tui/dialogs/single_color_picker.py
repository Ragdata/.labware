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
Single Color Picker
"""
from textual._color_constants import COLOR_NAME_TO_RGB
from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Static, Select

from labware.tui import labels


class SingleColorPickerDialog(ModalScreen[str | bool | None]):

    DEFAULT_CSS = """
    SingleColorPickerDialog {
        align: center middle;
        background: $primary 30%;

        #simple-color-dlg {
            width: 50%;
            height: 18;
            border: thick $background 70%;
            content-align: center middle;
        }

        Button {
            width: 50%;
            margin: 1;
        }

        Select {
            margin: 1;
        }

        #chosen-color {
            width: 100%;
            height:5;
        }

        Horizontal {
            height: auto;
        }
    }
    """

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.title = "Color Picker"
        self.current_color: str | None = None

    def compose(self) -> ComposeResult:
       colors = list(COLOR_NAME_TO_RGB.keys())
       colors.sort()
       static = Static(id="chosen-color")
       static.styles.background = None
       static.border_title = "Chosen Color"

       yield Vertical(
           Header(),
           Center(Select.from_values(colors, id="simple-color-picker")),
           Center(static),
           Center(
               Horizontal(
                   Button(labels.OK, variant="primary", id="color-ok"),
                   Button(labels.CANCEL, variant="error", id="color-cancel"),
                   id="color_btn_row"
               )
           ),
           id="simple-color-dlg"
       )

    @on(Select.Changed, "#simple-color-picker")
    def on_selection_changed(self, event: Select.Changed) -> None:
        current_choice = str(event.select.value)
        self.current_color = (str(event.select.value) if self.current_color != current_choice else None)
        static = self.query_one("#chosen-color", Static)
        static.styles.background = self.current_color

    @on(Button.Pressed, "#color-ok")
    def on_ok(self, event: Button.Pressed) -> None:
        self.dismiss(self.current_color)

    @on(Button.Pressed, "#color-cancel")
    def on_cancel(self, event: Button.Pressed) -> None:
        self.dismiss(False)


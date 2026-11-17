"""tkinter-Oberfläche für den einfachen Taschenrechner."""

import tkinter as tk
from functools import partial
from typing import Callable, Dict

from calculator import OPERATORS, Calculator

BUTTON_ROWS = (
    ("C", "⌫", "±", "/"),
    ("7", "8", "9", "*"),
    ("4", "5", "6", "-"),
    ("1", "2", "3", "+"),
    ("0", ".", "="),
)

# (Hintergrund, Vordergrund)
STYLES = {
    "default": ("#e0e0e0", "#000000"),
    "operator": ("#ff9800", "#ffffff"),
    "equals": ("#2196f3", "#ffffff"),
    "clear": ("#f44336", "#ffffff"),
}


class CalculatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Einfacher Rechner")
        self.resizable(False, False)
        self.configure(padx=8, pady=8)

        self._display_var = tk.StringVar(value="0")
        self._calculator = Calculator(on_change=self._display_var.set)

        self._build_display()
        self._build_buttons()

        self.bind("<Key>", self._on_key)
        self.focus_set()

    def _build_display(self) -> None:
        tk.Entry(
            self,
            textvariable=self._display_var,
            font=("Segoe UI", 20),
            justify="right",
            state="readonly",
            width=14,
            bd=2,
            relief="sunken",
        ).grid(row=0, column=0, columnspan=4, padx=2, pady=4, sticky="nsew")

    def _build_buttons(self) -> None:
        for row, labels in enumerate(BUTTON_ROWS, start=1):
            col = 0
            for label in labels:
                span = 2 if label == "0" else 1
                self._add_button(label, row, col, span)
                col += span

        for col in range(4):
            self.grid_columnconfigure(col, weight=1)
        for row in range(len(BUTTON_ROWS) + 1):
            self.grid_rowconfigure(row, weight=1)

    def _add_button(self, label: str, row: int, col: int, span: int) -> None:
        background, foreground = self._style_for(label)
        tk.Button(
            self,
            text=label,
            width=5,
            height=2,
            font=("Segoe UI", 14),
            bg=background,
            fg=foreground,
            command=self._command_for(label),
            takefocus=0,
        ).grid(row=row, column=col, columnspan=span, padx=2, pady=2, sticky="nsew")

    @staticmethod
    def _style_for(label: str):
        if label in OPERATORS:
            return STYLES["operator"]
        if label == "=":
            return STYLES["equals"]
        if label == "C":
            return STYLES["clear"]
        return STYLES["default"]

    def _command_for(self, label: str) -> Callable[[], None]:
        if label.isdigit():
            return partial(self._calculator.press_digit, label)
        if label in OPERATORS:
            return partial(self._calculator.press_operator, label)

        commands: Dict[str, Callable[[], None]] = {
            "C": self._calculator.clear,
            "⌫": self._calculator.backspace,
            "±": self._calculator.toggle_sign,
            ".": self._calculator.press_decimal,
            "=": self._calculator.press_equals,
        }
        return commands[label]

    def _on_key(self, event: tk.Event) -> str:
        char = event.char
        if char.isdigit():
            self._calculator.press_digit(char)
        elif char in (".", ","):
            self._calculator.press_decimal()
        elif char in OPERATORS:
            self._calculator.press_operator(char)
        elif event.keysym in ("Return", "KP_Enter", "Equal"):
            self._calculator.press_equals()
        elif event.keysym == "BackSpace":
            self._calculator.backspace()
        elif event.keysym in ("Escape", "Delete"):
            self._calculator.clear()
        return "break"


if __name__ == "__main__":
    CalculatorApp().mainloop()

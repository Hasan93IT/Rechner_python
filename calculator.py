"""Reine Rechenlogik des Taschenrechners — ohne GUI-Abhängigkeiten."""

import math
from typing import Callable, Optional

ERROR = "Fehler"
OPERATORS = frozenset("+-*/")
MAX_INPUT_LENGTH = 12
PRECISION = 10


class Calculator:
    """Hält den Zustand einer Rechnung und meldet Anzeige-Änderungen."""

    def __init__(self, on_change: Optional[Callable[[str], None]] = None) -> None:
        self._on_change = on_change
        self._accumulator: Optional[float] = None
        self._operator: Optional[str] = None
        self._awaiting_operand = True
        self._display = "0"

    @property
    def display(self) -> str:
        """Aktueller Anzeigewert."""
        return self._display

    # --- Eingaben ------------------------------------------------------

    def press_digit(self, digit: str) -> None:
        if len(digit) != 1 or digit not in "0123456789":
            raise ValueError(f"Ungültige Ziffer: {digit!r}")

        if self._awaiting_operand or self._display in ("0", ERROR):
            self._set_display(digit)
            self._awaiting_operand = False
        elif len(self._display) < MAX_INPUT_LENGTH:
            self._set_display(self._display + digit)

    def press_decimal(self) -> None:
        if self._awaiting_operand or self._display in ("0", ERROR):
            self._set_display("0.")
            self._awaiting_operand = False
        elif "." not in self._display:
            self._set_display(self._display + ".")

    def press_operator(self, operator: str) -> None:
        if operator not in OPERATORS:
            raise ValueError(f"Ungültiger Operator: {operator!r}")

        if not self._resolve_pending():
            return
        if self._accumulator is None:
            self._accumulator = self._read_display()

        self._operator = operator
        self._awaiting_operand = True

    def press_equals(self) -> None:
        if self._resolve_pending():
            self._reset_state()

    def clear(self) -> None:
        self._reset_state()
        self._set_display("0")

    def backspace(self) -> None:
        if self._awaiting_operand or self._display == ERROR:
            return

        text = self._display
        if len(text) <= 1 or (len(text) == 2 and text.startswith("-")):
            self._set_display("0")
            self._awaiting_operand = True
        else:
            self._set_display(text[:-1])

    def toggle_sign(self) -> None:
        if self._display == ERROR:
            return

        if self._awaiting_operand and self._accumulator is not None:
            self._accumulator = -self._accumulator
            self._set_display(self._format(self._accumulator))
        elif self._display.startswith("-"):
            self._set_display(self._display[1:])
        elif self._display != "0":
            self._set_display("-" + self._display)

    # --- Interna -------------------------------------------------------

    def _reset_state(self) -> None:
        self._accumulator = None
        self._operator = None
        self._awaiting_operand = True

    def _set_display(self, text: str) -> None:
        self._display = text
        if self._on_change is not None:
            self._on_change(text)

    def _read_display(self) -> float:
        try:
            return float(self._display)
        except ValueError:
            return 0.0

    def _resolve_pending(self) -> bool:
        """Führt eine offene Operation aus. False bedeutet Fehler."""
        if self._operator is None or self._awaiting_operand or self._accumulator is None:
            return True

        try:
            result = self._apply(self._accumulator, self._read_display(), self._operator)
        except ZeroDivisionError:
            self._reset_state()
            self._set_display(ERROR)
            return False

        self._set_display(self._format(result))
        self._accumulator = result
        return True

    @staticmethod
    def _apply(a: float, b: float, operator: str) -> float:
        if operator == "+":
            return a + b
        if operator == "-":
            return a - b
        if operator == "*":
            return a * b
        if operator == "/":
            if b == 0:
                raise ZeroDivisionError("Division durch Null")
            return a / b
        raise ValueError(f"Unbekannter Operator: {operator!r}")

    @staticmethod
    def _format(value: float) -> str:
        if not math.isfinite(value):
            return ERROR
        if value == int(value):
            return str(int(value))
        return f"{value:.{PRECISION}g}"

"""Unit-Tests für die Rechenlogik (unabhängig von tkinter)."""

import re
import unittest

from calculator import ERROR, Calculator

NUMBER = re.compile(r"-?\d+(?:\.\d+)?")


class CalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def enter(self, *tokens: str) -> str:
        """Gibt eine Folge wie '7', '+', '8', '=' ein."""
        for token in tokens:
            if NUMBER.fullmatch(token):
                for char in token:
                    if char == ".":
                        self.calc.press_decimal()
                    elif char == "-":
                        self.calc.toggle_sign()
                    else:
                        self.calc.press_digit(char)
            elif token == ".":
                self.calc.press_decimal()
            elif token in "+-*/":
                self.calc.press_operator(token)
            elif token == "=":
                self.calc.press_equals()
            elif token == "C":
                self.calc.clear()
            elif token == "⌫":
                self.calc.backspace()
            elif token == "±":
                self.calc.toggle_sign()
            else:
                raise AssertionError(f"Unbekanntes Token: {token!r}")
        return self.calc.display

    def test_grundrechenarten(self) -> None:
        for tokens, expected in (
            (("7", "+", "8", "="), "15"),
            (("9", "-", "4", "="), "5"),
            (("6", "*", "7", "="), "42"),
            (("8", "/", "2", "="), "4"),
        ):
            with self.subTest(tokens=tokens):
                self.assertEqual(self.enter(*tokens), expected)

    def test_kettenrechnung(self) -> None:
        self.assertEqual(self.enter("5", "*", "3", "+", "2", "="), "17")

    def test_dezimalzahlen(self) -> None:
        self.assertEqual(self.enter("0.1", "+", "0.2", "="), "0.3")

    def test_division_durch_null(self) -> None:
        self.assertEqual(self.enter("1", "/", "0", "="), ERROR)
        self.assertEqual(self.enter("9"), "9")

    def test_operator_wird_ersetzt(self) -> None:
        self.assertEqual(self.enter("8", "+", "*", "2", "="), "16")

    def test_vorzeichen(self) -> None:
        self.assertEqual(self.enter("5", "+", "±", "3", "="), "-2")

    def test_loeschen_und_backspace(self) -> None:
        self.assertEqual(self.enter("1", "2", "3", "⌫"), "12")
        self.assertEqual(self.enter("C"), "0")

    def test_aenderung_wird_gemeldet(self) -> None:
        updates = []
        calc = Calculator(on_change=updates.append)
        calc.press_digit("4")
        calc.press_operator("+")
        calc.press_digit("1")
        calc.press_equals()
        self.assertEqual(updates[-1], "5")


if __name__ == "__main__":
    unittest.main()

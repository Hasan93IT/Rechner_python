# Rechner_python

[![CI](https://github.com/Hasan93IT/Rechner_python/actions/workflows/ci.yml/badge.svg)](https://github.com/Hasan93IT/Rechner_python/actions/workflows/ci.yml)

Einfacher Taschenrechner mit einer tkinter-GUI.

## Aufbau

| Datei | Zweck |
| --- | --- |
| `calculator.py` | Reine Rechenlogik, ohne GUI-Abhängigkeiten |
| `main.py` | tkinter-Oberfläche |
| `test_calculator.py` | Unit-Tests für die Rechenlogik |

## Starten

In PyCharm `main.py` ausführen oder im Projektverzeichnis:

```bash
python main.py
```

Bedienung: Ziffern und Operatoren über Buttons oder Tastatur, `Enter` für `=`,
`Backspace` für `⌫`, `Esc` für `C`.

## Tests

```bash
python -m unittest discover -v
```

## Continuous Integration

Die GitHub-Action `.github/workflows/ci.yml` läuft bei jedem Push, jedem Pull
Request und manuell. Sie prüft die Syntax aller Python-Dateien und führt die
Unit-Tests aus — auf Ubuntu und Windows mit Python 3.9 bis 3.13.

# -*- coding: utf-8 -*-
import re
import string
import unittest
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "math-symbols.ahk"
SCRIPT_TEXT = SCRIPT.read_text(encoding="utf-8")


def parse_string_map(name):
    match = re.search(
        rf"global {re.escape(name)} := Map\(\n(?P<body>.*?)\n\)",
        SCRIPT_TEXT,
        re.S,
    )
    if not match:
        raise AssertionError(f"{name} map not found")

    return dict(
        re.findall(r'^\s*"([^"]+)",\s*"([^"]+)"(?:,)?$', match.group("body"), re.M)
    )


def parse_bool_map_keys(name):
    match = re.search(
        rf"global {re.escape(name)} := Map\(\n(?P<body>.*?)\n\)",
        SCRIPT_TEXT,
        re.S,
    )
    if not match:
        raise AssertionError(f"{name} map not found")

    return set(
        re.findall(r'^\s*"([^"]+)",\s*true(?:,)?$', match.group("body"), re.M)
    )


@dataclass(frozen=True)
class Hotstring:
    options: str
    function: str
    output: str


HOTSTRING_RE = re.compile(
    r'^:X(?P<options>[^:]*):(?P<trigger>/[^:]+)::'
    r'(?P<function>PasteSymbol|PasteImmediate) "(?P<output>[^"]*)"$',
    re.M,
)


def parse_hotstrings():
    parsed = {}
    for match in HOTSTRING_RE.finditer(SCRIPT_TEXT):
        parsed[match.group("trigger")] = Hotstring(
            options=match.group("options"),
            function=match.group("function"),
            output=match.group("output"),
        )
    return parsed


class MathSymbolModeTests(unittest.TestCase):
    def test_superscript_mode_map(self):
        self.assertEqual(
            parse_string_map("SuperscriptChars"),
            {
                "0": "⁰",
                "1": "¹",
                "2": "²",
                "3": "³",
                "4": "⁴",
                "5": "⁵",
                "6": "⁶",
                "7": "⁷",
                "8": "⁸",
                "9": "⁹",
                "+": "⁺",
                "-": "⁻",
                "/": "ᐟ",
                "=": "⁼",
                "(": "⁽",
                ")": "⁾",
                "a": "ᵃ",
                "b": "ᵇ",
                "c": "ᶜ",
                "d": "ᵈ",
                "e": "ᵉ",
                "f": "ᶠ",
                "g": "ᵍ",
                "h": "ʰ",
                "i": "ⁱ",
                "j": "ʲ",
                "k": "ᵏ",
                "l": "ˡ",
                "m": "ᵐ",
                "n": "ⁿ",
                "o": "ᵒ",
                "p": "ᵖ",
                "r": "ʳ",
                "s": "ˢ",
                "t": "ᵗ",
                "u": "ᵘ",
                "v": "ᵛ",
                "w": "ʷ",
                "x": "ˣ",
                "y": "ʸ",
                "z": "ᶻ",
            },
        )

    def test_subscript_mode_map_and_known_unicode_gaps(self):
        subscript_chars = parse_string_map("SubscriptChars")
        unsupported = parse_bool_map_keys("UnsupportedSubscriptChars")

        self.assertEqual(
            subscript_chars,
            {
                "0": "₀",
                "1": "₁",
                "2": "₂",
                "3": "₃",
                "4": "₄",
                "5": "₅",
                "6": "₆",
                "7": "₇",
                "8": "₈",
                "9": "₉",
                "+": "₊",
                "-": "₋",
                "=": "₌",
                "(": "₍",
                ")": "₎",
                "a": "ₐ",
                "e": "ₑ",
                "h": "ₕ",
                "i": "ᵢ",
                "j": "ⱼ",
                "k": "ₖ",
                "l": "ₗ",
                "m": "ₘ",
                "n": "ₙ",
                "o": "ₒ",
                "p": "ₚ",
                "r": "ᵣ",
                "s": "ₛ",
                "t": "ₜ",
                "u": "ᵤ",
                "v": "ᵥ",
                "x": "ₓ",
                "y": "ᵧ",
            },
        )
        self.assertEqual(unsupported, set("/bcdfgqwz"))
        self.assertFalse(set(subscript_chars) & unsupported)

        covered_lowercase = (
            {key for key in subscript_chars if key in string.ascii_lowercase}
            | (unsupported & set(string.ascii_lowercase))
        )
        self.assertEqual(covered_lowercase, set(string.ascii_lowercase))

    def test_mode_hotkeys_route_all_keyboard_letters_digits_and_symbols(self):
        routed_chars = set(re.findall(r'::ModeType "([^"]+)"', SCRIPT_TEXT))
        self.assertEqual(
            routed_chars,
            set(string.ascii_lowercase)
            | set(string.ascii_uppercase)
            | set(string.digits)
            | set("+-/=()"),
        )

    def test_mode_function_wiring(self):
        self.assertIn("WaitForHotstringKeys()", SCRIPT_TEXT)
        self.assertIn('SendInput "^v"', SCRIPT_TEXT)
        self.assertIn('endChar := A_EndChar = "`t" ? "" : A_EndChar', SCRIPT_TEXT)
        self.assertIn("PasteText symbol endChar", SCRIPT_TEXT)
        self.assertIn("PasteText symbol", SCRIPT_TEXT)
        self.assertIn('ToggleSymbolMode(mode) {', SCRIPT_TEXT)
        self.assertIn('SetSymbolMode(mode) {', SCRIPT_TEXT)
        self.assertIn('ShowUnsupportedSubscript(char) {', SCRIPT_TEXT)
        self.assertIn("UnsupportedSubscriptChars.Has(char)", SCRIPT_TEXT)


class MathHotstringTests(unittest.TestCase):
    def test_hotstrings_are_parseable_and_unique(self):
        matches = list(HOTSTRING_RE.finditer(SCRIPT_TEXT))
        triggers = [match.group("trigger") for match in matches]

        self.assertGreaterEqual(len(matches), 150)
        self.assertEqual(len(triggers), len(set(triggers)))

    def test_hotstrings_cover_major_symbol_areas(self):
        hotstrings = parse_hotstrings()
        expected_by_area = {
            "logic": {
                "/neg": ("PasteSymbol", "¬"),
                "/and": ("PasteSymbol", "∧"),
                "/xor": ("PasteSymbol", "⊕"),
                "/implies": ("PasteSymbol", "⇒"),
                "/iff": ("PasteSymbol", "↔"),
                "/vdash": ("PasteSymbol", "⊢"),
            },
            "quantifiers": {
                "/forall": ("PasteSymbol", "∀"),
                "/exists": ("PasteSymbol", "∃"),
                "/nexists": ("PasteSymbol", "∄"),
                "/unique": ("PasteSymbol", "∃!"),
            },
            "sets": {
                "/in": ("PasteSymbol", "∈"),
                "/notin": ("PasteSymbol", "∉"),
                "/subseteq": ("PasteSymbol", "⊆"),
                "/cup": ("PasteSymbol", "∪"),
                "/emptyset": ("PasteSymbol", "∅"),
                "/powerset": ("PasteSymbol", "𝒫"),
            },
            "relations_functions_products": {
                "/times": ("PasteSymbol", "×"),
                "/circ": ("PasteSymbol", "∘"),
                "/mapsto": ("PasteSymbol", "↦"),
                "/dom": ("PasteSymbol", "dom"),
                "/inv": ("PasteImmediate", "⁻¹"),
                "/degree": ("PasteSymbol", "°"),
            },
            "comparison_arithmetic": {
                "/leq": ("PasteSymbol", "≤"),
                "/neq": ("PasteSymbol", "≠"),
                "/approx": ("PasteSymbol", "≈"),
                "/---": ("PasteSymbol", "—"),
                "/sqrt": ("PasteSymbol", "√"),
                "/integral": ("PasteSymbol", "∫"),
            },
            "number_systems_constants": {
                "/N": ("PasteSymbol", "ℕ"),
                "/L": ("PasteSymbol", "ℒ"),
                "/l": ("PasteSymbol", "ℓ"),
                "/pi": ("PasteSymbol", "π"),
                "/Sigma": ("PasteSymbol", "Σ"),
                "/partial": ("PasteSymbol", "∂"),
            },
            "arrows": {
                "/left": ("PasteSymbol", "←"),
                "/ra": ("PasteSymbol", "→"),
                "/La": ("PasteSymbol", "⇐"),
                "/LRa": ("PasteSymbol", "⇔"),
            },
            "superscript_hotstrings": {
                "/^0": ("PasteImmediate", "⁰"),
                "/^n": ("PasteImmediate", "ⁿ"),
                "/^i": ("PasteImmediate", "ⁱ"),
                "/^-": ("PasteImmediate", "⁻"),
                "/^+": ("PasteImmediate", "⁺"),
            },
            "subscript_hotstrings": {
                "/_0": ("PasteImmediate", "₀"),
                "/_a": ("PasteImmediate", "ₐ"),
                "/_j": ("PasteImmediate", "ⱼ"),
                "/_v": ("PasteImmediate", "ᵥ"),
                "/_y": ("PasteImmediate", "ᵧ"),
            },
            "proof_words": {
                "/pf": ("PasteSymbol", "Proof."),
                "/claim": ("PasteSymbol", "Claim."),
                "/st": ("PasteSymbol", "such that"),
                "/wlog": ("PasteSymbol", "without loss of generality"),
                "/contradiction": ("PasteSymbol", "contradiction"),
            },
        }

        for area, expected in expected_by_area.items():
            with self.subTest(area=area):
                for trigger, (function, output) in expected.items():
                    self.assertIn(trigger, hotstrings)
                    self.assertEqual(hotstrings[trigger].function, function)
                    self.assertEqual(hotstrings[trigger].output, output)

    def test_immediate_suffix_hotstrings_fire_without_an_end_char(self):
        hotstrings = parse_hotstrings()
        immediate_triggers = [
            trigger
            for trigger in hotstrings
            if trigger.startswith("/^") or trigger.startswith("/_") or trigger == "/inv"
        ]

        self.assertGreaterEqual(len(immediate_triggers), 35)
        for trigger in immediate_triggers:
            with self.subTest(trigger=trigger):
                self.assertEqual(hotstrings[trigger].function, "PasteImmediate")
                self.assertIn("*", hotstrings[trigger].options)

    def test_case_sensitive_aliases_are_preserved(self):
        hotstrings = parse_hotstrings()

        self.assertIn("#Hotstring C", SCRIPT_TEXT)
        self.assertEqual(hotstrings["/sigma"].output, "σ")
        self.assertEqual(hotstrings["/Sigma"].output, "Σ")
        self.assertEqual(hotstrings["/ra"].output, "→")
        self.assertEqual(hotstrings["/Ra"].output, "⇒")
        self.assertEqual(hotstrings["/l"].output, "ℓ")
        self.assertEqual(hotstrings["/L"].output, "ℒ")


if __name__ == "__main__":
    unittest.main()

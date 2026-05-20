# math-notes-helper
Contains an AutoHotkey (.ahk) file which allows for simpler math notes anywhere on your computer. 

## Mode limitations

Superscript and subscript modes paste single Unicode characters where Unicode
provides them. Some letters do not have matching single-codepoint forms:

- Superscript mode supports lowercase letters except `q`.
- Subscript mode supports `a`, `e`, `h`, `i`, `j`, `k`, `l`, `m`, `n`, `o`,
  `p`, `r`, `s`, `t`, `u`, `v`, `x`, and `y`.
- Subscript mode cannot convert `b`, `c`, `d`, `f`, `g`, `q`, `w`, or `z`.
- Uppercase letters are not converted in either mode.

## Tests

Run the static test suite with:

```powershell
python -m unittest discover -s tests -v
```

The tests cover the AHK mode maps, hotstring groups, immediate suffix
hotstrings, and known Unicode gaps in superscript and subscript modes.

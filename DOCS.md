# Ethos — Language Syntax & Hard Trait Reference

**v0.1.0-alpha** · by [Aman Adlakha](https://github.com/amancode22)

> The Hard Trait SDK (C/C++ and Rust) is under development and will be released separately. This document covers the language syntax and the runtime format the Ethos executor uses to load Hard Traits.

---

## Contents

1. [How the syntax works](#1-how-the-syntax-works)
2. [How the lexer works](#2-how-the-lexer-works)
3. [Statements](#3-statements)
4. [Operators](#4-operators)
5. [Hard Trait runtime format](#5-hard-trait-runtime-format)
6. [Soft Trait runtime](#6-soft-trait-runtime)
7. [Errors](#7-errors)

---

## 1. How the syntax works

Ethos programs are `.ethos` files. The rules:

- Every statement is a sentence ending with a **period**.
- Keywords are case-insensitive. String contents are not.
- Strings go in `"double"` or `'single'` quotes.
- Indentation doesn't matter — the parser tracks block depth itself. Indent anyway for readability.
- Blank lines are ignored.

---

## 2. How the lexer works

Two passes happen before anything runs.

**Pass 1 — split into sentences.** The source is cut on every `.` that isn't inside a quoted string. Each chunk becomes one statement.

**Pass 2 — tokenize.** Each sentence is split into words using POSIX-style shell splitting (so quoted strings stay intact). Everything outside quotes is lowercased. The trailing `.` is stripped from the last token.

Then a pre-processing step merges these multi-word phrases into single tokens:

```
is not          is above        is below
is at least     is at most      divided by
to the power of bring in        how to
otherwise if    run function    delete variable
```

---

## 3. Statements

### `say` — print something

```
say <value>.
```

```
say "Hello.".
say score.
say 42.
```

→ `print(<value>)`

---

### `set` — assign a variable

```
set <var> to <expression>.
```

Expressions can mix variables, literals, and arithmetic operators.

```
set x to 10.
set name to "Aman".
set total to x times 3 plus 1.
```

**String slicing:**

```
set <var> to <source> from <start> to <end>.
```

```
set piece to name from 0 to 3.
```

→ `piece = name[0:3]`

---

### `add` / `subtract` — in-place arithmetic

```
add <value> to <var>.
subtract <value> from <var>.
```

```
add 1 to counter.
subtract 5 from health.
```

→ `counter += 1` / `health -= 5`

---

### `delete variable` — delete a variable

```
delete variable <name>.
```

→ `del name`

---

### `ask` — read user input

```
ask <"prompt"> into <var>.
```

Must be exactly four tokens. `into` is required.

```
ask "Your name: " into username.
```

→ `username = input("Your name: ")`

---

### `if` / `otherwise` / `end` — conditionals

```
if <condition>.
    ...
otherwise if <condition>.
    ...
otherwise.
    ...
end.
```

One `end.` closes the whole chain. `otherwise if` → `elif`, `otherwise` alone → `else`.

```
if score is above 90.
    say "A".
otherwise if score is at least 75.
    say "B".
otherwise.
    say "C".
end.
```

Conditions can chain with `and`, `or`, `not`:

```
if age is at least 18 and verified is 1.
    say "Access granted.".
end.
```

---

### `repeat` — loop N times

```
repeat <n>.
    ...
end.
```

Loop variable is anonymous (`_`).

→ `for _ in range(n):`

---

### `count` — ranged loop

```
count from <start> to <end> variable <var>.
    ...
end.
```

Optional step:

```
count from <start> to <end> variable <var> stepping <step>.
    ...
end.
```

```
count from 1 to 5 variable i.
    say i.
end.

count from 10 to 0 variable i stepping -2.
    say i.
end.
```

→ `for i in range(start, int(end) + 1, step):`  
(End offset flips: `+1` going forward, `-1` going backward.)

---

### `while` — condition loop

```
while <condition>.
    ...
end.
```

```
while lives is above 0.
    subtract 1 from lives.
end.
```

---

### `how to` / `run` — functions

**Define:**

```
how to <name>.
    ...
end.

how to <name> with <param1>, <param2>.
    ...
end.
```

**Call:**

```
run <name>.
run <name> with <arg1>, <arg2>.
run function <name> with <arg1>.
```

`run` and `run function` do the same thing.

```
how to greet with name.
    say name.
end.

run greet with "Aman".
```

---

### `bring in` — import a module or Soft Trait

```
bring in <module>.
```

→ `import <module>`

---

### `note` / `notes` — comments

```
note single line comment.

notes.
block comment
spanning lines.
endnotes.
```

→ `# ...` and `''' ... '''`

---

### `python` / `pythonend` — inspect generated Python

Statements inside this block print the transpiled Python instead of running it.

```
python.
set x to 5 plus 3.
pythonend.
```

Output: `PY_GEN: x =  5 + 3`

---

### `debug` / `debugend` — trace tokens

Prints the token list for each statement before it executes.

```
debug.
set x to 10.
debugend.
```

Output: `DEBUG: set x to 10`

---

## 4. Operators

### Arithmetic

| Ethos              | Python |
|--------------------|--------|
| `plus`             | `+`    |
| `minus`            | `-`    |
| `times`            | `*`    |
| `divided by`       | `/`    |
| `to the power of`  | `**`   |

### Comparison

| Ethos          | Python |
|----------------|--------|
| `is`           | `==`   |
| `is not`       | `!=`   |
| `is above`     | `>`    |
| `is below`     | `<`    |
| `is at least`  | `>=`   |
| `is at most`   | `<=`   |

### Logical

| Ethos  | Python |
|--------|--------|
| `and`  | `and`  |
| `or`   | `or`   |
| `not`  | `not`  |

---

## 5. Hard Trait runtime format

The Hard Trait SDK (C/C++ and Rust) is under development. This section documents what the Ethos runtime currently expects from an installed Hard Trait — enough to understand how loading works, not enough to write one from scratch yet.

Community SDK contributions for languages other than C/C++ and Rust are welcome via PR.

### Directory layout

```
~/.ethos/traits/hard_traits/<trait-name>/
├── manifest.json
└── <binary>.so
```

The folder name must match the `name` field in `manifest.json`.

---

### manifest.json

```json
{
  "name": "mymath",
  "binary": "mymath.so",
  "functions": {
    "add_ints": {
      "return": "int",
      "args": ["int", "int"]
    },
    "get_message": {
      "return": "char *",
      "args": []
    }
  }
}
```

| Field | Required | Description |
|---|---|---|
| `name` | ✅ | Trait name. Must match the directory name. |
| `binary` | ✅ | Shared library filename, relative to the trait folder. |
| `functions` | ✅ | Map of exported function names to their signatures. |
| `functions.<n>.return` | ✅ | Return type string. Use `"void"` for no return value. |
| `functions.<n>.args` | ✅ | List of argument type strings. Use `[]` for none. |

---

### Supported types

| manifest string          | C type               |
|--------------------------|----------------------|
| `"char"`                 | `char`               |
| `"unsigned char"`        | `unsigned char`      |
| `"wchar_t"`              | `wchar_t`            |
| `"short"`                | `short`              |
| `"unsigned short"`       | `unsigned short`     |
| `"int"`                  | `int`                |
| `"unsigned int"`         | `unsigned int`       |
| `"long"`                 | `long`               |
| `"unsigned long"`        | `unsigned long`      |
| `"long long"`            | `long long`          |
| `"unsigned long long"`   | `unsigned long long` |
| `"int8_t"`               | `int8_t`             |
| `"uint8_t"`              | `uint8_t`            |
| `"int16_t"`              | `int16_t`            |
| `"uint16_t"`             | `uint16_t`           |
| `"float"`                | `float`              |
| `"double"`               | `double`             |
| `"long double"`          | `long double`        |
| `"char *"`               | `char *`             |
| `"wchar_t *"`            | `wchar_t *`          |
| `"void *"`               | `void *`             |
| `"pointer_to_int"`       | `int *`              |
| `"size_t"`               | `size_t`             |
| `"ssize_t"`              | `ssize_t`            |
| `"bool"`                 | `bool`               |
| `"void"`                 | (no return value)    |

An unrecognized type skips that one function with a warning. The rest of the trait loads fine.

---

### SDK language support

| Language | Status |
|---|---|
| C / C++ | Official SDK — under development |
| Rust | Official SDK — under development |
| Everything else | Community PRs welcome |

---

### How loading works

On startup, Ethos scans `~/.ethos/traits/hard_traits/` and for each subfolder:

1. Looks for `manifest.json` — missing → warning, skip.
2. Parses it as JSON — invalid → warning, skip.
3. Checks the binary file exists — missing → warning, skip.
4. Loads it with `ctypes.CDLL`.
5. Wires up `restype` and `argtypes` for each function in `"functions"`. Bad type → warning for that function only, rest still loads.
6. Puts the library object in the execution environment under the trait's `name`. Your Ethos program can then call its functions.

---

## 6. Soft Trait runtime

Soft Traits are Python packages sitting in `~/.ethos/traits/`. At startup, that folder is prepended to `sys.path`. That's it — `bring in` just works.

Forge never runs install scripts. It only extracts the wheel or sdist archive. For a package to be importable, its top-level module folder must land directly inside `~/.ethos/traits/` after extraction.

---

## 7. Errors

### Parser

| Message | What happened |
|---|---|
| `Error: 'end' found without a matching block` | `end.` with no matching `if`, `while`, `repeat`, `count`, or `how to`. |
| `Error: 'say' needs a value` | `say` used with nothing after it. |
| `Invalid syntax used, correct syntax is ask 'Prompt string' into variable_name` | `ask` missing `into`, or wrong number of tokens. |

### Runtime

| Message | What happened |
|---|---|
| `Ethos Runtime Error: <msg>` | Exception raised during `exec()`. Python error shown. |

### Hard Trait loading

| Message | What happened |
|---|---|
| `Warning: Trait <n> does not have a manifest.json file...` | No manifest found in the trait folder. |
| `Warning: Trait <n> manifest.json file is invalid...` | Manifest isn't valid JSON. |
| `Warning: Trait <n> binary path defined in manifest.json is invalid...` | The `.so` file listed in `"binary"` doesn't exist. |
| `Warning: In trait <n> there is a function named <fn> of which types are not correctly written...` | Type string not in the supported types table. |

### Forge

| Message | What happened |
|---|---|
| `[-] This package does not exist or its a network error/pypi might be blocked` | PyPI lookup failed or package doesn't exist. |
| `[-] Cannot get results from pypi...` | PyPI response couldn't be decoded. |
| `[-] This package doesnt support your system and its tar sdist isnt published` | No compatible wheel or sdist for this platform. |
| `[-] Invalid Hard Trait: No manifest.json found` | Zip passed to Forge has no manifest. |
| `[-] Trait cannot be installed due to invalid manifest.json.` | Manifest missing `name` or `binary`. |
| `[-] Failed to remove. Soft trait <n> is not installed.` | Package not found in `~/.ethos/traits/`. |
| `[-] Failed to remove. Hard trait <n> is not installed.` | Trait not found in `~/.ethos/traits/hard_traits/`. |

---

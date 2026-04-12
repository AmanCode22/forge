# Forge

<img src="forge_logo.png" alt="Forge Logo" width="500">

**The package manager for Ethos.**

Install Traits. Manage dependencies. Stay out of your way.

Forge is how you extend Ethos. It installs **Soft Traits** (Python packages from PyPI or local files) and **Hard Traits** (compiled native binaries) into your Ethos environment and manages them from the command line.

I'm building this alongside Ethos as part of the same solo project. Class 9 student from India.

---

## Installation

### Windows

A combined installer for both **Forge and Ethos** is on the [ethos-lang releases page](https://github.com/AmanCode22/ethos-lang/releases). That's the recommended way — sets up both tools in one shot. There's also a standalone compiled `.exe` for Forge only on the [Forge releases page](https://github.com/AmanCode22/forge/releases).

### macOS

A combined `.pkg` installer for both **Ethos and Forge** is on the [ethos-lang releases page](https://github.com/AmanCode22/ethos-lang/releases). There is no separate Forge `.pkg` — they ship together. One package installs both tools and adds them to your PATH.

See [MACOS_INSTALL.md](MACOS_INSTALL.md) for manual install, build from source, and DarlingHQ instructions.

### Linux

See [LINUX_INSTALL.md](LINUX_INSTALL.md) for all options — OBS repos, AUR, and the universal tarball.

> Installing `ethos-forge` via a Linux package manager will pull in `ethos-lang` automatically as a hard dependency. You don't need to install Ethos first.

### Android via Termux
Nuitka builds on termux are not supported due to restrictions and linker issue so ethos in termux requires python and is just a wrapper to run python source code compressed using zipapp. After rust rewrite the termux prebuilt binaries would be provided till then .deb file and termux pkg integration is just done. Supported after v0.5.0 beta.
You can also add repo of ethos in termux.
#### By downlaoading debs
Run after downloading the deb file manually or using wget or curl
```bash
pkg update && pkg upgrade
pkg install python
pkg install ./termux-deb-path-here-which-you-downloaded.deb
```
#### By adding repo
Run
```
echo "deb [trusted=yes] https://amancode22.github.io/ethos-termux-repo/repo termux extras" >> $PREFIX/etc/apt/sources.list.d/ethos-local.list
pkg update
pkg install ethos-lang-termux ethos-forge-termux
```
### From source

Python 3.10+, no extra dependencies beyond the standard library.

```bash
git clone https://github.com/AmanCode22/forge.git
cd forge
python main.py --help
```

---

## Quick concepts

**Soft Trait** — a Python package installed from PyPI or a local file. Use it in Ethos with `bring in`. Lives in `~/.ethos/traits/`.

**Hard Trait** — a compiled shared library (C, C++, Rust, or anything with a C-compatible ABI), packaged as a zip with a `manifest.json`. Loads automatically when Ethos starts. Lives in `~/.ethos/traits/hard_traits/<n>/`. Its SDK and more information can be found at foundry [github.com/amancode22/ethos-foundry](https://github.com/amancode22/ethos-foundry)

---

## Output prefixes

| Prefix | Means |
|--------|-------|
| `[*]`  | in progress |
| `[+]`  | success |
| `[-]`  | something went wrong |

---

## Commands

```bash
forge --version
forge -v
```

### Soft Traits

Install from PyPI:

```bash
forge pymodule get requests
```

Forge queries the PyPI JSON API, picks the best wheel for your platform (platform-specific first, then pure-Python `any`, then sdist fallback), downloads it, and extracts into `~/.ethos/traits/`.

Install from a remote wheel URL:

```bash
forge pymodule wheel get <url>
```

Install from a local `.whl` file:

```bash
forge pymodule wheel local <path>
```

Install from a remote sdist tarball:

```bash
forge pymodule sdist get <url>
```

Install from a local `.tar.gz` sdist:

```bash
forge pymodule sdist local <path>
```

### Hard Traits

Install from a URL:

```bash
forge get <url>
```

Forge downloads the zip, finds `manifest.json` at any depth, validates `name` and `binary`, and moves the trait folder into `~/.ethos/traits/hard_traits/<n>/`.

Install from a local zip:

```bash
forge local <path>
```
### Ethos Foundry support

Searching a hard trait in ethos-foundry
```bash
forge foundry search greetc
```

Installing a trait from foundry
```bash
forge foundry get greetc
```

### Listing installed traits

```bash
forge list             # everything
forge list pymodule    # Soft Traits only
forge list native      # Hard Traits only
```

### Removing traits

```bash
forge remove <trait-name>         # Hard Trait
forge remove pymodule <package>   # Soft Trait
```

---

## How Soft Trait installation works

Forge never runs install scripts — it only extracts the archive. Platform detection works by reading `sysconfig.get_platform()` and matching against wheel filenames. For a package to be importable, its top-level module folder must land directly inside `~/.ethos/traits/` after extraction.

---

## How Hard Trait installation works

Forge unpacks the zip to a temp directory, does a recursive search for `manifest.json`, validates `name` and `binary`, then moves the trait's parent folder into `~/.ethos/traits/hard_traits/<n>/`. Ethos handles the rest at startup — reads the manifest, loads the `.so` with `ctypes.CDLL`, wires up every exported function's signature from the manifest.

---

## Where things live

```
~/.ethos/
└── traits/
    ├── requests/           ← Soft Trait (Python package)
    ├── numpy/              ← Soft Trait
    └── hard_traits/
        └── mymath/         ← Hard Trait
            ├── manifest.json
            └── mymath.so
```

---

## Error reference

| Message | What happened |
|---|---|
| `[-] This package does not exist or its a network error/pypi might be blocked` | PyPI lookup failed or wrong package name |
| `[-] Cannot get results from pypi...` | PyPI response couldn't be decoded |
| `[-] This package doesnt support your system and its tar sdist isnt published` | No compatible wheel or sdist for your platform |
| `[-] Invalid Hard Trait: No manifest.json found` | The zip has no `manifest.json` anywhere inside it |
| `[-] Trait cannot be installed due to invalid manifest.json.` | Manifest missing `name` or `binary` |
| `[-] Failed to remove. Soft trait <n> is not installed.` | Folder not in `~/.ethos/traits/` |
| `[-] Failed to remove. Hard trait <n> is not installed.` | Folder not in `~/.ethos/traits/hard_traits/` |

---

## What's next

- Eventually: rewrite core in C, C++, or Rust to drop the Python dependency entirely

---

## Contributing

Solo project but PRs are welcome — especially Hard Trait SDK support for languages other than C/C++ and Rust. Bug reports and fixes always appreciated.

Build instructions: [BUILDING.md](BUILDING.md)
Linux installation: [LINUX_INSTALL.md](LINUX_INSTALL.md)
macOS installation: [MACOS_INSTALL.md](MACOS_INSTALL.md)

---

## Related

- Ethos (the language) → [github.com/AmanCode22/ethos-lang](https://github.com/AmanCode22/ethos-lang)
- ethos-builder (build scripts, packaging) → [github.com/AmanCode22/ethos-builder](https://github.com/AmanCode22/ethos-builder)
- Ethos Foundry (Collection of hard traits): [github.com/amancode22/ethos-foundry](github.com/amancode22/ethos-foundry)

The combined Windows and macOS installers for both Forge and Ethos are in the [ethos-lang releases](https://github.com/AmanCode22/ethos-lang/releases).

---

## License

GPL-3.0. See [LICENSE](LICENSE).

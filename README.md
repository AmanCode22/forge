# Forge

![Forge Logo](forge_logo.png)

**The package manager for Ethos.**

Install Traits. Manage dependencies. Stay out of your way.

Forge is how you extend Ethos. It installs **Soft Traits** (Python packages from PyPI or local files) and **Hard Traits** (compiled native binaries) into your Ethos environment and manages them from the command line.

I'm building this alongside Ethos as part of the same solo project.

---

## Installation

### Windows

A combined installer for both **Forge and Ethos** lives in the [ethos-lang releases](https://github.com/amancode22/ethos-lang/releases). That's the recommended way — it sets up both tools in one step. There's also a standalone compiled `.exe` for Forge in the [Forge releases](https://github.com/amancode22/forge/releases).

### Linux (pre-built binary)

```bash
chmod +x forge
sudo mv forge /usr/local/bin/
```

Linux package builds are coming soon — `.tar.gz` with a compiler and `install.sh`, COPR, PPA, and AUR (both PKGBUILD and a pre-compiled binary package).

### From source

Python 3.10+, no extra dependencies.

```bash
git clone https://github.com/amancode22/forge.git
cd forge
python main.py --help
```

---

## Quick concepts

**Soft Trait** — a Python package, installed from PyPI or a local file. Use it in Ethos with `bring in`. Lives in `~/.ethos/traits/`.

**Hard Trait** — a compiled shared library (C, C++, Rust, or anything with a C-compatible ABI), packaged as a zip with a `manifest.json`. Loads automatically when Ethos starts. Lives in `~/.ethos/traits/hard_traits/<name>/`.

---

## Output prefixes

| Prefix | Means |
|--------|-------|
| `[*]`  | info / in progress |
| `[+]`  | success |
| `[-]`  | something went wrong |

---

## Commands

```bash
forge --version
forge -v
```

### Soft Traits

**Install from PyPI** — Forge queries the PyPI JSON API, selects the best wheel for your platform (platform-specific wheel first, then pure-Python `any` wheel, then sdist fallback), downloads it, and extracts into `~/.ethos/traits/`:

```bash
forge pymodule get <package>
forge pymodule get requests
```

**Install from a remote wheel URL:**

```bash
forge pymodule wheel get <url>
```

**Install from a local `.whl` file:**

```bash
forge pymodule wheel local <path>
```

**Install from a remote sdist tarball:**

```bash
forge pymodule sdist get <url>
```

**Install from a local `.tar.gz` sdist:**

```bash
forge pymodule sdist local <path>
```

---

### Hard Traits

**Install from a URL** — downloads the zip, searches it for `manifest.json` at any depth, validates that `name` and `binary` are present, then moves the trait folder into `~/.ethos/traits/hard_traits/<name>/`:

```bash
forge get <url>
```

**Install from a local zip:**

```bash
forge local <path>
```

---

### Listing installed traits

```bash
forge list             # everything (Soft and Hard Traits)
forge list pymodule    # Soft Traits only
forge list native      # Hard Traits only
```

---

### Removing traits

```bash
forge remove <trait-name>         # remove a Hard Trait by folder name
forge remove pymodule <package>   # remove a Soft Trait by folder name
```

---

## How Soft Trait installation works

Forge never runs install scripts. It only extracts the archive. The platform detection works by reading `sysconfig.get_platform()` and matching that tag against wheel filenames. If no matching wheel is found, it falls back to the sdist `.tar.gz`. For a package to be importable after installation, its top-level module folder must land directly inside `~/.ethos/traits/`.

---

## How Hard Trait installation works

Forge unpacks the zip into a temp directory, does a recursive search for `manifest.json`, validates that `name` and `binary` fields exist, then moves the trait's parent folder into `~/.ethos/traits/hard_traits/<name>/`. The Ethos runtime handles the rest at startup — it reads the manifest, loads the `.so` with `ctypes.CDLL`, and wires up every exported function's signature.

---

## Where things live

```
~/.ethos/
└── traits/
    ├── requests/           <- Soft Trait (Python package)
    ├── numpy/              <- Soft Trait
    └── hard_traits/
        └── mymath/         <- Hard Trait
            ├── manifest.json
            └── mymath.so
```

---

## Error reference

| Message | What happened |
|---|---|
| `[-] This package does not exist or its a network error/pypi might be blocked` | PyPI lookup failed or the package name is wrong. |
| `[-] Cannot get results from pypi...` | PyPI response couldn't be decoded. |
| `[-] This package doesnt support your system and its tar sdist isnt published` | No compatible wheel or sdist for your platform. |
| `[-] Invalid Hard Trait: No manifest.json found` | The zip doesn't contain a `manifest.json` anywhere inside it. |
| `[-] Trait cannot be installed due to invalid manifest.json.` | Manifest is missing `name` or `binary`. |
| `[-] Failed to remove. Soft trait <n> is not installed.` | Folder not found in `~/.ethos/traits/`. |
| `[-] Failed to remove. Hard trait <n> is not installed.` | Folder not found in `~/.ethos/traits/hard_traits/`. |

---

## What's next

- Linux `.tar.gz` (compiler + install.sh), COPR, PPA, and AUR with pre-compiled package
- macOS support
- `forge update` — update an installed Soft Trait to latest
- Hard Trait SDK for C/C++ and Rust
- Eventually: rewrite core in C, C++, or Rust to drop the Python dependency entirely

---

## Contributing

Solo project but PRs are welcome — especially Hard Trait SDK support for languages other than C/C++ and Rust. Bug reports and fixes are always appreciated.

Build instructions: [BUILDING.md](BUILDING.md).

## Related

The combined Windows installer for both Forge and Ethos lives in the [ethos-lang releases](https://github.com/amancode22/ethos-lang/releases).

Ethos itself: [github.com/amancode22/ethos-lang](https://github.com/amancode22/ethos-lang)

---

## License

GPL-3.0. See [LICENSE](LICENSE).

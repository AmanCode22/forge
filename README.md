
# Forge

**The package manager for Ethos.**

*Install Traits. Manage dependencies. Stay out of your way.*



---

Forge is how you extend Ethos. It installs **Soft Traits** (Python packages) and **Hard Traits** (compiled native binaries) into your Ethos environment and manages them from the command line.

> Built by [Aman Adlakha](https://github.com/amancode22) — a Class 9 student from India, doing this solo.

---

## Quick concepts

**Soft Trait** — a Python package, installed from PyPI or a local file. Use it in Ethos with `bring in`.

**Hard Trait** — a compiled shared library (C, C++, Rust, or anything with a C-compatible ABI), packaged as a zip with a `manifest.json`. Loads automatically when Ethos starts.

---

## Installation

### Linux (pre-built binary)

```bash
chmod +x forge
sudo mv forge /usr/local/bin/
```

> Windows, macOS, Android (Termux), and native Linux packages (`.deb`, `.rpm`, AUR) are on the roadmap.

### From source

Python 3.10+, no extra dependencies.

```bash
git clone https://github.com/amancode22/forge.git
cd forge
python main.py --help
```

---

## Commands

Output prefixes:

| Prefix | Means |
|--------|-------|
| `[*]`  | info / in progress |
| `[+]`  | success |
| `[-]`  | something went wrong |

---

### Soft Traits

#### From PyPI

```bash
forge pymodule get <package>
```

Forge hits the PyPI API, picks the best wheel for your system (platform wheel → pure Python wheel → sdist fallback), downloads it, extracts it. Done.

```bash
forge pymodule get requests
```

#### From a remote wheel URL

```bash
forge pymodule wheel get <url>
```

#### From a local wheel file

```bash
forge pymodule wheel local <path>
```

#### From a remote sdist tarball

```bash
forge pymodule sdist get <url>
```

#### From a local sdist tarball

```bash
forge pymodule sdist local <path>
```

---

### Hard Traits

#### From a URL

```bash
forge get <url>
```

Downloads the zip, validates the manifest, installs the trait.

#### From a local zip

```bash
forge local <path>
```

---

### Listing what's installed

```bash
forge list             # everything
forge list pymodule    # soft traits only
forge list native      # hard traits only
```

---

### Removing things

```bash
forge remove <trait-name>            # remove a hard trait
forge remove pymodule <package>      # remove a soft trait
```

---

## Where things live

```
~/.ethos/
└── traits/
    ├── requests/        ← soft trait
    ├── numpy/           ← soft trait
    └── hard_traits/
        └── mymath/      ← hard trait
            ├── manifest.json
            └── mymath.so
```

---

## What's next

- [ ] Windows `.msi` installer
- [ ] macOS `.pkg` installer
- [ ] Linux: `.deb`, `.rpm`, AUR
- [ ] Android via Termux
- [ ] Eventually: rewrite core in C, C++, or Rust to drop the Python dependency entirely

---

## Contributing

Solo project, but PRs are welcome — especially Hard Trait SDK support for languages other than C/C++ and Rust. Bug reports and fixes are always appreciated too.

For instructions on building yourself refer to [BUILDING.md](BUILDING.md).
---

## License

GPL-3.0. See [LICENSE](LICENSE).

---

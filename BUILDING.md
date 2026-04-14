# Building forge

## Prerequisites

- Python 3.10 or newer (with pip)
- Git (or download the repo zip and extract it yourself)

---

## Linux

Install the packages Nuitka needs for your distro:

**Ubuntu / Debian and derivatives**
```bash
sudo apt update
sudo apt install python3 python3-dev build-essential patchelf
```

**Fedora / RHEL and derivatives**
```bash
sudo dnf install python3 python3-devel gcc gcc-c++ patchelf
```

**Arch Linux / Manjaro and derivatives**
```bash
sudo pacman -S python base-devel patchelf
```

Then build:

```bash
git clone https://github.com/AmanCode22/forge
cd forge/
python3 -m venv forge_build_env
./forge_build_env/bin/pip install -r requirements.txt
mkdir binary/
unset LDFLAGS
./forge_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/forge main.py
```

The compiled binary lands in `binary/forge`.

> `--unstripped` is important — without it the environment may strip the binary after Nuitka builds it, which destroys the self-extracting payload and causes a `couldn't find attached data header` error at runtime.

---

## Windows

Open PowerShell in the source directory:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
python -m nuitka --assume-yes-for-downloads --onefile main.py --output-filename=forge.exe
```

You get `forge.exe` in the current folder.

---

## macOS

You need Python 3.10+ and the Xcode command line tools:

```bash
xcode-select --install
```

Then install Nuitka's dependencies via Homebrew:

```bash
brew install python@3.12 ccache
```

### Native build (build for the architecture you're running on)

Works on both Apple Silicon (arm64) and Intel (x86_64):

```bash
git clone https://github.com/AmanCode22/forge
cd forge/
python3 -m venv forge_build_env
./forge_build_env/bin/pip install -r requirements.txt
mkdir binary/
./forge_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/forge main.py
```

This produces a binary for the architecture you're currently running.

### Building a Universal Binary (arm64 + x86_64 in one file)

Build both architectures separately and combine with `lipo`.

**Step 1 — arm64 binary** (on Apple Silicon):

```bash
arch -arm64 ./forge_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/forge-arm64 main.py
```

**Step 2 — x86_64 binary** (on Intel, or Apple Silicon using Rosetta):

```bash
arch -x86_64 /usr/bin/python3 -m venv forge_build_env_x86
arch -x86_64 ./forge_build_env_x86/bin/pip install -r requirements.txt
arch -x86_64 ./forge_build_env_x86/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/forge-x86_64 main.py
```

**Step 3 — combine:**

```bash
lipo -create binary/forge-arm64 binary/forge-x86_64 -output binary/forge
```

**Verify:**

```bash
file binary/forge
lipo -info binary/forge
```

### Building x86_64 on x86_64 (Intel Mac)

Run the native build above on an Intel Mac. No extra flags needed.

### Building arm64 on arm64 (Apple Silicon)

Run the native build above on an Apple Silicon Mac. No extra flags needed.

### Cross-compiling x86_64 on Apple Silicon (Rosetta)

```bash
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
arch -x86_64 /usr/local/bin/brew install python@3.12

arch -x86_64 /usr/local/bin/python3.12 -m venv forge_build_env_x86
arch -x86_64 ./forge_build_env_x86/bin/pip install -r requirements.txt
arch -x86_64 ./forge_build_env_x86/bin/python3 -m nuitka --standalone --unstripped  -o binary/forge-x86_64 main.py
```

### Building the combined .pkg installer for macOS

The `.pkg` installer ships both `ethos` and `forge` together. There is no separate Forge `.pkg`. You need both binaries built first — either from source or by downloading the pre-built binaries from the [releases page](https://github.com/AmanCode22/ethos-lang/releases) and [Forge releases page](https://github.com/AmanCode22/forge/releases).

```bash
mkdir -p pkg_root/usr/local/bin
cp binary/forge pkg_root/usr/local/bin/forge
cp /path/to/ethos/binary/ethos pkg_root/usr/local/bin/ethos
chmod +x pkg_root/usr/local/bin/forge
chmod +x pkg_root/usr/local/bin/ethos

pkgbuild \
  --root pkg_root \
  --identifier com.amancode22.ethos \
  --version 0.3.0 \
  --install-location / \
  ethos-component.pkg

productbuild \
  --component ethos-component.pkg /usr/local \
  --identifier com.amancode22.ethos \
  --version 0.3.0 \
  Ethos-v0.3.0-macos.pkg
```

The resulting `Ethos-v0.3.0-macos.pkg` installs both `ethos` and `forge` to `/usr/local/bin/`.

### Using DarlingHQ (running macOS Forge binary on Linux)

[Darling](https://www.darlinghq.org/) lets you run macOS binaries on Linux. To run the macOS Forge binary:

```bash
# Install Darling — see https://docs.darlinghq.org/installation.html

darling shell

# Inside the Darling shell
forge --version
forge pymodule get requests
```

Build the macOS binary on a real Mac. Use Darling only for running it on Linux.

---

## Android (Termux)

Just zipapps due to linker issue so no build required

---
For packaging scripts, OBS spec files, Debian control files, and the Windows installer, see [ethos-builder](https://github.com/AmanCode22/ethos-builder).

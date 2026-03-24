# Building forge

## Prerequisites

- Python 3.10 or newer (with pip)
- Git (or download the repo zip and extract it yourself)

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
./forge_build_env/bin/python3 -m nuitka --standalone --onefile --onefile-no-strip -o binary/forge main.py
```

The compiled binary lands in `binary/forge`. Run it with `./binary/forge`.

> `--onefile-no-strip` is important — without it the environment may strip the binary after Nuitka builds it, which destroys the self-extracting payload and causes a `couldn't find attached data header` error at runtime.

## Windows

Open PowerShell in the source directory:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
python -m nuitka --assume-yes-for-downloads --onefile main.py --output-filename=forge.exe
```

You get `forge.exe` in the current folder.

## macOS

Coming soon.

## Android (Termux)

On the roadmap after the project hits stable release.

---

For packaging scripts, OBS spec files, Debian control files, and the Windows installer, see [ethos-builder](https://github.com/AmanCode22/ethos-builder).

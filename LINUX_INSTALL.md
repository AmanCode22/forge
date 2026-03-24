# Installing Forge on Linux

The binary on the [releases page](https://github.com/AmanCode22/forge/releases) is a standalone compiled executable — no Python required to run it.

> Installing `ethos-forge` via any Linux package manager will pull in `ethos-lang` automatically as a hard dependency. You don't need to install Ethos first — it comes along.

---

## Option 1 — OBS Repository

Click the link, pick your distro, and the page shows you the exact commands to add the repo and install:

🔗 [Add repository and install ethos-forge](https://software.opensuse.org/download.html?project=home:AmanCode22&package=ethos-forge)

**Supported distros**

| Distribution | Architectures |
|---|---|
| openSUSE Leap 15.6 | x86_64 |
| Arch Linux | x86_64 |
| Debian 12 | i586, x86_64 |
| Debian 13 | x86_64 |
| Debian Unstable | x86_64 |
| Fedora 42 | aarch64, x86_64 |
| Fedora 43 | aarch64, x86_64 |
| Fedora Rawhide | x86_64 |
| openEuler 24.03 | aarch64, x86_64 |
| openSUSE Factory ARM | aarch64, armv7l |
| openSUSE Slowroll | i586, x86_64 |
| openSUSE Tumbleweed | i586, x86_64 |
| Ubuntu 24.04 | x86_64 |
| Ubuntu 25.04 | x86_64 |
| Ubuntu 25.10 | x86_64 |

> `ethos-forge` declares `ethos-lang` as a hard dependency. Your package manager pulls it in automatically.

---

## Option 2 — AUR (Arch Linux)

Builds from source using Nuitka. The AUR package for `ethos-forge` depends on `ethos-lang`, so both get installed together.

🔗 [AUR: ethos-forge](https://aur.archlinux.org/packages/ethos-forge)

```bash
# yay
yay -S ethos-forge

# paru
paru -S ethos-forge

# manually
git clone https://aur.archlinux.org/ethos-forge.git
cd ethos-forge
makepkg -si
```

---

## Option 3 — Universal Tarball

The tarball on the [ethos-lang releases page](https://github.com/AmanCode22/ethos-lang/releases) ships **both ethos and forge** as pre-compiled binaries. There is no separate Forge tarball — they are bundled together.

Download `ethos-build.tar.gz` from the [ethos-lang releases page](https://github.com/AmanCode22/ethos-lang/releases), then:

```bash
tar -xzf ethos-build.tar.gz
cd ethos-build
chmod +x install.sh
sudo ./install.sh
```

Running with `sudo` copies both `ethos` and `forge` to `/usr/local/bin/`.

Running **without** `sudo` triggers a prompt asking if you want a local install instead — binaries go to `~/bin/` and the installer adds it to your PATH in `.bashrc`.

---

## Verify

```bash
forge --version
```

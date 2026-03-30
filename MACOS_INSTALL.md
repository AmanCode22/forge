# Installing Forge on macOS

The pre-built binary on the [releases page](https://github.com/AmanCode22/forge/releases) is a standalone compiled executable — no Python required to run it.

---

## Option 1 — .pkg Installer (recommended)

The `.pkg` on the [ethos-lang releases page](https://github.com/AmanCode22/ethos-lang/releases) installs both **Ethos and Forge** in one shot. There is no separate Forge `.pkg` — they ship together.

Download pkg file for your architecture and double-click it. The installer copies `ethos` and `forge` to `/usr/local/bin/` and they're immediately available in your terminal.

---

## Option 2 — Manual install from pre-built binary

Download the standalone `forge` binary from the [releases page](https://github.com/AmanCode22/forge/releases), then:

```bash
chmod +x forge
sudo mv forge /usr/local/bin/forge
```

You'll also want Ethos — download it from the [ethos-lang releases page](https://github.com/AmanCode22/ethos-lang/releases):

```bash
chmod +x ethos
sudo mv ethos /usr/local/bin/ethos
```

Verify:

```bash
forge --version
ethos --version
```

---

## Option 3 — Build from source

See [BUILDING.md](BUILDING.md) for the full build instructions including native builds, universal binaries, cross-compilation via Rosetta, and how to produce the `.pkg` installer yourself.

---

## DarlingHQ (running macOS Forge binary on Linux)

[Darling](https://www.darlinghq.org/) is a macOS compatibility layer for Linux. To run the macOS Forge binary on Linux:

```bash
# Install Darling — see https://docs.darlinghq.org/installation.html

darling shell

# Inside Darling
forge --version
forge pymodule get requests
```

Build the macOS binary on a real Mac. Use Darling only for running it on Linux. See [BUILDING.md](BUILDING.md) for build steps.

---

## Verify

```bash
forge --version
```

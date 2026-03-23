# Building
## Prerequisites
- Python3.10+(with pip installed) in path
- Git installed(Or you can download the repo zip also)
## Building on linux
You must install the basic developement packages reqiured by nuitka to build ethos according to your distro
- Ubuntu/Debian and derrivatives
```
sudo apt update
sudo apt install python3 python3-dev build-essential patchelf
```
- Fedora/RHEL and derrivaties
```
sudo dnf install python3 python3-devel gcc gcc-c++ patchelf
```
- Arch Linux/Manjaro and derrivaties
```
sudo pacman -S python base-devel patchelf
```

After this you can build using given commands
```
git clone https://github.com/amancode22/forge # you can  skip this if you have zip(you must extract it yourself)
cd forge/
python3 -m venv forge_build_env
./forge_build_env/bin/pip install -r requirements.txt
mkdir binary/
./forge_build_env/bin/python3 -m nuitka --standalone --onefile -o binary/forge main.py
```
After this completes you would have a compiled binary of forge in binary folder.
You can use it typing  ```./binary/forge``` in terminal.
## Building on Windows
Open powershell and change directory to where you downloaded source
```
pip install --upgrade pip
pip install -r requirements.txt
python -m nuitka --assume-yes-for-downloads --onefile main.py --output-filename=forge.exe
```
You can use forge.exe now!
## Building on Macos
Would be added soon.
## Building on Android(Termux)
Termux support is currently in future roadmap and would be added after project reaches stable release.

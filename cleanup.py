import shutil
from pathlib import Path

traits_path = Path.home() / ".ethos" / "traits"
hard_traits_path = traits_path / "hard_traits"


def handle_remove_pymodule(name):
    print("[*] Trying to remove soft trait......")
    target = traits_path / name
    if target.exists():
        shutil.rmtree(target)
        print("[+] Soft Trait removed successfully.")
    else:
        print(f"[-] Failed to remove. Soft trait {name} is not installed.")


def handle_remove_native(name):
    print("[*] Trying to remove hard trait.....")
    target = hard_traits_path / name
    if target.exists():
        shutil.rmtree(target)
        print("[+] Hard Trait removed successfully.")
    else:
        print(f"[-] Failed to remove. Hard trait {name} is not installed.")

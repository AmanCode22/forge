import shutil
from pathlib import Path

traits_path = Path.home() / ".ethos" / "traits"
hard_traits_path = traits_path / "hard_traits"


def handle_remove_pymodule(args):
    target = traits_path / args.name
    if target.exists():
        shutil.rmtree(target)
        print("Soft Trait removed successfully.")


def handle_remove_native(args):
    target = hard_traits_path / args.name
    if target.exists():
        shutil.rmtree(target)
        print("Hard Trait removed successfully.")

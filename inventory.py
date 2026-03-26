from pathlib import Path

traits_path = Path.home() / ".ethos" / "traits"
hard_traits_path = traits_path / "hard_traits"


def handle_list_pymodule(args):
    for i in traits_path.iterdir():
        if not i.is_dir() or i.name == "hard_traits":
            continue
        if i.name.endswith(".dist-info"):
            continue
        if i.name == "__pycache__":
            continue
        print(f"[*] {i.name} (Soft Trait)")


def handle_list_native(args):
    for i in hard_traits_path.iterdir():
        if not i.is_dir():
            continue
        print(f"[*] {i.name} (Hard Trait)")


def handle_list(args):
    handle_list_pymodule(args)
    handle_list_native(args)

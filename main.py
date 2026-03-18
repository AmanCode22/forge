import argparse
import sys
from pymodule import handle_get, handle_wheel_get, handle_wheel_local, handle_sdist_get, handle_sdist_local
from hard_trait import handle_native_get, handle_native_local
from inventory import handle_list, handle_list_pymodule, handle_list_native
from cleanup import handle_remove_native, handle_remove_pymodule

def main():
    parser = argparse.ArgumentParser(
        prog="forge", 
        description="Ethos programming language's package manager."
    )
    subparsers = parser.add_subparsers(dest="main_command", required=True)

    pymodule_parser = subparsers.add_parser("pymodule", help="Manage Python-based traits.")
    pymodule_sub = pymodule_parser.add_subparsers(dest="py_action", required=True)

    # forge pymodule get <name>
    py_get = pymodule_sub.add_parser("get", help="Standard PyPI fetcher.")
    py_get.add_argument("module_name")
    py_get.set_defaults(func=handle_get)

    # forge pymodule wheel ...
    wheel_parser = pymodule_sub.add_parser("wheel", help="Direct wheel management.")
    wheel_sub = wheel_parser.add_subparsers(dest="wheel_action", required=True)
    w_get = wheel_sub.add_parser("get", help="Download wheel from URL.")
    w_get.add_argument("url")
    w_get.set_defaults(func=handle_wheel_get)
    w_local = wheel_sub.add_parser("local", help="Install local wheel file.")
    w_local.add_argument("path")
    w_local.set_defaults(func=handle_wheel_local)

    # forge pymodule sdist ...
    sdist_parser = pymodule_sub.add_parser("sdist", help="Source distribution management.")
    sdist_sub = sdist_parser.add_subparsers(dest="sdist_action", required=True)
    s_get = sdist_sub.add_parser("get", help="Download and build from URL.")
    s_get.add_argument("url")
    s_get.set_defaults(func=handle_sdist_get)
    s_local = sdist_sub.add_parser("local", help="Build from local source path.")
    s_local.add_argument("path")
    s_local.set_defaults(func=handle_sdist_local)

    # forge get <url>
    native_get = subparsers.add_parser("get", help="Download native binary (Hard Trait).")
    native_get.add_argument("url")
    native_get.set_defaults(func=handle_native_get)

    # forge local <path>
    native_local = subparsers.add_parser("local", help="Register local binary.")
    native_local.add_argument("path")
    native_local.set_defaults(func=handle_native_local)


    # forge list, forge list pymodule, forge list native
    list_parser = subparsers.add_parser("list", help="List installed traits.")
    list_parser.set_defaults(func=handle_list) # Default action
    list_sub = list_parser.add_subparsers(dest="list_type")
    
    l_py = list_sub.add_parser("pymodule", help="List only soft traits.")
    l_py.set_defaults(func=handle_list_pymodule)
    
    l_nat = list_sub.add_parser("native", help="List only hard traits.")
    l_nat.set_defaults(func=handle_list_native)

    # forge remove <name>, forge remove pymodule <name>
    remove_parser = subparsers.add_parser("remove", help="Remove traits.")
    remove_parser.add_argument("name", nargs="?", help="Name of native trait to remove.")
    remove_parser.set_defaults(func=handle_remove_native)
    
    remove_sub = remove_parser.add_subparsers(dest="remove_action")
    r_py = remove_sub.add_parser("pymodule", help="Remove a soft trait folder.")
    r_py.add_argument("name")
    r_py.set_defaults(func=handle_remove_pymodule)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
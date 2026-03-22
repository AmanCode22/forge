import argparse
import sys

from cleanup import handle_remove_native, handle_remove_pymodule
from hard_trait import handle_native_get, handle_native_local
from inventory import handle_list, handle_list_native, handle_list_pymodule
from pymodule import (
    handle_get,
    handle_sdist_get,
    handle_sdist_local,
    handle_wheel_get,
    handle_wheel_local,
)
from version import stage, version


def main():
    parser = argparse.ArgumentParser(
        prog="forge",
        description="The official package manager for the Ethos programming language.",
        epilog="""Examples:
          forge pymodule get requests                   # Install a soft trait from PyPI
          forge get https://example.com/math_trait.zip  # Install a native hard trait
          forge list                                    # View all installed traits
          forge remove pymodule requests                # Uninstall a specific soft trait""",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"Forge {version} {stage}"
    )
    subparsers = parser.add_subparsers(dest="main_command", required=True)

    pymodule_parser = subparsers.add_parser(
        "pymodule", help="Manage Python-based dependencies (Soft Traits)."
    )
    pymodule_sub = pymodule_parser.add_subparsers(dest="py_action", required=True)

    # forge pymodule get <name>
    py_get = pymodule_sub.add_parser(
        "get",
        help="Fetch and install a Soft Trait directly from the PyPI registry.",
        epilog="""Example:
        forge pymodule get requests""",
    )
    py_get.add_argument("module_name")
    py_get.set_defaults(func=handle_get)

    # forge pymodule wheel ...
    wheel_parser = pymodule_sub.add_parser(
        "wheel", help="Install python wheel directly as soft traits."
    )
    wheel_sub = wheel_parser.add_subparsers(dest="wheel_action", required=True)
    w_get = wheel_sub.add_parser(
        "get",
        help="Download and install a pre-compiled Python .whl package from a remote URL.",
        epilog="""Example:
        forge pymodule wheel get <url to wheel>""",
    )
    w_get.add_argument("url")
    w_get.set_defaults(func=handle_wheel_get)
    w_local = wheel_sub.add_parser(
        "local",
        help="Install a Soft Trait from a local .whl file on your system.",
        epilog="""Example:
        forge pymodule wheel local <path to local wheel file>""",
    )
    w_local.add_argument("path")
    w_local.set_defaults(func=handle_wheel_local)

    # forge pymodule sdist ...
    sdist_parser = pymodule_sub.add_parser(
        "sdist",
        help="Python packages source tar distribution as soft traits installer.",
    )
    sdist_sub = sdist_parser.add_subparsers(dest="sdist_action", required=True)
    s_get = sdist_sub.add_parser(
        "get",
        help="Download and extract a Python Source Distribution (.tar.gz) from a remote URL.",
        epilog="""Example:
        forge pymodule sdist get <url to sdist tar>""",
    )
    s_get.add_argument("url")
    s_get.set_defaults(func=handle_sdist_get)
    s_local = sdist_sub.add_parser(
        "local",
        help="Extract and install a Soft Trait from a local .tar.gz source file.",
        epilog="""Example:
        forge pymodule sdist local <file to local tar.gz>""",
    )
    s_local.add_argument("path")
    s_local.set_defaults(func=handle_sdist_local)

    # forge get <url>
    native_get = subparsers.add_parser(
        "get",
        help="Download and extract a native binary (Hard Trait) from a remote URL.",
        epilog="""Example:
            forge get <url to native binary's zip>""",
    )
    native_get.add_argument("url")
    native_get.set_defaults(func=handle_native_get)

    # forge local <path>
    native_local = subparsers.add_parser(
        "local",
        help="Extract and install a local zip file containing a Hard Trait.",
        epilog="""Example:
        forge local <path to local zip of hard trait>""",
    )
    native_local.add_argument("path")
    native_local.set_defaults(func=handle_native_local)

    # forge list, forge list pymodule, forge list native
    list_parser = subparsers.add_parser(
        "list",
        help="Display all currently installed Soft and Hard Traits in the Ethos environment.",
        epilog="""Example:
        forge list""",
    )
    list_parser.set_defaults(func=handle_list)  # Default action
    list_sub = list_parser.add_subparsers(dest="list_type")

    l_py = list_sub.add_parser(
        "pymodule",
        help="Display only the installed Python-based Soft Traits.",
        epilog="""Example:
        forge list pymodule""",
    )
    l_py.set_defaults(func=handle_list_pymodule)

    l_nat = list_sub.add_parser(
        "native",
        help="Display only the installed C/C++ Hard Traits.",
        epilog="""Example:
        forge list native""",
    )
    l_nat.set_defaults(func=handle_list_native)

    # forge remove <name>, forge remove pymodule <name>
    remove_parser = subparsers.add_parser(
        "remove",
        help="Uninstall and delete a native Hard Trait by its folder name.",
        epilog="""Example:
        forge remove <hard trait name>""",
    )
    remove_parser.add_argument(
        "name", nargs="?", help="Name of native trait to remove."
    )
    remove_parser.set_defaults(func=handle_remove_native)

    remove_sub = remove_parser.add_subparsers(dest="remove_action")
    r_py = remove_sub.add_parser(
        "pymodule",
        help="Uninstall and delete a Python-based Soft Trait by its folder name.",
        epilog="""Example:
        forge remove pymodule requests""",
    )
    r_py.add_argument("name")
    r_py.set_defaults(func=handle_remove_pymodule)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

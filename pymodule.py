import json
import pathlib
import re
import sysconfig
import tarfile
import tempfile
import urllib.request
import zipfile
from sys import exit


def extract_wheel(file_path):
    traits_path = pathlib.Path.home() / ".ethos" / "traits"
    traits_path.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(traits_path)


def extract_sdist(file_path):
    traits_path = pathlib.Path.home() / ".ethos" / "traits"
    traits_path.mkdir(parents=True, exist_ok=True)
    with tarfile.open(file_path, "r:gz") as tar_ref:
        tar_ref.extractall(traits_path)


def get_os_tags():
    platform_name = sysconfig.get_platform()
    platform_tag = re.sub(r"[-.]", "_", platform_name)
    return platform_tag


def resolve_dependencies(pkg_name, seen=None):
    if seen is None:
        seen = set()

    pkg_name = pkg_name.lower()
    if pkg_name in seen:
        return []

    seen.add(pkg_name)

    try:
        with urllib.request.urlopen(
            f"https://pypi.org/pypi/{pkg_name}/json"
        ) as response:
            data = json.loads(response.read().decode("utf-8"))
    except:
        return [pkg_name]

    requires = data.get("info", {}).get("requires_dist")
    deps_to_install = []

    if requires:
        for req in requires:
            if ";" in req and "extra ==" in req:
                continue

            dep_name = re.split(r"[<>=!~ ();]", req)[0].strip()
            if dep_name:
                deps_to_install.extend(resolve_dependencies(dep_name, seen))

    deps_to_install.append(pkg_name)
    return list(dict.fromkeys(deps_to_install))


def handle_get(args):
    module_name = str(args.module_name)
    print(f"[*] Resolving dependencies for {module_name}....")

    packages_to_install = resolve_dependencies(module_name)
    print(
        f"[*] Found {len(packages_to_install)} packages to install: {', '.join(packages_to_install)}"
    )

    for pkg in packages_to_install:
        print(f"\n[*] Trying to download {pkg} from pypi website....")
        try:
            with urllib.request.urlopen(
                f"https://pypi.org/pypi/{pkg}/json"
            ) as response:
                raw_data = response.read()
                module_json_info = json.loads(raw_data.decode("utf-8"))
        except:
            print(f"[-] Cannot get results from pypi for {pkg}, skipping.")
            continue

        latest_version = module_json_info["info"]["version"]
        latest_release_json = module_json_info["releases"][latest_version]
        download_url = ""
        os_tag = get_os_tags()
        is_wheel = False
        tar_url = ""

        for i in latest_release_json:
            if i["filename"].endswith("any.whl"):
                download_url = i["url"]
                is_wheel = True
                break
            elif os_tag in i["filename"] and i["filename"].endswith(".whl"):
                download_url = i["url"]
                is_wheel = True
                break
            elif i["filename"].endswith(".tar.gz"):
                tar_url = i["url"]

        if download_url == "" and tar_url == "":
            print(
                f"[-] {pkg} doesnt support your system and its tar sdist isnt published. Skipping."
            )
            continue

        with tempfile.TemporaryDirectory() as temp_dir:
            if is_wheel:
                print(f"[*] Found perfect wheel for {pkg}, downloading it.....")
                temp_file = pathlib.Path(temp_dir) / "downloaded_trait"
                urllib.request.urlretrieve(download_url, temp_file)
                print("[*] Wheel downloaded, installing it....")
                extract_wheel(temp_file)
                print(f"[+] Soft trait {pkg} installed successfully.")
            else:
                print(
                    f"[*] No compatible wheel found for {pkg}, trying sdist tar. Downloading sdist....."
                )
                temp_file = pathlib.Path(temp_dir) / "downloaded_trait"
                urllib.request.urlretrieve(tar_url, temp_file)
                print("[*] Downloading done, trying to install it...")
                extract_sdist(temp_file)
                print(f"[+] Soft trait {pkg} installed successfully.")


def handle_wheel_local(args):
    print("[*] Trying to install provided wheel file....")
    extract_wheel(args.path)
    print("[+] Wheel succesfully installed as soft trait.")


def handle_wheel_get(args):
    print("[*] Trying to download wheel from provided url...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = pathlib.Path(temp_dir) / "downloaded_trait"
        urllib.request.urlretrieve(args.url, temp_file)
        print("[*] Wheel downloaded succesfully, installing it....")
        extract_wheel(temp_file)
        print("[+] Wheel succesfully installed as soft trait.")


def handle_sdist_get(args):
    print("[*] Trying to download sdist tar from provided url...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = pathlib.Path(temp_dir) / "downloaded_trait"
        urllib.request.urlretrieve(args.url, temp_file)
        print("[*] Sdist tar downloaded succesfully, installing it....")
        extract_sdist(temp_file)
        print("[+] Sdist tar succesfully installed as soft trait.")


def handle_sdist_local(args):
    print("[*] Trying to install provided sdist tar file....")
    extract_sdist(args.path)
    print("[+] Sdist tar succesfully installed as soft trait.")

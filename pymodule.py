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


def handle_get(args):
    print("[*] Trying to download module from pypi website....")
    module_name = str(args.module_name)
    try:
        with urllib.request.urlopen(
            f"https://pypi.org/pypi/{module_name}/json"
        ) as response:
            raw_data = response.read()
            try:
                module_json_info = json.loads(raw_data.decode("utf-8"))
            except:
                print(
                    "[-] Cannot get results from pypi , check your network or pypi might be blocked."
                )
                exit()
    except:
        print(
            "[-] This package does not exists or its a network error/pypi might be blocked"
        )
        exit()
    latest_version = module_json_info["info"]["version"]
    latest_release_json = module_json_info["releases"][latest_version]
    download_url = ""
    os_tag = get_os_tags()
    is_wheel = False
    tar_url = ""
    print("[*] Choosing best from available wheels and sdist for your system....")
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
            "[-] This package doesnt support your system and its tar sdist isnt published"
        )
        exit()
    with tempfile.TemporaryDirectory() as temp_dir:
        if is_wheel:
            print("[*] Found perfect wheel, downloading it.....")
            temp_file = pathlib.Path(temp_dir) / "downloaded_trait"
            urllib.request.urlretrieve(download_url, temp_file)
            print("[*] Wheel downloaded, installing it....")
            extract_wheel(temp_file)
            print("[+] Soft trait installed successfully.")
        else:
            print(
                "[*] No compatible wheel found, trying sdist tar. Downloading sdist....."
            )
            temp_file = pathlib.Path(temp_dir) / "downloaded_trait"
            urllib.request.urlretrieve(tar_url, temp_file)
            print("[*] Downloading done, trying to install it...")
            extract_sdist(temp_file)
            print("[+] Soft trait installed successfully.")


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

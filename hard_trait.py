import json
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from sys import exit

hard_traits_path = Path.home() / ".ethos" / "traits" / "hard_traits"
hard_traits_path.mkdir(parents=True, exist_ok=True)


def extract_native_zip(file_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            search_result = list(Path(temp_dir).rglob("manifest.json"))
            if not search_result or search_result == []:
                print("[-] Invalid Hard Trait: No manifest.json found")
                exit()
            with open(search_result[0]) as f:
                json_manifest = json.load(f)
            if not ("name" in json_manifest) or not ("binary" in json_manifest):
                print("[-] Trait cannot be installed due to invalid manifest.json.")
                exit()
            trait_name = json_manifest["name"]
            target_folder = hard_traits_path / trait_name
            shutil.move(str(search_result[0].parent), str(target_folder))


def handle_native_local(args):
    print("[*] Unzipping and installing local zip hard trait....")
    extract_native_zip(args.path)
    print("[+] Hard Trait installed succesfully.")


def handle_native_get(args):
    print("[*] Trying to download hard trait zip from given url....")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "downloaded_trait"
        urllib.request.urlretrieve(args.url, temp_file)
        print("[*] Downloaded hard trait zip. Extracting and installing it.....")
        extract_native_zip(temp_file)
        print("[+] Hard trait installed succesfully from the url.")

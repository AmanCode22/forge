import json
import os
import platform
import shutil
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from sys import exit

hard_traits_path = Path.home() / ".ethos" / "traits" / "hard_traits"
hard_traits_path.mkdir(parents=True, exist_ok=True)


def detect_platform():

    system = platform.system().lower()
    if system == "darwin":
        os_name = "macos"
    elif system == "windows":
        os_name = "windows"
    elif system == "linux":
        os_name = "linux"
    elif system=="android":
        os_name="android"
    else:
        os_name = system

    machine = platform.machine().lower()

    if machine in ["x86_64", "amd64"]:
        arch = "x86_64"
    elif machine in ["arm64", "aarch64"]:
        arch = "aarch64"
    elif machine in ["armv7l", "armv8l","arm"]:
        arch = "armv7"
    else:
        arch = machine

    if os_name == "windows" and "arm" in machine:
        arch = "arm64"

    return f"{os_name}-{arch}"


def fetch_api_with_fallback(endpoint):
    primary_url = "https://foundry-ethos.pages.dev/" + endpoint
    fallback_url = "https://amancode22.github.io/ethos-foundry/" + endpoint
    req_primary = urllib.request.Request(
        primary_url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        },
    )
    try:
        with urllib.request.urlopen(req_primary, timeout=20) as response:
            code = response.getcode()
            return response.read().decode("utf-8"), code
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return error_body, e.code
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"Primary URL of foundry failed: {e}. Switching to fallback...")

        try:
            with urllib.request.urlopen(fallback_url, timeout=20) as response:
                code = response.getcode()
                return response.read().decode("utf-8"), code
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            return error_body, e.code
        except Exception as fallback_error:
            return f"Both URLs failed. Last error: {fallback_error}"


def search_trait_foundry(args):
    trait_name = args.query
    try:
        index, code = fetch_api_with_fallback("index.json")
        if code != 200:
            raise Exception(
                f"Result code {code} is not valid, requiring code 200 check your network else report issue."
            )
        index = json.loads(index)
    except Exception as e:
        print(
            f"From foundry got invalid results, error while converting api output to json: {e}"
        )
        exit(1)
    findings = {}
    count = 0
    for i in index["traits"]:
        if not index["traits"][i]["verified"]:
            continue
        if trait_name in i:
            count += 1
            print(
                f"[{count}] {i}\n\tAuthor: {index['traits'][i]['author']}\n\tDescription: {index['traits'][i]['description']}"
            )
        elif trait_name in index["traits"][i]["tags"]:
            count += 1
            print(
                f"[{count}] {i}\n\tAuthor: {index['traits'][i]['author']}\n\tDescription: {index['traits'][i]['description']}"
            )
    if count == 0:
        print("[-] No results found in Ethos Foundry.")
    else:
        print(f"Total Number of Results: {count}")


def install_trait_foundry(args):
    trait_name = args.hardtrait_name
    resp, code = fetch_api_with_fallback("traits/greetc/manifest.json")
    if code == 404:
        print(f"[-] Trait {trait_name} is not found on foundry.")
        exit(1)
    if code == 200:
        try:
            result_json = json.loads(resp)
        except Exception as e:
            print(
                f"Got error while converting foundry response to json check your internet or report issue if a bug, error is: {e}"
            )
            exit(1)
        platform = detect_platform()
        if platform not in result_json["platforms"]:
            print(f"[-] This trait is not built for your platform {platform}.")
            exit(1)
        url = result_json["platforms"][platform]["url"]
        checksum = result_json["platforms"][platform]["checksum"]
        print(f"[*] Found url: {url} for hard trait binary, trying to download it.....")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / url.split("/")[-1]
            urllib.request.urlretrieve(url, temp_file)
            print(
                "[*] Downloaded hard trait binary. Making foundry manifest.json compatible with ethos..."
            )
            manifest_final = {}
            manifest_final["name"] = result_json["name"]
            manifest_final["functions"] = result_json["functions"]
            manifest_final["binary"] = url.split("/")[-1]
            print(
                "[*] Created ethos compatible manifest. Saving manifest.json and hard trait binary also......."
            )
            target_folder = hard_traits_path / trait_name
            target_folder.mkdir(parents=True, exist_ok=True)

            shutil.move(str(temp_file), str(target_folder))
            with open(target_folder / "manifest.json", "w") as f:
                json.dump(manifest_final, f)
            print(f"[+] Hard trait {trait_name} installed succesfully.")

    else:
        print(
            f"[-] Recieved invalid http code {code}, check your internet or report issue."
        )
        exit(1)

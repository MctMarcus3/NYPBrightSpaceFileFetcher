import json
import os
import re
import string

from datetime import datetime 
from json import JSONDecodeError
from os import path
from pathvalidate import sanitize_filename
from tqdm import tqdm

# Some courses have an annoying prefix, we'll ignore it
course_prefix = re.compile("^[^-]+ - ")


def create_filepath(course, path):
    course_name = course["OrgUnit"]["Name"]
    course_name = course_prefix.sub("", course_name)
    return "/".join(
        [sanitize_filename(course_name)] + [sanitize_filename(module["Title"]) for module in path])


def create_filename(item):
    extension = item["Url"].split(".")[-1]
    extension = extension.split("?")[0]
    return sanitize_filename(item["Title"]) + "." + extension


def create_filename_without_extension(item):
    return sanitize_filename(item["Title"])

def download_from_url(brightspace_api, url, filepath, lastModified=None):
    # Parse LastModified to Epoch Timestamp
    parsed_datetime = None
    fsLastModified = None
    if lastModified is not None:
        parsed_datetime = datetime.strptime(lastModified, "%Y-%m-%dT%H:%M:%S.%fZ")
    if path.exists(filepath): 
        fsLastModified = os.path.getmtime(filepath)
        if parsed_datetime is not None and fsLastModified is not None:
            if parsed_datetime > fsLastModified:
                os.rename(filepath, f"{fsLastModified}_{filepath}")
    if not path.exists(filepath):
        # Only download file if it doesn't exist
        os.makedirs("/".join(filepath.split("/")[:-1]), exist_ok=True)
        file_size = int(brightspace_api.session.head(url).headers["Content-Length"])
        with tqdm(
                total=file_size, initial=0,
                unit="B", unit_scale=True, desc="Downloading " + url.split("/")[-1]) as pbar:
            req = brightspace_api.session.get(url, stream=True)
            with(open(filepath, "ab")) as f:
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(1024)
            pbar.update(file_size)
        os.utime(filepath, (datetime.now().timestamp(), round(parsed_datetime.timestamp())))
        return True
    return False

def get_config(config_file):
    try:
        with open(config_file, "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print(f"File {config_file} does not exist")
    except JSONDecodeError:
        print(f"File {config_file} is not a valid json file")
    exit()


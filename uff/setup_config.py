import json
import os

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from uff.brightspace import BrightspaceAPI
from uff.courses import get_courses_list
from uff.ufora_login import get_session


def setup():
    email = inquirer.text(message="What's your email address").execute()
    password = inquirer.secret(message="What's your password").execute()
    otc_secret = inquirer.secret(message="What's your 2FA secret?", default="").execute()
    browser = inquirer.select(message="What's your browser (Used to get cookie from brightspace)?", choices=[
                                                                          "Chrome",
                                                                          "Firefox",
                                                                          "Edge",
                                                                          "Opera",
                                                                          "Chromium"]).execute()
    session = get_session(email, password, otc_secret)
    if session is None:
        print("Invalid login credentials")
        return
    defaultConfigPath = "./config.json" if os.name == "posix" else ".\\config.json"
    defaultDirPath = "../" if os.name == "posix" else "..\\"
    config_file = inquirer.filepath(
        message="Specify config file location",
        default=defaultConfigPath).execute()
    output_directory=inquirer.filepath(
        message="Specify output directory", 
        only_directories=True,  
        default=defaultDirPath).execute()
    brightspace_api=BrightspaceAPI(email, password, otc_secret)
    courses=get_courses_list(brightspace_api)
    selected_courses=inquirer.checkbox(message="Select courses to sync (press enter when ready)",
                                         choices=courses
                                         ).execute()

    course_ids=[courses[course] for course in selected_courses]

    with open(config_file, "w+") as f:
        f.write(json.dumps({
            "output_directory": output_directory,
            "courses": course_ids,
            "credentials": {
                "email": email,
                "password": password,
                "otc_secret": otc_secret,
                "browser": browser
            }
        }, indent=4))
    print("Setup complete!")

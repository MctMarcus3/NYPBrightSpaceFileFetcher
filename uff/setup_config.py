import json
import os

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from uff.brightspace import BrightspaceAPI
from uff.courses import get_courses_list
from uff.ufora_login import get_session


def setup():
    driverless, browser, session = False, False, None
    email, password, otc_secret, session = None, None, None, None
    driverless = inquirer.confirm(message="Driverless Setup without Selerium?", default=False).execute()
    if not driverless: 
        email = inquirer.text(message="What's your email address").execute()
        password = inquirer.secret(message="What's your password").execute()
        otc_secret = inquirer.secret(message="What's your 2FA secret?", default="").execute()
        session = get_session(email, password, otc_secret)
    browserSetup = inquirer.confirm(message="Setup Browser?", default=False).execute()
    if browserSetup:
        browser = inquirer.select(message="What's your browser (Used to get cookie from brightspace)?", choices=[
                                                                          "Chrome",
                                                                          "Firefox",
                                                                          "Edge",
                                                                          "Opera",
                                                                          "Chromium"]).execute()
        inquirer.confirm(message=f"Ensure that you are logged in to {browser}", default=False).execute()
        session = get_session(browser=browser)

    if session is None:
        print("Invalid login credentials/Not logged in to Brightspace LMS")
        return
    defaultConfigPath = "./config.json" if os.name == "posix" else ".\\config.json"
    defaultDirPath = "../" if os.name == "posix" else "..\\"
    config_file = inquirer.filepath(
        message="Specify config file location",
        default=defaultConfigPath).execute()
    output_directory=inquirer.filepath(
        message="Specify output directory", 
        default=defaultDirPath).execute()
    brightspace_api=BrightspaceAPI(email, password, otc_secret, browser)
    courses=get_courses_list(brightspace_api)
    selected_courses=inquirer.checkbox(message="Select courses to sync\nMove - Arrow Keys\nSpace - Select\nEnter - ready",
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

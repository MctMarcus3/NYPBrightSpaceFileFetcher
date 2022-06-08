import os
from urllib.request import Request

import pyotp
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from http.cookiejar import CookieJar
import browser_cookie3
from typing import Optional, Callable


def get_cookie(url: str, default_browser: Optional[str] = None) -> CookieJar or None:
    """
    Attempts to get a User Login Session from a Browser
    """
    urlobj = urlparse(url)
    learn_domain = urlobj.hostname
    print(learn_domain)
    browsers = {
        "chrome": browser_cookie3.chrome,
        "firefox": browser_cookie3.firefox,
        "edge": browser_cookie3.edge,
        "opera": browser_cookie3.opera,
        "chromium": browser_cookie3.chromium,
        "unknown": browser_cookie3.load
    }

    def get_cookies_from_browser(browser_name: str, browser_fn: Callable[..., CookieJar]):
        try:
            print(
                f"Attempting to get cookies for {learn_domain} from browser: {browser_name}")
            ret = browser_fn(domain_name=learn_domain)
            print(f"Grabbed Cookies for \"{learn_domain}\" from browser: {browser_name}")
            if len(ret) == 0:
                return None
            return ret
        except Exception:
            print(f"Failed to Grab Cookies for Browser: {browser_name}")

    if default_browser is not None:
        # Use Provided Arg
        selection = default_browser.lower()
    else:
        return None

    # If Invalid Selection Go Through All Browsers
    if selection is None or browsers.get(selection) is None:
        return None
    else:
        return get_cookies_from_browser(selection, browsers[selection])
    


    
# Selenium Login Sequence
# LOGIN_URL = "https://elosp.ugent.be/welcome"
LOGIN_URL = "https://nyplms.polite.edu.sg/d2l/home"

# LOGIN_BUTTON = "ugent-login-button"
EMAIL_BUTTON = "//input[@type='email' and @name='loginfmt']"
NEXT_BUTTON = "//input[@type='submit' and @value='Next']"
PASSWORD_BUTTON = "//input[@name='passwd']"
SIGN_IN_BUTTON = "//input[@type='submit' and @value='Sign in']"

# OTC_BUTTON = "//input[@name='otc']"
# VERIFY_BUTTON = "//input[@type='submit' and @value='Verify']"

UFORA_TITLE = "Homepage - Nanyang Polytechnic"


def create_session(email, password, otc_secret):
    print("Launching headless browser to login")
    os.environ["WDM_LOG_LEVEL"] = "0"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(LOGIN_URL)
    # driver.find_element(By.ID, LOGIN_BUTTON).click()

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, EMAIL_BUTTON))).send_keys(email)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, NEXT_BUTTON))
    ).click()

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, PASSWORD_BUTTON))).send_keys(password)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, SIGN_IN_BUTTON))
    ).click()

    # otc_button = WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.XPATH, OTC_BUTTON))
    # )
    # totp = pyotp.TOTP(otc_secret)
    # code = totp.now()

    # otc_button.send_keys(code)

    # WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.XPATH, VERIFY_BUTTON))
    # ).click()

    WebDriverWait(driver, 20).until(
        EC.title_is(UFORA_TITLE)
    )
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session


def get_session(email=None, password=None, otc_secret=None, browser=None) -> requests.Session:
    cookiejar = get_cookie(LOGIN_URL, browser)
    session = None
    if cookiejar is None:
        session = create_session(email, password, otc_secret)
    else: 
        session = requests.Session()
        session.cookies = cookiejar
    return session

    

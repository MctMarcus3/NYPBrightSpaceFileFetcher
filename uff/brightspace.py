import traceback

from uff.ufora_login import get_session

ufora = "https://nyplms.polite.edu.sg"
root = f"{ufora}/d2l/api"
lp_root = f"{root}/lp/1.37"
le_root = f"{root}/le/1.62"


class APIError(Exception):
    pass


class BrightspaceAPI:

    def __init__(self, email=None, password=None, otc_secret=None, browser=None):
        self._session = None
        self.email = email
        self.password = password
        self.otc_secret = otc_secret
        self.browser = browser
        try:
            self.session = get_session(
                self.email, self.password, self.otc_secret, self.browser)
        except Exception:
            print(traceback.format_exc())
            raise APIError("No session could be created. Please make sure your credentials are correct")

    @staticmethod
    def from_config(config):
        credentials = config["credentials"]
        return BrightspaceAPI(credentials.get("email"), credentials.get("password"), credentials.get("otc_secret"), browser=credentials.get("browser"))

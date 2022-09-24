from dotenv import load_dotenv
from os import environ


class Env:
    def __init__(self) -> None:
        try:
            load_dotenv()
        except Exception:
            pass
        self.ISERV_URL: str = environ["ISERV_URL"]
        self.ISERV_USERNAME: str = environ["ISERV_USERNAME"]
        self.ISERV_PASSWORD: str = environ["ISERV_PASSWORD"]

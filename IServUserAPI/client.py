import requests


class Client:
    def __init__(self, url: str) -> None:
        self.session = requests.Session()
        self.url = url

    def login(self, username: str, password: str):
        with self.session as s:
            s.post(
                url=self.url + "/iserv/auth/login",
                data=f"_username={username}&_password={password}",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            return s.get(url=self.url + "/iserv")

    def logout(self):
        with self.session as s:
            return s.get(url=self.url + "/iserv/auth/logout")

import requests
import msgpack
from pathlib import Path
import datetime
import base64
from queue import Queue
import os

from flask import Flask, escape, request
import webbrowser

from typing import List, Dict, Optional
from gotomeeting_manager.gotoexceptions import CredentialError, HTTPError400, HTTPError403, HTTPError404, \
    HTTPError409, HTTPError500, HTTPError502, UserNotFoundError, GroupNotFoundError

from gotomeeting_manager.goto_auth_server import AuthServerThread
from gotomeeting_manager.gotoresponses import UserResponse, GroupResponse


class Manager:

    _config = {
        "access_token": str,
        "refresh_token": str,
        "last_refreshed": str
    }
    _config_path: str

    def __init__(self, consumer_key: Optional[str] = None, consumer_secret: Optional[str] = None,
                 path_to_config: str = "./goto.creds"):

        if consumer_key is None:
            consumer_key = os.environ.get("GOTO_CONSUMER_KEY")
            if consumer_key is None:
                raise CredentialError("'Consumer Key' not specified and not set in $GOTO_CONSUMER_KEY")

        if consumer_secret is None:
            consumer_secret = os.environ.get("GOTO_CONSUMER_SECRET")
            if consumer_secret is None:
                raise CredentialError("'Consumer Secret' not specified and not set in $GOTO_CONSUMER_SECRET")

        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._config_path = path_to_config
        self._load_config()

    # LOAD AND DUMP CONFIG
########################################################################################################################
    def _load_config(self):
        config_file = Path(self._config_path)
        if config_file.exists():
            # Open project specific config
            with open(config_file, "rb") as file:
                self._config = msgpack.unpack(stream=file, raw=False)

        else:
            print("Tokens not found!")
            print("Creating new file...")
            self._cold_start()

    def _dump_config(self):
        config_file = Path(self._config_path)
        with open(config_file, "wb+") as file:
            msgpack.pack(o=self._config, stream=file)

    # TOKEN API CALLS
########################################################################################################################

    def _cold_start(self):
        print("Performing cold start")
        auth_code = self._get_auth_token()
        self._request_tokens(auth_code=auth_code)

    def _get_auth_token(self) -> str:
        """
        Retrieves single-use authentication token which is used to request initial access and refresh tokens
        :return: auth_code: str
        """

        print("Creating authentication web server...")
        app = Flask("Auth_app")
        queue = Queue(maxsize=1)

        @app.route('/')
        def get_auth_code():
            code = request.args.get("code")
            queue.put(escape(code))
            return "Code received! You can close this window now."

        server = AuthServerThread(app)

        try:
            server.start()

            print("Running app...")
            base_url = f"https://api.getgo.com/oauth/v2/authorize?client_id={self._consumer_key}&response_type=code"
            webbrowser.open_new_tab(base_url)

            print("Waiting for code...")
            auth_code = queue.get(timeout=60)

            print("Code received!")
            server.shutdown()

            return auth_code

        except KeyboardInterrupt:
            server.shutdown()

        except TimeoutError:
            server.shutdown()
            print("Timeout reached. Could not receive the code.")

        except Exception:
            server.shutdown()

    def _request_tokens(self, auth_code: str):

        encoded_tokens = base64.b64encode(bytes(f"{self._consumer_key}:{self._consumer_secret}", "utf-8"))

        base_url = "https://api.getgo.com/oauth/v2/token"

        headers = {
            "Authorization": "Basic " + str(encoded_tokens, encoding="utf-8"),
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "authorization_code",
            "code": auth_code
        }

        r = requests.post(url=base_url, headers=headers, data=data)

        if r.status_code != 200:
            raise self._manage_exceptions(r.status_code)(r.text)

        self._config["access_token"] = r.json()["access_token"]
        self._config["refresh_token"] = r.json()["refresh_token"]
        self._config["last_refreshed"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self._dump_config()

    def _refresh_tokens(self, force_refresh: bool = False):

        # Calculate time since last refresh
        time_since_refresh = (datetime.datetime.now() -
                              datetime.datetime.strptime(self._config["last_refreshed"], "%m/%d/%Y, %H:%M:%S")).seconds

        # Check whether tokens have been refreshed within the last 25 days and performs cold start if not
        # Can also be overridden with the force_refresh flag
        if (time_since_refresh >= 25 * 24 * 3600) or force_refresh:
            self._cold_start()

        # Check whether tokens have been refreshed in the last 45 minutes and refreshes them if not
        elif time_since_refresh >= 2700:
            print("Refreshing access token")

            encoded_tokens = base64.b64encode(bytes(f"{self._consumer_key}:{self._consumer_secret}", "utf-8"))

            base_url = "https://api.getgo.com/oauth/v2/token"

            headers = {
                "Authorization": "Basic " + str(encoded_tokens, encoding="utf-8"),
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            data = {
                "grant_type": "refresh_token",
                "refresh_token": self._config["refresh_token"]
            }

            r = requests.post(url=base_url, headers=headers, data=data)

            if r.status_code != 200:
                raise self._manage_exceptions(r.status_code)(r.text)

            self._config["access_token"] = r.json()["access_token"]
            self._config["refresh_token"] = r.json()["refresh_token"]
            self._config["last_refreshed"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

            self._dump_config()

    def create_user(self, first_name: str, last_name: str, email: str,
                    product: str = "G2M") -> Optional[UserResponse]:
        """
        Create a user
        :param first_name: The user's first name
        :param last_name: The user's last name
        :param email: The user's email
        :param product: Optional list containing all the products to assign to the user. Defaults to "G2M" only
        :return:
        """

        self._refresh_tokens()

        base_url = "https://api.getgo.com/G2M/rest/organizers"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }

        data = {
            "organizerEmail": email,
            "firstName": first_name,
            "lastName": last_name,
            "productType": product
        }

        r = requests.post(url=base_url, headers=headers, json=data)

        if r.status_code != 201:
            raise self._manage_exceptions(r.status_code)(r.text)

        try:
            key = r.json()[0]["key"]
        except KeyError:
            return None

        user = self.get_user_by_key(key=key)
        return user

    def get_user_by_email(self, email: str) -> UserResponse:

        self._refresh_tokens()

        base_url = "https://api.getgo.com/G2M/rest/organizers"
        headers = {
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }
        parameters = {
            "email": email
        }

        r = requests.get(url=base_url, headers=headers, params=parameters)

        if r.status_code == 404:
            raise UserNotFoundError

        if r.status_code != 200:
            raise self._manage_exceptions(r.status_code)(r.text)

        return UserResponse.create_from_dict(r.json()[0])

    def get_user_by_key(self, key: str) -> UserResponse:

        self._refresh_tokens()

        base_url = f"https://api.getgo.com/G2M/rest/organizers/{key}"

        headers = {
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }

        r = requests.get(url=base_url, headers=headers)

        if r.status_code == 404:
            raise UserNotFoundError

        if r.status_code != 200:
            raise self._manage_exceptions(r.status_code)(r.text)

        return UserResponse.create_from_dict(r.json()[0])

    def get_all_users(self) -> List[UserResponse]:
        self._refresh_tokens()

        base_url = "https://api.getgo.com/G2M/rest/organizers"

        headers = {
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }

        parameters = {
            "email": ""
        }

        r = requests.get(url=base_url, headers=headers, params=parameters)

        if r.status_code == 404:
            raise UserNotFoundError

        if r.status_code != 200:
            raise self._manage_exceptions(r.status_code)(r.text)

        users = []

        for response in r.json():
            users.append(UserResponse.create_from_dict(user_data=response))

        return users

    def get_groups(self) -> List[GroupResponse]:

        self._refresh_tokens()

        base_url = "https://api.getgo.com/G2M/rest/groups"

        headers = {
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }

        r = requests.get(url=base_url, headers=headers)

        if r.status_code != 200:
            raise self._manage_exceptions(r.status_code)(r.text)

        groups = []

        for response in r.json():
            groups.append(GroupResponse.create_from_dict(group_data=response))

        return groups

    def create_user_in_group(self, first_name: str, last_name: str, email: str, group_name: str,
                             product: str = "G2M") -> UserResponse:
        self._refresh_tokens()

        groups = self.get_groups()
        group_key = None
        for group in groups:
            if group.group_name == group_name:
                group_key = group.group_key

        if group_key is None:
            raise GroupNotFoundError

        base_url = "https://api.getgo.com/G2M/rest/groups/" + str(group_key) + "/organizers"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }

        data = {
            "organizerEmail": email,
            "firstName": first_name,
            "lastName": last_name,
            "productType": product
        }

        r = requests.post(url=base_url, headers=headers, json=data)

        if r.status_code != 201:
            raise self._manage_exceptions(r.status_code)(r.text)

        try:
            key = r.json()[0]["key"]
        except KeyError:
            raise UserNotFoundError

        user = self.get_user_by_key(key=key)

        return user

    def delete_user(self, email: str) -> requests.Response:

        self._refresh_tokens()

        # Get the requested user's key using the provided email
        user_key = self.get_user_by_email(email).organizer_key

        base_url = "https://api.getgo.com/G2M/rest/organizers/" + str(user_key)

        headers = {
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }

        r = requests.delete(url=base_url, headers=headers)

        if r.status_code != 204:
            raise self._manage_exceptions(r.status_code)(r.text)

        return r

    def suspend_user(self, email: str, force_refresh: bool = False) -> UserResponse:

        self._refresh_tokens(force_refresh=force_refresh)

        # Get the requested user's key using the provided email
        user_key = self.get_user_by_email(email=email).organizer_key

        base_url = f"https://api.getgo.com/G2M/rest/organizers/{user_key}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }

        data = {
            "status": "suspended",
            "productType": "G2M"
        }

        r = requests.put(url=base_url, headers=headers, json=data)

        if r.status_code != 204:
            raise self._manage_exceptions(r.status_code)(r.text)

        return self.get_user_by_email(email=email)

    def update_user_products(self, email: str, products: List[str]) -> UserResponse:

        self._refresh_tokens()

        user_key = self.get_user_by_email(email=email).organizer_key

        base_url = f"https://api.getgo.com/G2M/rest/organizers/{user_key}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self._config["access_token"]
        }

        for product in products:
            data = {
                "productType": str(product)
            }

            r = requests.put(url=base_url, headers=headers, json=data)

            if r.status_code != 204:
                raise self._manage_exceptions(r.status_code)(r.text)

        return self.get_user_by_email(email=email)

    # MANAGE EXCEPTIONS
########################################################################################################################

    def _manage_exceptions(self, code):
        exceptions = {
            400: HTTPError400,
            403: HTTPError403,
            404: HTTPError404,
            409: HTTPError409,
            500: HTTPError500,
            502: HTTPError502,
        }
        return exceptions[code]


import os
import json
from urllib import parse

import requests

OAUTH = {
    "linkedin-oauth2": {"url": "https://www.linkedin.com/oauth/v2/accessToken",},
}


def get_payload(backend, code):

    key = f"{backend.upper()}_KEY".replace("-", "_")
    secret = f"{backend.upper()}_SECRET".replace("-", "_")

    client_id = os.environ.get(key, "nokey")
    client_secret = os.environ.get(secret, "nosecret")

    # https://developer.linkedin.com/blog/posts/2018/redirecting-oauth-uas
    # grant_type=authorization_code&redirect_uri=*&client_id=*&client_secret=*&code=*
    if backend == "linkedin-oauth2":
        payload = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost/auth/callback/linkedin-oauth2",
        }

    return payload


def get_access_token_from_code(backend, code):
    """Get access token for any OAuth backend from code"""

    url = OAUTH[backend]["url"]
    payload = get_payload(backend, code)

    if backend == "linkedin-oauth2":
        res = requests.post(url, data=payload)
        access_token = json.loads(res.content)["access_token"]

        return access_token

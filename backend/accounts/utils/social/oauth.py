import logging
import os
import json
from urllib import parse

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)

import requests

OAUTH = {
    "linkedin-oauth2": {
        "url": "https://www.linkedin.com/oauth/v2/accessToken",
    },
}


def get_payload(backend, code):

    logger.info("Getting payload")

    domain_name = os.environ.get("DOMAIN_NAME", "localhost")
    protocol = "http" if domain_name == "localhost" else "https"

    key = f"{backend.upper()}_KEY".replace("-", "_")
    secret = f"{backend.upper()}_SECRET".replace("-", "_")

    client_id = os.environ.get(key, "nokey")
    client_secret = os.environ.get(secret, "nosecret")

    # https://developer.linkedin.com/blog/posts/2018/redirecting-oauth-uas
    # grant_type=authorization_code&redirect_uri=*&client_id=*&client_secret=*&code=*
    if backend == "linkedin-oauth2":
        logger.info(f"Backend is: {backend}")
        payload = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": f"{protocol}://{domain_name}/auth/callback/linkedin-oauth2",
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

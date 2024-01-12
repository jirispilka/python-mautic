# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from pprint import pformat
import os

from flask import Flask, request, redirect, session, url_for, jsonify
from requests_oauthlib import OAuth2Session

from mautic import MauticOauth2Client, Contacts
from mautic.config import Config
from mautic.utils import update_token_tempfile

app = Flask(__name__)

client_id = Config.CLIENT_ID.get_secret_value()
client_secret = Config.CLIENT_SECRET.get_secret_value()
base_url = Config.BASE_URL

redirect_uri = "http://localhost:8000/callback"

base_url = f"{str(base_url).strip(' /')}/"
authorization_base_url = f"{base_url}oauth/v2/authorize"
token_url = f"{base_url}oauth/v2/token"
refresh_url = token_url

extra = {"client_id": client_id, "client_secret": client_secret}


@app.route("/")
def index():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider using an URL with a few key OAuth parameters.
    """
    mautic = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = mautic.authorization_url(authorization_base_url, grant_type="authorization_code")

    session["oauth_state"] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
@app.route("/callback", methods=["GET"])
def callback():
    """Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    mautic = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session["oauth_state"])
    token = mautic.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    # We use the session as a simple DB for this example.
    session["oauth_token"] = token
    update_token_tempfile(token)  # store token in /tmp/mautic_creds.json

    return redirect(url_for(".menu"))


@app.route("/menu", methods=["GET"])
def menu():
    """"""
    return """
    <h1>Congratulations, you have obtained an OAuth 2 token!</h1>
    <h2>What would you like to do next?</h2>
    <ul>
        <li><a href="/contacts"> Get contacts</a></li>
    </ul>

    <pre>
    %s
    </pre>
    """ % pformat(
        session["oauth_token"], indent=4
    )


@app.route("/contacts", methods=["GET"])
def contacts():
    """Fetching a protected resource using an OAuth 2 token."""
    mautic = MauticOauth2Client(
        base_url=base_url,
        client_id=client_id,
        client_secret=client_secret,
        token=session["oauth_token"],
        token_updater=update_token_tempfile,
    )
    return jsonify(Contacts(client=mautic).get_list())


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "not_to_be_used_in_production"
    app.config["SERVER_NAME"] = "localhost:8000"

    os.environ["DEBUG"] = "1"
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run(host="localhost", port=8000)

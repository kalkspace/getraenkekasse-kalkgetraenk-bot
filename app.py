from flask import Flask, request, abort
from requests import get
import os
from mastodon import Mastodon

if not "METE_BASEURL" in os.environ:
    raise Exception("Please specify METE_BASEURL")

METE_BASEURL = os.environ["METE_BASEURL"]
if not "MASTODON_ACCESS_TOKEN" in os.environ:
    raise Exception("Please specify MASTODON_ACCESS_TOKEN")
MASTODON_ACCESS_TOKEN = os.environ["MASTODON_ACCESS_TOKEN"]

mastodon = Mastodon(
    access_token=MASTODON_ACCESS_TOKEN,
    api_base_url="https://botsin.space",
)


app = Flask(__name__)


@app.route("/mete/api/v1/users/<int:user_id>/buy.json", methods=["GET"])
def buy(user_id):
    args = request.args
    try:
        drink = int(args.get("drink"))
    except KeyError:
        abort(400)

    buy_response = get(f"{METE_BASEURL}/api/v1/users/{user_id}/buy.json?drink={drink}")
    if not buy_response.ok:
        abort(500, buy_response)

    drink_response = get(f"{METE_BASEURL}/api/v1/drinks/{drink}.json")
    drink = drink_response.json()

    drink_name = drink["name"]
    mastodon.toot(f"{drink_name}!")

    return "Hello, World!"

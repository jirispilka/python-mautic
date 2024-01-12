"""
"""
import json

from mautic import Campaigns, MauticBasicAuthClient
from mautic.config import Config

mclient = MauticBasicAuthClient(
    base_url=Config.BASE_URL.__str__(), username=Config.USERNAME, password=Config.PASSWORD.get_secret_value()
)


campaign = Campaigns(client=mclient)

c = campaign.get("23")
print(json.dumps(c, indent=2))

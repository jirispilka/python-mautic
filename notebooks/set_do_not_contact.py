"""
    Load emails from Amazon SES and mark them as Do Not Contact in the Mautic platform.

    Bounced emails
    Complaints
"""

from datetime import datetime, timedelta

import boto3

from mautic import Contacts, MauticBasicAuthClient
from mautic.config import Config

mclient = MauticBasicAuthClient(
    base_url=Config.BASE_URL.__str__(), username=Config.USERNAME, password=Config.PASSWORD.get_secret_value()
)

TIMESTAMP_FROM = (datetime.now() - timedelta(days=3)).timestamp()

client = boto3.client("sesv2")
ses_suppressed = client.list_suppressed_destinations(StartDate=TIMESTAMP_FROM)

contacts = Contacts(client=mclient)


def get_by_email(keyword: str) -> tuple[str | None, dict | None]:
    d = contacts.get_list(search=keyword)

    if not d:
        print("ERROR: Not found email")
        return None, None

    if int(d.get("total")) > 1:
        print("ERROR Multiple users with the same ID")
        return None, None

    _id = list(d["contacts"].keys())[0]
    return _id, d["contacts"][_id]


N = len(ses_suppressed["SuppressedDestinationSummaries"])
print(f"Number of suppressed emails: {N}")


for i, v in enumerate(ses_suppressed["SuppressedDestinationSummaries"]):

    email = v["EmailAddress"]
    reason = v["Reason"]

    _id, rec = get_by_email(v["EmailAddress"])
    print(f"{i}/{N}, ID: {_id}, email: {email}, reason: {reason}")

    if not _id:
        continue

    reason = Contacts.BOUNCED if reason == "BOUNCE" else Contacts.MANUAL
    comments = f"SES-{v['Reason']}"

    print(f"doNotContact: {rec['doNotContact']}")
    if not rec["doNotContact"]:
        response = contacts.add_dnc(_id, channel="email", reason=reason, comments=comments)
        print(f"doNotContact: {response['contact']['doNotContact']}")

print("DONE")

"""
    Load contacts and companies from Hubspot and mark them as Do Not Contact in the Mautic.
    In the hubspot we keep a list of MQLs. This list needs to be exported every time.
"""

import pandas as pd

from mautic import Contacts, MauticBasicAuthClient
from mautic.config import Config

CONTACTS = ""
COMPANIES = "~/Downloads/hubspot-crm-exports-wellness-mql-opportunity-2024-01-24.csv"

mclient = MauticBasicAuthClient(
    base_url=Config.BASE_URL.__str__(), username=Config.USERNAME, password=Config.PASSWORD.get_secret_value()
)

contacts = Contacts(client=mclient)


def get_by_keyword(keyword: str) -> dict | None:
    d = contacts.get_list(search=keyword)

    if int(d.get("total")) == 0:
        print("INFO: No contact found")
        return None

    return d["contacts"]


def preprocess_domain(s: str) -> str:
    """Remove https://, remove www. and slashes"""
    s = s.replace("https://", "").replace("www.", "").replace("/", "")
    return s.replace(".com", "").replace(".edu", "").replace(".net", "").replace(".org", "")


df_c = pd.read_csv(COMPANIES)
domains = df_c["Company Domain Name"].unique().tolist()
keywords = list(map(preprocess_domain, domains))

if CONTACTS:
    df = pd.read_csv(CONTACTS)
    emails = df["Email"].unique().tolist()
else:
    emails = df_c["Email"].unique().tolist()

emails = [e for e in emails if str(e) != "nan"]
keywords += emails
keywords.sort()
N = len(keywords)

print("Running companies domains / contact emails")
for i, v in enumerate(keywords):

    print(f"{i}/{N}, domain/email: {v}")
    if people := get_by_keyword(v):
        for person in people.values():
            core = person["fields"]["core"]
            dnc = person["doNotContact"]
            print(
                f"First name: {core['firstname']['value']}, last name: {core['lastname']['value']}, company: {core['company']['value']}"
            )
            print(f"Email: {core['email']['value']}, dnc: {person['doNotContact']}")

            if not dnc:
                response = contacts.add_dnc(person["id"], channel="email", reason=Contacts.MANUAL, comments="lead")
                print(f"doNotContact: {response['contact']['doNotContact']}")

print("DONE")

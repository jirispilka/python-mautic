"""
    Load contacts and companies from Hubspot and check if they are in csv file.
"""

import pandas as pd

COMPANIES = "~/Downloads/hubspot-crm-exports-wellness-mql-opportunity-2024-01-29.csv"

csv_file = open("/home/jirka/gitlab/cqa-data-mining/notebooks/Tenants_data_na0-na2_20230607_multi_loc.csv").read()
csv_file = csv_file.lower()


def preprocess_domain(s: str | float) -> str:
    """Remove https://, remove www. and slashes"""
    s = str(s).replace("https://", "").replace("www.", "").replace("/", "")
    return s.replace(".com", "").replace(".edu", "").replace(".net", "").replace(".org", "")


df_c = pd.read_csv(COMPANIES)
domains = df_c["Company Domain Name"].unique().tolist()
keywords = list(map(preprocess_domain, domains))

emails = df_c["Email"].unique().tolist()
emails = [e for e in emails if str(e) != "nan"]
keywords += emails
keywords.sort()
N = len(keywords)

print("Running companies domains / contact emails")
for i, v in enumerate(keywords):

    if v in csv_file:
        print(f"{i}/{N}, domain/email: {v}")
        print(v)

print("DONE")

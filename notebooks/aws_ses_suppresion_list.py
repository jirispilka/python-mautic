"""
Get emails from SES suppressed destinations
"""

import boto3

client = boto3.client('sesv2')

response = client.list_suppressed_destinations(
    StartDate=1704067200
)

for v in response["SuppressedDestinationSummaries"]:
    print(v)

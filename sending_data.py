import bloock
from bloock.client.integrity import IntegrityClient
from bloock.client.record import RecordClient
from bloock.entity.integrity.network import Network
import json
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
bloock.api_key = os.environ.get('API_KEY')

record_client = RecordClient()
integrity_client = IntegrityClient()

decision=input("enter decision:(yes or no): ")
dict_={"name":"Saif2",
        "uuid":"02",
        "decision":decision.upper()
        }
# Convert the dictionary to a JSON string
json_string = json.dumps(dict_)

# and build a record from it
record = record_client.from_json(json_string).build()
records = [record]

send_receipts = integrity_client.send_records(records)
print("\nWaiting for anchor...")

anchor = integrity_client.wait_anchor(send_receipts[0].anchor, timeout=120000)
print("Done!\n")
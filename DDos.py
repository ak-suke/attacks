import csv
from datetime import datetime
import requests
import threading
import time
import random

GRAPHQL_ENDPOINT = "http://localhost:4012/api/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "LoadTestingTool/1.0",
    "x-csrf-token": "f968ec6fcd3429029c47850e44d41496a053d9ea7e425fcdea93fa94d57144c5",
}

GRAPHQL_QUERY = """
query Posts($take: Int!, $skip: Int!) {
  posts(take: $take, skip: $skip) {
    count
    data {
      id
      title
      publishDate
      status
      privacy
    }
  }
}
"""


QUERY_VARIABLES = {
    "take": 10,
    "skip": 0
}

GRAPHQL_MUTATION = """
mutation ContactCreate($input: ContactInput!) {
  contactCreate(input: $input)
}
"""

MUTATION_VARIABLES = {
    "input": {
        "reference": "test_reference",
        "companyName": "Test Company",
        "facilityType": "Test Facility",
        "facilityName": "Test Facility Name",
        "postCode": "123456",
        "prefectureName": "Test Prefecture",
        "email": "test@example.com",
        "phoneNumber": "1234567890",
        "chargeName": "Test Name",
        "serviceName": "Test Service",
        "detailQuestion": "This is a test question."
    }
}

RATE_LIMIT = 0.1

NUM_THREADS = 10

CSV_FILE = "graphql_ddos_results.csv"

with open(CSV_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Request Type", "Status Code", "Response", "Error"])

def log_to_csv(timestamp, request_type, status_code, response, error):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, request_type, status_code, response, error])

def send_graphql_request(request_type):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if request_type == "query":
            payload = {"query": GRAPHQL_QUERY, "operationName": "Posts", "variables": QUERY_VARIABLES}
        elif request_type == "mutation":
            payload = {
                "query": GRAPHQL_MUTATION, "operationName": "ContactCreate", "variables": MUTATION_VARIABLES
            }

        response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json=payload)
        print(f"[{request_type.upper()}] Status Code: {response.status_code} | Response: {response.text}")
        log_to_csv(timestamp, request_type, response.status_code, response.text, "")
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{request_type.upper()}] Error: {e}")
        log_to_csv(timestamp, request_type, "Error", "", str(e))

def ddos_attack(request_type):
    while True:
        send_graphql_request(request_type)
        time.sleep(RATE_LIMIT)

if __name__ == "__main__":
    print(f"Starting DDoS simulation for GraphQL endpoint. Results will be saved to {CSV_FILE}")
    threads = []

    for _ in range(NUM_THREADS // 2):
        t = threading.Thread(target=ddos_attack, args=("query",))
        threads.append(t)
        t.start()

    # for _ in range(NUM_THREADS // 2):
    #     t = threading.Thread(target=ddos_attack, args=("mutation",))
    #     threads.append(t)
    #     t.start()

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Stopping DDoS simulation.")
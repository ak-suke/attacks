import csv
import threading
import time
import random
from datetime import datetime
import requests

FRONTEND_URL = "http://localhost:3012/contact"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "LoadTestingTool/1.0",
}
PAYLOAD = {
    "name": "Test User",
    "email": "testuser@example.com",
    "message": "This is a test message for DDoS simulation.",
}
RATE_LIMIT = 0.1
NUM_THREADS = 10
CSV_FILE = "frontend_ddos_results.csv"

# Create CSV file to log results
with open(CSV_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Status Code", "Response", "Error"])

def log_to_csv(timestamp, status_code, response, error):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, status_code, response, error])

def send_request():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = requests.post(FRONTEND_URL, headers=HEADERS, json=PAYLOAD)
        print(f"Status Code: {response.status_code} | Response: {response.text}")
        log_to_csv(timestamp, response.status_code, response.text, "")
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Error: {e}")
        log_to_csv(timestamp, "Error", "", str(e))

def ddos_attack():
    while True:
        send_request()
        time.sleep(RATE_LIMIT)

if __name__ == "__main__":
    print(f"Starting DDoS simulation for front-end at {FRONTEND_URL}. Results will be saved to {CSV_FILE}")
    threads = []

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=ddos_attack)
        threads.append(t)
        t.start()

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Stopping DDoS simulation.")


import csv
import requests

with open("books.csv", "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    url = next(reader)["url"].strip()

print("Testing URL...")
print("URL length:", len(url))

try:
    response = requests.get(url, timeout=15)
    print("HTTP status:", response.status_code)
    print("Page title available:", "A Light in the Attic" in response.text)
except requests.RequestException as error:
    print("Request failed:", error)
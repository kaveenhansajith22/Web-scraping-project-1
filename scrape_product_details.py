
import csv
import time
import requests
from bs4 import BeautifulSoup

INPUT_FILE = "books.csv"
OUTPUT_FILE = "detailed_books.csv"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; LearningScraper/1.0)"
}

# These are the original CSV columns plus the new product details.
extra_fields = [
    "description",
    "upc",
    "product_type",
    "price_excl_tax",
    "price_incl_tax",
    "tax",
    "product_availability",
    "number_of_reviews",
]

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    books = list(reader)

total = len(books)
successful = 0
failed = 0

fieldnames = list(books[0].keys()) + [
    field for field in extra_fields if field not in books[0]
]

with requests.Session() as session:
    session.headers.update(headers)

    with open(
        OUTPUT_FILE, "w", encoding="utf-8-sig", newline=""
    ) as output_file:

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for index, book in enumerate(books, start=1):
            url = book["url"].strip()

            print(f"[{index}/{total}] Scraping: {book['title']}")

            try:
                response = session.get(url, timeout=15)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Extract the description.
                description = ""
                heading = soup.find("div", id="product_description")

                if heading:
                    paragraph = heading.find_next_sibling("p")
                    if paragraph:
                        description = paragraph.get_text(" ", strip=True)

                # Extract the product information table.
                details = {}

                for row in soup.select("table tr"):
                    label = row.find("th")
                    value = row.find("td")

                    if label and value:
                        details[label.get_text(strip=True)] = (
                            value.get_text(" ", strip=True)
                        )

                book["description"] = description
                book["upc"] = details.get("UPC", "")
                book["product_type"] = details.get("Product Type", "")
                book["price_excl_tax"] = details.get("Price (excl. tax)", "")
                book["price_incl_tax"] = details.get("Price (incl. tax)", "")
                book["tax"] = details.get("Tax", "")
                book["product_availability"] = details.get("Availability", "")
                book["number_of_reviews"] = details.get("Number of reviews", "")

                writer.writerow(book)
                output_file.flush()
                successful += 1

            except requests.RequestException as error:
                print(f"  ERROR: {error}")
                failed += 1

            # Pause between requests.
            time.sleep(0.5)

print("\n--- SCRAPING SUMMARY ---")
print(f"Total books: {total}")
print(f"Successfully scraped: {successful}")
print(f"Failed requests: {failed}")
print(f"Output file: {OUTPUT_FILE}")
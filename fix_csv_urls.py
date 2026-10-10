
import csv
import os
import re

INPUT_FILE = "books.csv"
TEMP_FILE = "books_cleaned.csv"

fixed_count = 0

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as input_file:
    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames

    with open(TEMP_FILE, "w", encoding="utf-8-sig", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            original_url = row["url"].strip()

            # Find the actual HTTP or HTTPS URL anywhere in the text.
            match = re.search(r"https?://[^\s)\]]+", original_url)

            if match:
                clean_url = match.group(0)

                if clean_url != original_url:
                    fixed_count += 1

                row["url"] = clean_url

            writer.writerow(row)

os.replace(TEMP_FILE, INPUT_FILE)

print(f"URLs cleaned: {fixed_count}")
print("Finished.")
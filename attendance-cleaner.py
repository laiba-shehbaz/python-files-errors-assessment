"""Student Attendance Cleaner - cleans names in attendance.txt and writes a sorted CSV."""

import csv

INPUT_FILE = "attendance.txt"
OUTPUT_FILE = "attendance-clean.csv"


def read_names(filename=INPUT_FILE):
    """Read raw lines from the file; return None if the file is missing."""
    try:
        with open(filename, encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: {filename} was not found. Place it next to this script.")
        return None


def clean_names(raw_lines):
    """Strip spaces and apply title case using a list comprehension.

    The split/join also collapses extra spaces *inside* a name.
    Blank lines are skipped.
    """
    return [" ".join(line.strip().title().split()) for line in raw_lines if line.strip()]


def write_csv(names, filename=OUTPUT_FILE):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["name"])
            writer.writerows([name] for name in names)
        return True
    except OSError as error:
        print(f"Error: could not write {filename}: {error}")
        return False


def main():
    raw_lines = read_names()
    if raw_lines is None:
        return

    original_records = len(raw_lines)
    cleaned = clean_names(raw_lines)
    unique_students = set(cleaned)          # a set removes duplicates
    sorted_names = sorted(unique_students)  # sets are unordered, so sort

    print(f"Original number of records : {original_records}")
    print(f"Blank lines skipped        : {original_records - len(cleaned)}")
    print(f"Records after cleaning     : {len(cleaned)}")
    print(f"Unique students (set)      : {len(unique_students)}")
    print(f"Duplicates removed         : {len(cleaned) - len(unique_students)}")
    print("\nCleaned attendance list (sorted A-Z):")
    for number, name in enumerate(sorted_names, start=1):
        print(f"  {number:>2}. {name}")

    if write_csv(sorted_names):
        print(f"\nSaved {len(sorted_names)} names to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

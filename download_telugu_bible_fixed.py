#!/usr/bin/env python3
"""
Fixed Telugu Bible Data Downloader
This script properly handles the JSON structure from GitHub.
"""

import urllib.request
import json
import os

print("=" * 60)
print("Telugu Bible Data Downloader (Fixed)")
print("=" * 60)
print()

# GitHub URL for complete Telugu Bible
url = "https://raw.githubusercontent.com/godlytalias/Bible-Database/master/Telugu/bible.json"

print(f"📥 Downloading Telugu Bible from GitHub...")
print(f"Source: {url}")
print()
print("⏳ This may take a few minutes (11.2 MB file)...")
print()

try:
    # Download the file
    with urllib.request.urlopen(url) as response:
        data = response.read()
        raw_json = json.loads(data.decode('utf-8'))

    print("✅ Download complete!")
    print()
    print("📊 Processing data structure...")

    # The JSON from GitHub is a LIST of dictionaries, not a single dictionary
    # Each list item contains one book as {book_name: {chapters}}
    # We need to merge them into a single dictionary

    bible_data = {}

    if isinstance(raw_json, list):
        print(f"   - Found {len(raw_json)} books")
        for book_item in raw_json:
            if isinstance(book_item, dict):
                # Each book_item is like {"ఆదికాండము": {"1": {"1": "verse", ...}, ...}}
                for book_name, chapters in book_item.items():
                    bible_data[book_name] = chapters
    elif isinstance(raw_json, dict):
        # If it's already a dictionary, use it directly
        bible_data = raw_json
    else:
        raise ValueError(f"Unexpected JSON structure: {type(raw_json)}")

    print()

    # Save to telugu_bible.json
    output_file = "telugu_bible.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bible_data, f, ensure_ascii=False, indent=2)

    # Calculate stats
    total_verses = 0
    total_books = len(bible_data)

    for book_name, chapters in bible_data.items():
        if isinstance(chapters, dict):
            for chapter_num, verses in chapters.items():
                if isinstance(verses, dict):
                    total_verses += len(verses)

    print(f"📊 Statistics:")
    print(f"   - Books: {total_books}")
    print(f"   - Total verses: {total_verses:,}")
    print(f"   - Output file: {output_file}")
    print(f"   - File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
    print()
    print("=" * 60)
    print("✅ Telugu Bible data ready!")
    print("You can now run: python app.py")
    print("=" * 60)

except urllib.error.URLError as e:
    print(f"❌ Network error: {e}")
    print()
    print("Please check your internet connection and try again.")
except json.JSONDecodeError as e:
    print(f"❌ JSON parsing error: {e}")
    print()
    print("The downloaded file may be corrupted. Please try again.")
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Alternative: Download manually from:")
    print("https://github.com/godlytalias/Bible-Database")
    print()
    print("Then save as 'telugu_bible.json' in this directory.")

input("\nPress Enter to exit...")

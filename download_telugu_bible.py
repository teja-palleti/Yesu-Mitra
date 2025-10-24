#!/usr/bin/env python3
"""
Download Telugu Bible JSON data from GitHub
This script downloads the complete Telugu Bible in JSON format.
"""

import urllib.request
import json
import os

print("=" * 60)
print("Telugu Bible Data Downloader")
print("=" * 60)
print()

# Option 1: GitHub repo with complete Telugu Bible (11.2 MB)
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
        bible_json = json.loads(data.decode('utf-8'))

    print("✅ Download complete!")
    print()

    # Save to telugu_bible.json
    output_file = "telugu_bible.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bible_json, f, ensure_ascii=False, indent=2)

    # Calculate stats
    total_verses = 0
    total_books = len(bible_json)

    for book_data in bible_json:
        for book_name, chapters in book_data.items():
            for chapter_num, verses in chapters.items():
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

except Exception as e:
    print(f"❌ Error downloading Bible data: {e}")
    print()
    print("Alternative: Download manually from:")
    print("https://github.com/godlytalias/Bible-Database")
    print()
    print("Then save as 'telugu_bible.json' in this directory.")

input("\nPress Enter to exit...")

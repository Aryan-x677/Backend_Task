# Backend_Task

# Spotify Artist Catalog & Unclaimed ISRC Cross-Reference

## Overview
This project fetches a full catalog of songs for a chosen artist from the Spotify API and cross-references the tracks' ISRC codes against a large dataset of unclaimed musical work right shares.  

The final output is an Excel file containing:  
1. **Artist Catalog** – all tracks with album, release date, and ISRC.  
2. **Matches** – tracks found in the unclaimed works dataset.  
3. **Notes** – assumptions, observations, and execution details.

---

## Features
- Fetches all albums, singles, and EPs for a chosen artist via the Spotify API.  
- Handles **large datasets (~6 GB TSV)** efficiently using chunked processing.  
- Cross-references ISRC codes to identify unclaimed tracks.  
- Exports a clean **multi-sheet Excel file** for easy analysis.  
- Measures execution time and logs progress for transparency.  

---

## Prerequisites
- Python 3.10+  
- Virtual environment (recommended)

### Python Packages
Install dependencies via:

```bash
pip install -r requirements.txt
requirements.txt includes:
pandas
requests
openpyxl


Dataset:

The dataset used is:
unclaimedmusicalworkrightshares.tsv (~6 GB)
Note: This file is too large to include in the repository. Download it from Google Drive link: https://drive.google.com/file/d/1ZAAgkfhmMaq5r6dfKq4D3qgfBewM0D2x/view and place it in the data/ folder.

Folder Structure:

backend-task/
│── data/
│   └── unclaimedmusicalworkrightshares.tsv
│── output/
│   └── artist_report.xlsx
│── fetch_spotify.py
│── compare_dataset.py
│── main.py
│── requirements.txt
│── README.md


USAGE:
Activate your virtual environment:

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Run the main script:
python main.py
 

The script will:
1. Fetch the artist’s catalog from Spotify.
2. Process the TSV dataset in chunks and find ISRC matches.
3. Export the results to output/artist_report.xlsx.

Open the Excel file to view all sheets:
Artist Catalog
Matches
Notes

Approach Summary:

1. Spotify API: Fetch artist albums → fetch tracks → extract ISRCs.
2. Dataset processing: Read TSV in chunks → filter by ISRC → append matches.
3. Output: Save all results to Excel with clear sheets and notes.

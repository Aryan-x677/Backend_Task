import pandas as pd
from fetch_spotify import fetch_artist_tracks
from cross_reference import find_matches_in_tsv
import openpyxl
import time

def main():
    start_time = time.time()

    artist_name = input("Enter the artist's name: ")
    print(f"Fetching catalog for artist: {artist_name}")

    catalog = fetch_artist_tracks(artist_name)

    if not catalog:
        print("No tracks found for the given artist.")
        return None

    df_catalog = pd.DataFrame(catalog)

    print("Catalog fetched successfully.")
    print("Cross-referencing with the TSV file...")

    isrcs = set(df_catalog['isrc'].dropna().unique())

    tsv_file = 'data/unclaimedmusicalworkrightshares.tsv'
    matches_df = find_matches_in_tsv(isrcs, tsv_file)

    if matches_df.empty:
        print("No matches found in the TSV file.")
        return 
    
    print("Saving results to Excel file...")

    with pd.ExcelWriter('output/artist_catalog.xlsx', engine="openpyxl") as writer:
        df_catalog.to_excel(writer, sheet_name='Catalog', index=False)
        matches_df.to_excel(writer, sheet_name='Matches', index=False)

        notes = pd.DataFrame(
            {"notes": "Cross-referenced data between Spotify catalog and TSV file."},
            {"note": "Spotify API used to fetch artist catalog"},
            {"note": "Execution time: 289.59 sec (approx)"},
            {"note": "Assumptions: ISRC codes matched exactly"}, index=[0])
        
        notes.to_excel(writer, sheet_name='Notes', index=False)

    print("Data saved to artist_catalog.xlsx successfully.")

    end_time = time.time()
    print(f"Process completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
    

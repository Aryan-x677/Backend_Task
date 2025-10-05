import pandas as pd 

def find_matches_in_tsv(catalog_irsc, tsv_file):
    matches = []
    chunksize = 500_000

    for chunk in pd.read_csv(tsv_file, sep='\t', chunksize=chunksize):
        
        if 'ISRC' not in chunk.columns:
            raise ValueError("The TSV file does not contain an 'IRSC' column.")
        
        filtered = chunk[chunk["ISRC"].isin(catalog_irsc)]

        if not filtered.empty:
            matches.append(filtered)
        
    if matches:
        return pd.concat(matches, ignore_index=True)
    
    return pd.DataFrame()
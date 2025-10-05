import pandas as pd

# Read just the first row to check columns
df = pd.read_csv("data/unclaimedmusicalworkrightshares.tsv", sep="\t", nrows=5)
print(df.columns)

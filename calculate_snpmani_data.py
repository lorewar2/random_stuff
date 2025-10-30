import pandas as pd
barcode_df = pd.read_csv("pool4_barcodes_donors.csv")

barcode_df["barcode"] = barcode_df["barcode"].str.split("-", n=1).str[0]

barcode_donor_list = list(zip(barcode_df["barcode"], barcode_df["donor_id"]))

khm_df = pd.read_csv("khm_filtered.tsv", sep="\t", header=None, usecols=[0, 1], names=["barcode", "cluster"])
print(khm_df["barcode"])
khm_df["barcode"] = khm_df["barcode"].str.split("-", n=1).str[0]
filtered_df = khm_df[khm_df["barcode"].isin(barcode_df["barcode"])]
filtered_df = filtered_df.merge(barcode_df, on="barcode", how="left")

# Display results
print(filtered_df)

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import adjusted_rand_score

le = LabelEncoder()
filtered_df["donor_encoded"] = le.fit_transform(filtered_df["donor_id"])

filtered_df["cluster"] = filtered_df["cluster"].astype(int)

ari = adjusted_rand_score(filtered_df["cluster"], filtered_df["donor_encoded"])
print("Adjusted Rand Index between clusters and donors:", ari)


# summary

filtered_df["cluster"] = filtered_df["cluster"].astype(int)

# Step 1: Create a crosstab (cluster x donor_id) counting cells
cluster_donor_counts = pd.crosstab(filtered_df["cluster"], filtered_df["donor_id"])

# Step 2: Display nicely
for cluster in cluster_donor_counts.index:
    counts = cluster_donor_counts.loc[cluster]
    counts_str = " ".join([f"{donor}-{count}" for donor, count in counts.items() if count > 0])
    print(f"Cluster {cluster}: {counts_str}")
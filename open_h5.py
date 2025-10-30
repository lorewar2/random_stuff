import h5py
import pandas as pd

pd.set_option("display.max_rows", None)


# Path to your file
file_path = "day11.h5"

with h5py.File(file_path, "r") as f:
    # Categorical donor ID mapping
    categories = [x.decode() for x in f["obs/__categories/pool_id"][:]]
    donor_indices = f["obs/pool_id"][:]  # integer codes
    donors = [categories[i] for i in donor_indices]

# Convert to dataframe for inspection
donor_df = pd.DataFrame({"pool_id": donors})
#print(donor_df)
#print("Unique donors:", donor_df["donor_id"].unique())

import scanpy as sc

adata = sc.read_h5ad("day11.h5")

# Show donor column in cell metadata
print(adata.obs["donor_id"].value_counts())

summary = adata.obs.groupby(["donor_id", "pool_id", "sample_id"]).size().reset_index(name="n_cells")
#print(summary)

pool4 = adata.obs[adata.obs["pool_id"] == "pool4"]

donor_barcodes = (
    pool4.groupby(["donor_id", "sample_id"])
    .apply(lambda x: list(x.index))  # x.index contains the cell barcodes
    .reset_index(name="cell_barcodes")
)
# Filter out entries with zero cells
donor_barcodes["n_cells"] = donor_barcodes["cell_barcodes"].apply(len)
donor_barcodes = donor_barcodes[donor_barcodes["n_cells"] > 0]
donor_barcodes = donor_barcodes[donor_barcodes["sample_id"] == "5245STDY7487301"]
# Optionally display all rows
pd.set_option("display.max_rows", None)

# Print results
print("Cell barcodes for each donor in Pool 4:")
print(donor_barcodes[["donor_id", "sample_id", "n_cells", "cell_barcodes"]])


# import scanpy as sc
# import pandas as pd

# # Load your single-cell h5ad / h5 file
# adata = sc.read_h5ad("day11.h5")

# # Ensure pool_id and donor_id columns exist
# if "pool_id" not in adata.obs or "donor_id" not in adata.obs:
#     raise ValueError("File is missing 'pool_id' or 'donor_id' fields in .obs")

# # Filter only Pool 4 cells
# pool4 = adata.obs[adata.obs["pool_id"] == "pool4"].copy()

# # Keep only barcodes with a donor_id
# pool4 = pool4[pool4["donor_id"].notna()]
# pool4 = pool4[pool4["sample_id"] == "5245STDY7487301"]

# # Create a flat DataFrame with barcode and donor_id
# barcode_df = pd.DataFrame({
#     "barcode": pool4.index,
#     "donor_id": pool4["donor_id"].values
# })

# # Sort by barcode
# barcode_df = barcode_df.sort_values("barcode").reset_index(drop=True)

# # Display all rows if needed
# pd.set_option("display.max_rows", None)

# # Print result
# print(barcode_df)

# barcode_df.to_csv("pool4_barcodes_donors.csv", index=False)
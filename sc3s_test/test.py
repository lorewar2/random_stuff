

import scanpy as sc
import sc3s

# Load your dataset
adata = sc.read_csv("mod_dense.csv")


# Log transform the data (equivalent to log2(x+1))
sc.pp.log1p(adata)

# Perform PCA for dimensionality reduction
sc.tl.pca(adata, n_comps= 50, svd_solver='arpack')

# Apply SC3 consensus clustering with n_clusters=6 (matching the ks=6)
sc3s.tl.consensus(adata, n_clusters=6)

print(adata.obs['sc3s_6'])


import scanpy as sc

# Load the .h5ad file
adata = sc.read_h5ad("../data_snrnaseq/annotated-final_1.h5ad") 

# View the object
#print(adata)

# View metadata for cells
print(adata.obs.head())

# View gene annotations
print(adata.var.head())

# View raw expression matrix (sparse matrix!)
print(adata.X[:5, :5].todense())

# Check what dimensionality reduction is available (e.g. PCA, UMAP)
print(adata.obsm.keys())



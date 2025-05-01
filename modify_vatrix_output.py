import numpy as np
from scipy.io import mmread, mmwrite
from scipy.sparse import coo_matrix

# Load ALT and REF matrices
alt = mmread('alt.mtx').tocoo()
ref = mmread('ref.mtx').tocoo()

# Sum ALT and REF counts by row (variant)
alt_sum = np.array(alt.sum(axis=1)).flatten()
ref_sum = np.array(ref.sum(axis=1)).flatten()

# Identify variants (rows) with >12 ALT and >12 REF counts
valid_variants = np.where((alt_sum > 12) & (ref_sum > 12))[0]
valid_variant_set = set(valid_variants)

# Create a mapping from old row index to new row index
row_map = {old: new for new, old in enumerate(valid_variants)}

# Function to filter a matrix by valid rows
def filter_matrix(matrix, valid_variant_set, row_map):
    rows, cols, data = [], [], []
    for i, j, v in zip(matrix.row, matrix.col, matrix.data):
        if i in valid_variant_set:
            rows.append(row_map[i])
            cols.append(j)
            data.append(v)
    return coo_matrix((data, (rows, cols)), shape=(len(valid_variant_set), matrix.shape[1]))

# Filter the matrices
alt_mod = filter_matrix(alt, valid_variant_set, row_map)
ref_mod = filter_matrix(ref, valid_variant_set, row_map)

# Write the new matrices
mmwrite('alt_mod.mtx', alt_mod)
mmwrite('ref_mod.mtx', ref_mod)
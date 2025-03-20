
```{r}
library(ggplot2)

# Load the dataset
data <- tmp_clusters

set.seed(1)  # For reproducibility
data <- data[sampled_indices, ]

likelihoods <- data[, 3:ncol(data)]
likelihoods <- t(apply(likelihoods[,1:ncol(likelihoods)], 1, function(x){(x/mean(x))}))
# Perform PCA
pca_result <- prcomp(likelihoods, center = TRUE, scale. = TRUE)

# Create a data frame for plotting
pca_data <- data.frame(PC1 = pca_result$x[, 1], 
                        PC2 = pca_result$x[, 2], 
                        Cluster = as.factor(data[, 2]))  # Convert cluster to factor for coloring

# Plot PCA results
ggplot(pca_data, aes(x = PC1, y = PC2, color = Cluster)) +
  geom_point(alpha = 0.7, size = 2) +
  theme_minimal() +
  labs(title = "PCA of Cell Clusters", x = "PC1", y = "PC2", color = "Cluster")

```

```{r}
library(ggplot2)
library(umap)
library(RColorBrewer)
# Load the dataset
data <- final_clusters_common
data <- data[data$status != "unassigned", ]
data <- data[data$status != "doublet", ]
data <- data[1:(nrow(data) - 1500),]

set.seed(2)  # For reproducibility
sampled_indices <- sample(seq_len(nrow(data)), size = floor(nrow(data) * 0.2))
data <- data[sampled_indices, ]

# Extract relevant columns (likelihood values start from the third column)
likelihoods <- data[, 8:ncol(data)]
likelihoods <- t(apply(likelihoods[,1:ncol(likelihoods)], 1, function(x){(x/mean(x))}))

# Perform UMAP
umap_result <- umap(likelihoods)
ground_truth_clusters <- sub(".*-(\\d+)$", "\\1", data[, 1])
# Create a data frame for plotting
umap_data <- data.frame(UMAP1 = umap_result$layout[, 1], 
                        UMAP2 = umap_result$layout[, 2], 
                        Cluster = as.factor(ground_truth_clusters))  # Convert cluster to factor for coloring
```

```{r}
# Generate distinct colors for clusters
color_palette <- colorRampPalette(brewer.pal(12, "Set3"))(51)
print(color_palette)
# Plot UMAP results
ggplot(umap_data, aes(x = UMAP1, y = UMAP2, color = Cluster)) +
  geom_point(alpha = 0.7, size = 1.2) +
  scale_color_manual(values = color_palette) +
  theme_minimal() +
  labs(title = "UMAP of Cell Clusters", x = "UMAP1", y = "UMAP2", color = "Cluster")
```

```{r}
data <- final_clusters_common
data <- data[data$status != "unassigned", ]
data <- data[data$status != "doublet", ]
ground_truth_clusters <- sub(".*-(\\d+)$", "\\1", data[, 1])
predicted_clusters <- data[, 3]



custom_y_order <- c("38", "6", "46", "30", "13", "44", "27", "34", "32", "25", "29", "10", "16", "28", "49", "4","48", "18", "7", "21", "43", "17", "50", "12", "2", "24", "23", "15", "33", "26", "39", "20", "41", "31", "36", "45", "40", "0", "37", "47", "42", "35", "3", "14", "5", "19", "22", "9", "11", "8", "1")
custom_y_order <- as.numeric(custom_y_order)
# Convert to a data frame
df <- data.frame(x = as.numeric(ground_truth_clusters), y = as.numeric(predicted_clusters))

# Create a 2D bin count
bin_counts <- df %>%
  count(x, y, .drop = FALSE)  # Ensures missing combinations are included

# Create a complete grid using unique values in x and the custom y order
x_range <- seq(min(df$x), max(df$x), by = 1)
full_grid <- expand.grid(x = x_range, y = custom_y_order) %>%
  left_join(bin_counts, by = c("x", "y")) %>%
  mutate(n = ifelse(is.na(n), 0, n))  # Fill missing values with 0

# Convert y to a factor to enforce order
full_grid$y <- factor(full_grid$y, levels = custom_y_order)

# Plot heatmap using geom_tile()
ggplot(full_grid, aes(x = x, y = y, fill = n)) +
  geom_tile(color = "black") +  # Add black borders to all tiles
  scale_fill_gradient(low = "white", high = "red") +
  scale_x_continuous(breaks = x_range) +  # Ensure all x-axis ticks are shown
  labs(title = "Heatmap of Ground truth vs. Assignment", 
       x = "Ground truth", 
       y = "Assignment", 
       fill = "Count") +
  theme_minimal()
```

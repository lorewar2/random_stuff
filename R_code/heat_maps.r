
```{r}
library(dplyr)
data <- vireo_over_heat
data <- data %>%
  # Keep only rows where 'donor' is present
  filter(grepl("donor", donor_id)) %>%
  # Extract the number from 'donor_id' and assign it to a new column
  mutate(donor_id = gsub("donor", "", donor_id)) %>%
  # Convert donor_id to numeric
  mutate(donor_id = as.numeric(donor_id))
#data <- data[data$status != "unassigned", ]
#data <- data[data$status != "doublet", ]
data <- data[1:(nrow(data) - 2500),]
ground_truth_clusters <- sub(".*-(\\d+)$", "\\1", data[, 1])
predicted_clusters <- data[, 2]

map_clusters <- function(ground_truth, assigned_cluster) {
  mapping <- tapply(assigned_cluster, ground_truth, function(x) {
    unique_val <- unique(x)
    if (length(unique_val) == 1) return(unique_val)
    return(names(which.max(table(x))))  # Choose the most frequent assigned cluster if multiple
  })
  return(mapping)
}

cluster_mapping <- map_clusters(ground_truth_clusters, predicted_clusters)

print(cluster_mapping)
# Convert names to numeric for proper sorting
sorted_indices <- sort(as.numeric(names(cluster_mapping)))

# Extract values in sorted order as an array
sorted_values <- unname(cluster_mapping[as.character(sorted_indices)])

# Print the sorted values array
print(sorted_values)

custom_y_order <- sorted_values
custom_y_order <- as.numeric(custom_y_order)
custom_y_order[17] = 24
custom_y_order[20] = 34
custom_y_order[38] = 37
custom_y_order[48] = 43
custom_y_order[54] = 50
custom_y_order[56] = 52
#custom_y_order[54] = 32
#custom_y_order[55] = 41
print(custom_y_order)

# Given numbers
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

excluded_x_values <- c(5, 9, 13, 24, 40, 65 ,68)
full_grid <- full_grid[!(full_grid$x %in% excluded_x_values), ]

# Convert x to factor to avoid gaps
full_grid$x <- factor(full_grid$x, levels = sort(unique(full_grid$x)))

ggplot(full_grid, aes(x = x, y = y, fill = n)) +
  geom_tile(color = "black") +
  scale_fill_gradient(low = "blue", high = "red") +
  labs(title = "Vireo Overclus", 
       x = "Ground truth", 
       y = "Assignment", 
       fill = "Count") +
  theme_minimal()

```




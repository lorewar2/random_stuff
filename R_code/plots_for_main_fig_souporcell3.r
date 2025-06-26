
```{r}
# Load required libraries
library(ggplot2)
library(ggforce)  # For geom_circle

# Set seed for reproducibility
set.seed(123)

# Generate 40 random points
n_points <- 20
data <- data.frame(
  x = runif(n_points, 0, 10),
  y = runif(n_points, 0, 10)
)

# Define radius for circles
radius <- 0.5

# Create circle data (centered at each point)
data$radius <- radius

# Plot
ggplot(data) +
  geom_point(aes(x = x, y = y), size = 4, color = "blue") +
  geom_circle(aes(x0 = x, y0 = y, r = radius), color = "red", linetype = "dashed") +
  xlim(-0.5, 10.5) +
  ylim(-0.5, 10.5) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  theme_void() + 
  theme(panel.border = element_blank(),
            axis.line = element_line(colour = "black"),
            axis.line.x = element_line(size = 2, linetype = "solid", colour = "black"),
            axis.line.y = element_line(size = 1, linetype = "solid", colour = "black"))


```

```{r}
# Load required libraries
library(ggplot2)
library(ggforce)  # For geom_circle

# Set seed for reproducibility
set.seed(2)

# Generate 40 random points
n_points <- 4

data <- data.frame(
  x = c(2, 7),
  y = c(4.2, 2)
)

# Define radius for circles
radius <- 0.5

# Create circle data (centered at each point)
data$radius <- radius

# Plot
ggplot(data) +
  geom_point(aes(x = x, y = y), size = 4, color = "blue") +
  geom_circle(aes(x0 = x, y0 = y, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  theme_void() + 
  theme(panel.border = element_blank(),
            axis.line = element_line(colour = "black"),
            axis.line.x = element_line(size = 2, linetype = "solid", colour = "black"),
            axis.line.y = element_line(size = 1, linetype = "solid", colour = "black"))


```
```{r}
# Set seed for reproducibility
# Load required libraries
library(ggplot2)
library(ggforce)  # For geom_circle

# Set seed for reproducibility
set.seed(4)

# Generate 40 random points
n_points <- 4
x_cc = c(8, 2.2, 9.2, 4)
y_cc = c(8, 7.5, 3.4, 4)
data <- data.frame(
  x_cc,
  y_cc
)

x_cc_final = c(1.0, 5.0, 3.3, 8)
y_cc_final = c(2.5, 1.5, 7, 7.8)
points_per_cluster <- 3000
# Generate data around each cluster center
x_data <- c()
y_data <- c()
color_data <- c()
color <- c("grey", "grey", "grey", "grey")
radius_data <- 2.0  # Radius within which data is generated
for (i in 1:4) {
  x_data <- c(x_data, rnorm(points_per_cluster, mean = x_cc_final[i], sd = radius_data / 4))
  y_data <- c(y_data, rnorm(points_per_cluster, mean = y_cc_final[i], sd = radius_data / 4))
  for (j in 1:points_per_cluster) {
    color_data <- c(color_data, color[i])
  }
}
# Circle parameters
x0 <- 5     # center x
y0 <- 5     # center y
r <- 5    # radius
cell_data <- data.frame(x_data, y_data, color_data)
# Filter data: keep points inside the circle
cell_data <- cell_data %>%
  filter((x_data - x0)^2 + (y_data - y0)^2 <= r^2)

# Define radius for circles
radius <- 0.5

# Create circle data (centered at each point)
data$radius <- radius

# Plot
ggplot() +
  geom_point(data = cell_data, aes(x = x_data, y = y_data), size = 2, color = cell_data$color_data) +
  geom_point(data = data, aes(x = x_cc, y = y_cc), size = 4, color = "blue") +
  geom_circle(data = data, aes(x0 = x_cc, y0 = y_cc, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  theme_void() + 
  theme(panel.border = element_blank(),
            axis.line = element_line(colour = "black"),
            axis.line.x = element_line(size = 2, linetype = "solid", colour = "black"),
            axis.line.y = element_line(size = 1, linetype = "solid", colour = "black"))


```
```{r}
# Set seed for reproducibility
# Load required libraries
library(ggplot2)
library(ggforce)  # For geom_circle

# Set seed for reproducibility
set.seed(4)

# Generate 40 random points
n_points <- 4

x_cc = c(8, 3.3, 9.2, 3) 
y_cc = c(7.2, 7, 3.4, 2.5)
radius = 0.5
data <- data.frame(
  x_cc,
  y_cc,
  radius
)

x_cc_final = c(1.0, 5.0, 3.3, 8)
y_cc_final = c(2.5, 1.5, 7, 7.8)
points_per_cluster <- 3000
# Generate data around each cluster center
x_data <- c()
y_data <- c()
color_data <- c()
color <- cluster_colors <- c("Cluster1" = "#1b9e77", 
                    "Cluster2" = "#1b9e77", 
                    "Cluster3" = "#7570b3", 
                    "Cluster4" = "#e6ab02")
radius_data <- 2.0  # Radius within which data is generated
for (i in 1:4) {
  x_data <- c(x_data, rnorm(points_per_cluster, mean = x_cc_final[i], sd = radius_data / 4))
  y_data <- c(y_data, rnorm(points_per_cluster, mean = y_cc_final[i], sd = radius_data / 4))
  for (j in 1:points_per_cluster) {
    color_data <- c(color_data, color[i])
  }
}
# Circle parameters
x0 <- 5     # center x
y0 <- 5     # center y
r <- 5    # radius
cell_data <- data.frame(x_data, y_data, color_data)
# Filter data: keep points inside the circle
cell_data <- cell_data %>%
  filter((x_data - x0)^2 + (y_data - y0)^2 <= r^2)
# Plot
ggplot() +
  geom_point(data = cell_data, aes(x = x_data, y = y_data), size = 2, color = cell_data$color_data) +
  geom_point(data = data, aes(x = x_cc, y = y_cc), size = 4, color = "blue") +
  geom_circle(data = data, aes(x0 = x_cc, y0 = y_cc, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  theme_void() + 
  theme(panel.border = element_blank(),
            axis.line = element_line(colour = "black"),
            axis.line.x = element_line(size = 2, linetype = "solid", colour = "black"),
            axis.line.y = element_line(size = 1, linetype = "solid", colour = "black"))


```


```{r}
# Set seed for reproducibility
# Load required libraries
library(ggplot2)
library(ggforce)  # For geom_circle

# Set seed for reproducibility
set.seed(4)

# Generate 40 random points
n_points <- 4
x_cc = c(2, 7, 3.3, 8)
y_cc = c(4.2, 2, 7, 7.2)

radius = 0.5
data <- data.frame(
  x_cc,
  y_cc,
  radius
)

x_cc_final = c(1.0, 5.0, 3.3, 8)
y_cc_final = c(2.5, 1.5, 7, 7.8)
points_per_cluster <- 3000
# Generate data around each cluster center
x_data <- c()
y_data <- c()
color_data <- c()
color <- c("Cluster1" = "gray", 
                    "Cluster2" = "gray", 
                    "Cluster3" = "#7570b3", 
                    "Cluster4" = "#e6ab02")
radius_data <- 2.0  # Radius within which data is generated
for (i in 1:4) {
  x_data <- c(x_data, rnorm(points_per_cluster, mean = x_cc_final[i], sd = radius_data / 4))
  y_data <- c(y_data, rnorm(points_per_cluster, mean = y_cc_final[i], sd = radius_data / 4))
  for (j in 1:points_per_cluster) {
    color_data <- c(color_data, color[i])
  }
}
# Circle parameters
x0 <- 5     # center x
y0 <- 5     # center y
r <- 5    # radius
cell_data <- data.frame(x_data, y_data, color_data)
# Filter data: keep points inside the circle
cell_data <- cell_data %>%
  filter((x_data - x0)^2 + (y_data - y0)^2 <= r^2)
# Plot
ggplot() +
  geom_point(data = cell_data, aes(x = x_data, y = y_data), size = 2, color = cell_data$color_data) +
  geom_point(data = data, aes(x = x_cc, y = y_cc), size = 4, color = "blue") +
  geom_circle(data = data, aes(x0 = x_cc, y0 = y_cc, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  theme_void() + 
  theme(panel.border = element_blank(),
            axis.line = element_line(colour = "black"),
            axis.line.x = element_line(size = 2, linetype = "solid", colour = "black"),
            axis.line.y = element_line(size = 1, linetype = "solid", colour = "black"))


```

```{r}
# Set seed for reproducibility
# Load required libraries
library(ggplot2)
library(ggforce)  # For geom_circle

# Set seed for reproducibility
set.seed(4)

# Generate 40 random points
n_points <- 4
x_cc = c(1.5, 5.0, 3.3, 8)
y_cc = c(2.5, 1.5, 7, 7.8)
radius = 0.5
data <- data.frame(
  x_cc,
  y_cc,
  radius
)

x_cc_final = c(1.0, 5.0, 3.3, 8)
y_cc_final = c(2.5, 1.5, 7, 7.8)
points_per_cluster <- 3000
# Generate data around each cluster center
x_data <- c()
y_data <- c()
color_data <- c()
color <- c("Cluster1" = "#1b9e77", 
                    "Cluster2" = "#d95f02", 
                    "Cluster3" = "#7570b3", 
                    "Cluster4" = "#e6ab02")
radius_data <- 2.0  # Radius within which data is generated
for (i in 1:4) {
  x_data <- c(x_data, rnorm(points_per_cluster, mean = x_cc_final[i], sd = radius_data / 4))
  y_data <- c(y_data, rnorm(points_per_cluster, mean = y_cc_final[i], sd = radius_data / 4))
  for (j in 1:points_per_cluster) {
    color_data <- c(color_data, color[i])
  }
}
# Circle parameters
x0 <- 5     # center x
y0 <- 5     # center y
r <- 5    # radius
cell_data <- data.frame(x_data, y_data, color_data)
# Filter data: keep points inside the circle
cell_data <- cell_data %>%
  filter((x_data - x0)^2 + (y_data - y0)^2 <= r^2)
# Plot
ggplot() +
  geom_point(data = cell_data, aes(x = x_data, y = y_data), size = 2, color = cell_data$color_data) +
  geom_point(data = data, aes(x = x_cc, y = y_cc), size = 4, color = "blue") +
  geom_circle(data = data, aes(x0 = x_cc, y0 = y_cc, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  theme_void() + 
  theme(panel.border = element_blank(),
            axis.line = element_line(colour = "black"),
            axis.line.x = element_line(size = 2, linetype = "solid", colour = "black"),
            axis.line.y = element_line(size = 1, linetype = "solid", colour = "black"))


```
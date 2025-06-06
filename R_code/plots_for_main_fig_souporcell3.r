
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
radius <- 0.3

# Create circle data (centered at each point)
data$radius <- radius

# Plot
ggplot(data) +
  geom_point(aes(x = x, y = y), size = 2, color = "blue") +
  geom_circle(aes(x0 = x, y0 = y, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  labs(title = "Dots with Circles Around Them")


```

```{r}
# Load required libraries
library(ggplot2)
library(ggforce)  # For geom_circle

# Set seed for reproducibility
set.seed(2)

# Generate 40 random points
n_points <- 2
data <- data.frame(
  x = c(2, 7),
  y = c(5.2, 2)
)

# Define radius for circles
radius <- 0.3

# Create circle data (centered at each point)
data$radius <- radius

# Plot
ggplot(data) +
  geom_point(aes(x = x, y = y), size = 2, color = "blue") +
  geom_circle(aes(x0 = x, y0 = y, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  labs(title = "Dots with Circles Around Them")


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
x_cc = c(8, 2.2, 8.2, 4)
y_cc = c(8, 7.5, 3, 4)
data <- data.frame(
  x_cc,
  y_cc
)

x_cc_final = c(2, 4.5, 3.3, 8)
y_cc_final = c(2, 3, 7, 6)
points_per_cluster <- 10
# Generate data around each cluster center
x_data <- c()
y_data <- c()
color_data <- c()
color <- c("grey", "grey", "grey", "grey")
radius_data <- 1  # Radius within which data is generated
for (i in 1:4) {
  x_data <- c(x_data, rnorm(points_per_cluster, mean = x_cc_final[i], sd = radius_data / 2))
  y_data <- c(y_data, rnorm(points_per_cluster, mean = y_cc_final[i], sd = radius_data / 2))
  for (j in 1:points_per_cluster) {
    color_data <- c(color_data, color[i])
  }
}
cell_data <- data.frame(x_data, y_data, color_data)
# Define radius for circles
radius <- 0.3

# Create circle data (centered at each point)
data$radius <- radius

# Plot
ggplot() +
  geom_point(data = cell_data, aes(x = x_data, y = y_data), size = 2, color = color_data) +
  geom_point(data = data, aes(x = x_cc, y = y_cc), size = 2, color = "blue") +
  geom_circle(data = data, aes(x0 = x_cc, y0 = y_cc, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  labs(title = "Dots with Circles Around Them")


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

x_cc = c(2, 8, 3.3, 7)
y_cc = c(5.2, 6, 7, 2)
radius = c(0.3, 1.2, 1.2, 0.3)
data <- data.frame(
  x_cc,
  y_cc,
  radius
)

x_cc_final = c(2, 4.5, 3.3, 8)
y_cc_final = c(2, 3, 7, 6)
points_per_cluster <- 10
# Generate data around each cluster center
x_data <- c()
y_data <- c()
color_data <- c()
color <- c("grey", "grey", "green", "purple")
radius_data <- 1  # Radius within which data is generated
for (i in 1:4) {
  x_data <- c(x_data, rnorm(points_per_cluster, mean = x_cc_final[i], sd = radius_data / 2))
  y_data <- c(y_data, rnorm(points_per_cluster, mean = y_cc_final[i], sd = radius_data / 2))
  for (j in 1:points_per_cluster) {
    color_data <- c(color_data, color[i])
  }
}
cell_data <- data.frame(x_data, y_data, color_data)
# Plot
ggplot() +
  geom_point(data = cell_data, aes(x = x_data, y = y_data), size = 2, color = color_data) +
  geom_point(data = data, aes(x = x_cc, y = y_cc), size = 2, color = "blue") +
  geom_circle(data = data, aes(x0 = x_cc, y0 = y_cc, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  labs(title = "Dots with Circles Around Them")


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
x_cc = c(2, 4.5, 3.3, 8)
y_cc = c(2, 3, 7, 6)
radius = c(1.2, 1.2, 1.2, 1.2)
data <- data.frame(
  x_cc,
  y_cc,
  radius
)

x_cc_final = c(2, 4.5, 3.3, 8)
y_cc_final = c(2, 3, 7, 6)
points_per_cluster <- 10
# Generate data around each cluster center
x_data <- c()
y_data <- c()
color_data <- c()
color <- c("red", "yellow", "green", "purple")
radius_data <- 1  # Radius within which data is generated
for (i in 1:4) {
  x_data <- c(x_data, rnorm(points_per_cluster, mean = x_cc_final[i], sd = radius_data / 2))
  y_data <- c(y_data, rnorm(points_per_cluster, mean = y_cc_final[i], sd = radius_data / 2))
  for (j in 1:points_per_cluster) {
    color_data <- c(color_data, color[i])
  }
}
cell_data <- data.frame(x_data, y_data, color_data)
# Plot
ggplot() +
  geom_point(data = cell_data, aes(x = x_data, y = y_data), size = 2, color = color_data) +
  geom_point(data = data, aes(x = x_cc, y = y_cc), size = 2, color = "blue") +
  geom_circle(data = data, aes(x0 = x_cc, y0 = y_cc, r = radius), color = "red", linetype = "dashed") +
  xlim(0, 10) +
  ylim(0, 10) + 
  coord_fixed() +  # Ensure circles appear as circles (not ellipses)
  labs(title = "Dots with Circles Around Them")


```
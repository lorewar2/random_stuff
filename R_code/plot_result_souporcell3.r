

```{r}
library(reshape2)
library(ggplot2)
library(gridExtra)
library(ggthemes)
library(grid)

# Duplicate
test1 <- c(3, 2, 1, 0.1)
data <- data.frame(test1)
data$ID <- c("1", "2","3","4")
colors <- c("dodgerblue", "darkgoldenrod1","coral2","chartreuse3")

switch_graph_1 <- ggplot(melt(data), aes(variable, value, fill=ID, group=ID)) +
geom_bar(stat='identity', position='dodge', fill = colors) + 
theme_bw() + 
theme(plot.background=element_rect(fill="grey95", colour="grey95"),
               rect = element_rect(fill = 'grey95')) +
scale_y_continuous(labels = scales::comma, limits=c(0, 11)) +
labs(x = "32 Donors") +
ggtitle("Duplicate Clusters") +
theme(plot.title = element_text(color="black", size=10, face="bold"), axis.ticks.x = element_blank() ,axis.text.x = element_blank(), axis.title.x=element_text(color="black", size=8, face="italic"), axis.title.y=element_blank(), plot.margin = margin(t = 5, r = 5, b = 5, l = 30))

test1 <- c(6, 6, 2, 0.1)
data <- data.frame(test1)
data$ID <- c("1", "2","3","4")
colors <- c("dodgerblue", "darkgoldenrod1","coral2","chartreuse3")

switch_graph_2 <- ggplot(melt(data), aes(variable, value, fill=ID, group=ID)) +
geom_bar(stat='identity', position='dodge', fill = colors) + 
theme_bw() + 
theme(plot.background=element_rect(fill="grey95", colour="grey95"),
               rect = element_rect(fill = 'grey95')) +
scale_y_continuous(labels = scales::comma, limits=c(0, 11)) +
labs(x = "48 Donors") +
ggtitle("") +
theme(plot.title = element_text(color="black", size=10, face="bold"),, axis.ticks.x = element_blank() ,axis.text.x = element_blank(), axis.title.x=element_text(color="black", size=8, face="italic"), axis.title.y=element_blank(), plot.margin = margin(t = 5, r = 5, b = 5, l = 30), axis.text.y = element_blank())

test1 <- c(11, 9, 5, 0.1)
data <- data.frame(test1)
data$ID <- c("1", "2","3","4")
colors <- c("dodgerblue", "darkgoldenrod1","coral2","chartreuse3")

switch_graph_3 <- ggplot(melt(data), aes(variable, value, fill=ID, group=ID)) +
geom_bar(stat='identity', position='dodge', fill = colors) + 
theme_bw() + 
theme(plot.background=element_rect(fill="grey95", colour="grey95"),
               rect = element_rect(fill = 'grey95')) +
scale_y_continuous(labels = scales::comma, limits=c(0, 11)) +
labs(x = "64 Donors") +
ggtitle("") +
theme(plot.title = element_text(color="black", size=10, face="bold"),, axis.ticks.x = element_blank() ,axis.text.x = element_blank(), axis.title.x=element_text(color="black", size=8, face="italic"), axis.title.y=element_blank(), plot.margin = margin(t = 5, r = 5, b = 5, l = 30), axis.text.y = element_blank())


# Rand Index
test1 <- c(0.901, 0.943, 0.997, 0.9999)
data <- data.frame(test1)
data$ID <- c("1", "2","3","4")
colors <- c("dodgerblue", "darkgoldenrod1","coral2","chartreuse3")

switch_graph_4 <- ggplot(melt(data), aes(variable, value, fill=ID, group=ID)) +
geom_bar(stat='identity', position='dodge', fill = colors) + 
theme_bw() + 
theme(plot.background=element_rect(fill="grey95", colour="grey95"),
               rect = element_rect(fill = 'grey95')) +
scale_y_continuous(labels = scales::percent) +
  coord_cartesian(ylim = c(0.79, 1.0))+
labs(x = "32 Donors") +
ggtitle("Rand Index") +
theme(plot.title = element_text(color="black", size=10, face="bold"), axis.ticks.x = element_blank() ,axis.text.x = element_blank(), axis.title.x=element_text(color="black", size=8, face="italic"), axis.title.y=element_blank(), plot.margin = margin(t = 5, r = 5, b = 5, l = 10))

# Rand Index
test1 <- c(0.913, 0.951, 0.9975, 0.9995)
data <- data.frame(test1)
data$ID <- c("1", "2","3","4")
colors <- c("dodgerblue", "darkgoldenrod1","coral2","chartreuse3")

switch_graph_5 <- ggplot(melt(data), aes(variable, value, fill=ID, group=ID)) +
geom_bar(stat='identity', position='dodge', fill = colors) + 
theme_bw() + 
theme(plot.background=element_rect(fill="grey95", colour="grey95"),
               rect = element_rect(fill = 'grey95')) +
scale_y_continuous(labels = scales::percent) +
  coord_cartesian(ylim = c(0.79, 1.0))+
labs(x = "48 Donors") +
ggtitle("") +
theme(plot.title = element_text(color="black", size=10, face="bold"), axis.ticks.x = element_blank() ,axis.text.x = element_blank(), axis.title.x=element_text(color="black", size=8, face="italic"), axis.title.y=element_blank(), axis.text.y = element_blank(),plot.margin = margin(t = 5, r = 5, b = 5, l = 30))

# Rand Index
test1 <- c(0.793, 0.856, 0.9972, 0.99925)
data <- data.frame(test1)
data$ID <- c("1", "2","3","4")
colors <- c("dodgerblue", "darkgoldenrod1","coral2","chartreuse3")

switch_graph_6 <- ggplot(melt(data), aes(variable, value, fill=ID, group=ID)) +
geom_bar(stat='identity', position='dodge', fill = colors) + 
theme_bw() + 
theme(plot.background=element_rect(fill="grey95", colour="grey95"),
               rect = element_rect(fill = 'grey95')) +
scale_y_continuous(labels = scales::percent) +
  coord_cartesian(ylim = c(0.79, 1.0))+
labs(x = "64 Donors") +
ggtitle("") +
theme(plot.title = element_text(color="black", size=10, face="bold"), axis.ticks.x = element_blank() , axis.text.x = element_blank(), axis.text.y = element_blank(), axis.title.x=element_text(color="black", size=8, face="italic"), axis.title.y=element_blank(), plot.margin = margin(t = 5, r = 5, b = 5, l = 30))

# Barplot
# Inserting data 
ODI <- data.frame(Method=c("Vireo", "Vireo w overclus", "Souporcell", "Souporcell3"), 
                   runs=c(5,2,3,4)) 
  
# Assigning colors manually  
test <- ggplot(data=ODI, aes(x=Method, y=runs,fill=Method))+ 
  geom_bar(stat="identity")+ 
  scale_fill_manual(values=c("coral2", "chartreuse3", "dodgerblue", "darkgoldenrod1"))+ 
theme_bw() + 
theme(plot.background=element_rect(fill="grey90", colour="grey90"),
               rect = element_rect(fill = 'grey90')) 
legend <- cowplot::get_legend(test)

figure  <- grid.arrange(switch_graph_1, switch_graph_2, switch_graph_3, legend,  switch_graph_4, switch_graph_5, switch_graph_6, 
          ncol = 7, nrow = 1, widths=c(1,1,1,1,1,1,1), heights=c(1))

grid.roundrect(
  x = 0.5, y = 0.5,         # center of page
  width = 1, height = 1,    # full area
  r = unit(0.05, "snpc"),   # controls the corner radius (adjust as needed)
  gp = gpar(col = "black", fill = NA, lwd = 3)
)
```


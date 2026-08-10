library(SpiecEasi)

# -----------------------------
# Load abundance table
# -----------------------------

abundance <- read.csv(
  "results/filtered_abundance.csv",
  row.names = 1,
  check.names = FALSE
)

cat("Working directory:\n")
print(getwd())

cat("\nInput file exists:\n")
print(file.exists("results/filtered_abundance.csv"))

cat("Rows before transpose:", nrow(abundance), "\n")
cat("Columns before transpose:", ncol(abundance), "\n")

# taxa should be rows
abundance <- as.matrix(abundance)
abundance <- t(abundance)
# -----------------------------
# Remove empty samples
# -----------------------------

# -----------------------------
# Run SPIEC-EASI
# -----------------------------
cat("Samples:", nrow(abundance), "\n")
cat("Taxa:", ncol(abundance), "\n")

se <- spiec.easi(
  abundance,
  method = "mb",
  lambda.min.ratio = 1e-2,
  nlambda = 20
)

# -----------------------------
# Extract adjacency matrix
# -----------------------------

adj <- as.matrix(getRefit(se))
print(class(adj))
print(dim(adj))

taxa_names <- colnames(abundance)

cat("length(taxa_names):", length(taxa_names), "\n")
cat("nrow(adj):", nrow(adj), "\n")
cat("ncol(adj):", ncol(adj), "\n")

stopifnot(length(taxa_names) == nrow(adj))

rownames(adj) <- taxa_names
colnames(adj) <- taxa_names

print(head(rownames(adj)))
print(head(colnames(adj)))
print(head(taxa_names))

identical(rownames(adj), taxa_names)
identical(colnames(adj), taxa_names)

edge_idx <- which(upper.tri(adj) & adj != 0, arr.ind = TRUE)

edge_idx <- edge_idx[edge_idx[,1] < edge_idx[,2], ]

edges <- data.frame(
    taxon1 = rownames(adj)[edge_idx[,1]],
    taxon2 = colnames(adj)[edge_idx[,2]],
    weight = 1,
    significant = TRUE
)

write.csv(edges,
          "results/spiec_easi_edges.csv",
          row.names = FALSE)

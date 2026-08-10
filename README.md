# Microbiome Network Analysis

Code accompanying:

"Effects of Data Transformation and Network-Inference Method
on Microbiome Association Networks"

## Overview

Hello! This repository contains all the data, code, and figures used in my project. Below is a rough analysis pipeline. 

## Analysis pipeline

1. Preprocess the curatedMetagenomicData HMP dataset.
2. Apply prevalence filtering.
3. Construct Relative Pearson and Relative Spearman networks.
4. Apply CLR transformation.
5. Construct CLR Pearson and CLR Spearman networks.
6. Construct the SPIEC-EASI network in R.
7. Calculate network topology statistics.
8. Calculate edge and hub Jaccard similarity.
9. Analyze edge-sign composition.
10. Generate the figures and tables used in the paper.

Ran on:
Python version [3.13.7]
R version [4.6.0] 

...

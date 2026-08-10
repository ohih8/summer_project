# Microbiome Network Analysis

Code accompanying:

"Effects of Data Transformation and Network-Inference Method
on Microbiome Association Networks"

## Overview

This repository contains the code used to preprocess the HMP
microbiome dataset, construct five microbial association networks,
calculate network statistics, compare networks, and generate the
figures used in the paper.

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
Python 3.13.7
R 4.6.0 

...
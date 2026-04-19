# Enhanced DOA Algorithm for Crop Partition Optimization

## Overview

This project focuses on researching and developing an enhanced metaheuristic optimization algorithm for agricultural land allocation and crop partition planning.

The work is based on the **Tyrannosaurus Optimization Algorithm (TROA)** and redesigned into a modified version named **Dilophosaurus Optimization Algorithm (DOA)**.

The proposed algorithm is applied to solve crop allocation problems where farmland must be efficiently divided among multiple crop types while satisfying optimization objectives such as productivity, resource utilization, and land efficiency.

---

## Motivation

Traditional optimization methods often struggle with:

- Large search spaces  
- Multiple constraints  
- Nonlinear agricultural planning objectives  
- Local optimum stagnation  

Metaheuristic algorithms provide flexible and effective alternatives for solving these complex real-world problems.

This project explores how an improved population-based optimization method can generate better land allocation solutions.

---

## Main Contributions

- Studied and analyzed the original **TROA** algorithm  
- Redesigned search/update mechanisms into a new **DOA** variant  
- Applied DOA to crop partition and land allocation optimization  
- Evaluated solution quality under multiple experimental scenarios  
- Compared convergence behavior and computational efficiency  

---

## Problem Statement

Given:

- Limited agricultural land area  
- Multiple crop candidates  
- Different crop benefits / yields / constraints  

Find an optimal crop distribution plan that maximizes total objective value while maintaining feasible land partitioning.

---

## Algorithm Workflow

1. Initialize population of candidate crop allocation solutions  
2. Evaluate objective fitness  
3. Update positions using modified DOA search strategy  
4. Balance exploration and exploitation  
5. Iterate until stopping condition  
6. Return best crop partition solution  

---

## Technologies Used

- Python  
- NumPy  
- Matplotlib  
- Jupyter Notebook  

---

## Project Structure

```bash
DOA_crop/
│── main.py
│── doa.py
│── objective.py
│── datasets/
│── results/
│── visualization/
│── README.md

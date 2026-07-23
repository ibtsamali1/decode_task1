# Project 2: Data Classification Using AI

**DecodeLabs Industrial Training Kit — Batch 2026**

A supervised learning pipeline that trains a K-Nearest Neighbors classifier
on an e-commerce orders dataset to predict order outcomes (`OrderStatus`),
built to satisfy the Project 2 brief: load a dataset, split it into
train/test sets, apply a classification algorithm, and evaluate it properly
(confusion matrix + F1, not just raw accuracy).

---

## Table of Contents

- [Overview](#overview)
- [Project Goal (per brief)](#project-goal-per-brief)
- [Repository Contents](#repository-contents)
- [Dataset](#dataset)
- [Requirements & Installation](#requirements--installation)
- [How to Run](#how-to-run)
- [Pipeline Walkthrough](#pipeline-walkthrough)
- [Results](#results)
- [Interpreting the Results](#interpreting-the-results)
- [Project Structure](#project-structure)
- [Possible Extensions](#possible-extensions)
- [Skills Demonstrated](#skills-demonstrated)
- [Author / Contact](#author--contact)

---

## Overview

This project follows the **INPUT → PROCESS → OUTPUT** framework taught in
the DecodeLabs Project 2 training deck, applied to a real dataset
(`Copy_of_Dataset_for_Data_Analytics.xlsx`, 1,200 e-commerce orders) instead
of the toy Iris flower example used in the slides. The same core ideas apply:

1. Load and understand tabular data.
2. Encode categorical features and scale numeric ones.
3. Split into training and test sets (stratified, shuffled).
4. Train a K-Nearest Neighbors classifier, tuning K via an elbow curve.
5. Evaluate with a confusion matrix, precision, recall, and F1 — not just
   accuracy, since accuracy alone can be misleading ("Accuracy Mirage").

## Project Goal (per brief)

> Build a basic classification model using a small dataset.

**Key Requirements (all met):**
- [x] Load and understand a dataset
- [x] Split data into training and testing sets
- [x] Apply a simple classification algorithm
- [x] Evaluate beyond raw accuracy (confusion matrix, F1 score)

**Key Skills demonstrated:** data handling, supervised learning basics, model
training, feature engineering, model evaluation.

## Repository Contents

| File | Description |
|---|---|
| `classification_pipeline.py` | Full, runnable Python pipeline — load, clean, encode, scale, split, train, tune, evaluate |
| `Project2_Report.md` | Write-up of methodology, results, and interpretation |
| `elbow_curve.png` | Error rate vs. K, used to select the best K for KNN |
| `confusion_matrix.png` | Confusion matrix of the final model on the test set |
| `results_summary.txt` | Plain-text dump of accuracy, F1 scores, and the full classification report |
| `README.md` | This file |

## Dataset

**Source file:** `Copy_of_Dataset_for_Data_Analytics.xlsx`
**Shape:** 1,200 rows × 14 columns

| Column | Type | Notes |
|---|---|---|
| OrderID | string | Unique identifier — dropped before modeling |
| Date | datetime | Split into `OrderMonth` and `OrderDayOfWeek` |
| CustomerID | string | Near-unique identifier — dropped |
| Product | categorical | Printer, Tablet, Chair, Laptop, Desk, Monitor, Phone |
| Quantity | int | 1–5 |
| UnitPrice | float | 11.39–699.93 |
| ShippingAddress | string | Street number only in this dataset — dropped (no real geo signal) |
| PaymentMethod | categorical | Online, Cash, Credit Card, Debit Card, Gift Card |
| **OrderStatus** | categorical | **Target** — Cancelled, Returned, Pending, Shipped, Delivered |
| TrackingNumber | string | Unique identifier — dropped |
| ItemsInCart | int | 1–10 |
| CouponCode | categorical | SAVE10, FREESHIP, WINTER15, or missing (→ filled as `"NONE"`) |
| ReferralSource | categorical | Instagram, Email, Google, Facebook, Referral |
| TotalPrice | float | 11.39–3456.40 |

**Target class balance** (nearly perfectly even — no class imbalance to
worry about):

```
Cancelled    250
Returned     247
Pending      237
Shipped      235
Delivered    231
```

**Missing data:** Only `CouponCode` has nulls (309 rows), which simply means
no coupon was applied — filled with the string `"NONE"` rather than dropped.

## Requirements & Installation

- Python 3.8+
- Dependencies: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `openpyxl`

Install everything with:

```bash
pip install pandas numpy scikit-learn matplotlib openpyxl
```

(If you're on a system that requires it, e.g. Debian/Ubuntu with an
externally-managed Python environment:)

```bash
pip install pandas numpy scikit-learn matplotlib openpyxl --break-system-packages
```

## How to Run

1. Place `Copy_of_Dataset_for_Data_Analytics.xlsx` in the same directory as
   `classification_pipeline.py` (or update the file path at the top of the
   script's data-loading line).
2. Run the script:

```bash
python3 classification_pipeline.py
```

3. Outputs generated in the working directory:
   - `elbow_curve.png`
   - `confusion_matrix.png`
   - `results_summary.txt`
   - Full metrics also printed to the console.

**Note:** The script currently points to
`/mnt/user-data/uploads/Copy_of_Dataset_for_Data_Analytics.xlsx`. Change the
path in the `pd.read_excel(...)` line near the top of the file if you're
running this outside that environment.

## Pipeline Walkthrough

### 1. INPUT — Load & Prepare
- Read the Excel file with `pandas.read_excel`.
- Inspect shape, target class balance, and missing values.
- Drop identifier columns with no predictive value: `OrderID`,
  `CustomerID`, `TrackingNumber`, `ShippingAddress`.
- Engineer `OrderMonth` and `OrderDayOfWeek` from `Date`, then drop `Date`.
- Fill missing `CouponCode` values with `"NONE"`.
- One-hot encode categoricals (`Product`, `PaymentMethod`, `CouponCode`,
  `ReferralSource`) → 23 total features.
- Label-encode the target (`OrderStatus`) into integers.

### 2. PROCESS — Split, Scale, Tune, Train
- **Train/test split:** 80/20, `stratify=y` to preserve class balance,
  `shuffle=True` to remove any row-order bias, `random_state=42` for
  reproducibility.
- **Scaling:** `StandardScaler` fit on the training set only (to avoid data
  leakage) and applied to both train and test sets — puts every numeric
  feature on the same scale (mean 0, variance 1) so no single feature
  dominates KNN's distance calculation.
- **Choosing K:** Sweeps K = 1 through 30, records the test-set error rate
  at each K, and picks the K with the lowest error (the "elbow"). Plotted in
  `elbow_curve.png`.
- **Training:** `KNeighborsClassifier(n_neighbors=best_k)` fit on the scaled
  training data.

### 3. OUTPUT — Predict & Evaluate
- Generate predictions on the held-out test set.
- Compute **accuracy**, **macro F1**, and **weighted F1**.
- Print a full `classification_report` (precision/recall/F1 per class).
- Plot and save a **confusion matrix** (`confusion_matrix.png`) to visualize
  exactly which classes get confused with which.
- Save all numeric results to `results_summary.txt`.

## Results

| Metric | Score |
|---|---|
| Best K (via elbow method) | 2 |
| Accuracy | 22.9% |
| F1 (macro avg) | 0.207 |
| F1 (weighted avg) | 0.208 |

| Class | Precision | Recall | F1-score |
|---|---|---|---|
| Cancelled | 0.28 | 0.46 | 0.35 |
| Delivered | 0.18 | 0.24 | 0.21 |
| Pending | 0.23 | 0.26 | 0.24 |
| Returned | 0.22 | 0.14 | 0.17 |
| Shipped | 0.17 | 0.04 | 0.07 |

See `confusion_matrix.png` for the full breakdown and `results_summary.txt`
for the raw numbers.

## Interpreting the Results

With 5 balanced classes, random guessing already scores **~20% accuracy**.
This model reached **22.9%** — barely above chance.

This is not a coding error; it's the model honestly reporting that **order
attributes like quantity, price, product, payment method, referral source,
and order timing carry little to no real signal about whether an order ends
up Cancelled, Returned, Pending, Shipped, or Delivered** in this dataset.
That outcome is more plausibly driven by factors not captured here (e.g.
warehouse logistics, carrier delays, fraud/payment review) — or wasn't
built into the data generation process at all.

This mirrors the training deck's own conclusion: a textbook dataset like
Iris hits ~95%+ accuracy because its features genuinely separate the
classes; this dataset shows the opposite, equally valid case. Recognizing
*and explaining* that gap — rather than reporting a number in a vacuum — is
the actual skill this project exercises.

## Project Structure

```
.
├── classification_pipeline.py   # Full pipeline (load → clean → encode →
│                                 #   scale → split → tune K → train → evaluate)
├── Project2_Report.md            # Detailed write-up of methodology & findings
├── elbow_curve.png                # K vs. error rate
├── confusion_matrix.png           # Final model's confusion matrix
├── results_summary.txt            # Raw metrics + classification report
└── README.md                      # This file
```

## Possible Extensions

- **Try a different target:** Predict `Product` or `PaymentMethod` instead
  of `OrderStatus` — these may correlate more strongly with `UnitPrice` /
  `TotalPrice`, giving KNN a real boundary to learn (useful contrast case).
- **Compare algorithms:** Add a `DecisionTreeClassifier` or
  `LogisticRegression` alongside KNN and compare F1 scores side by side.
- **Feature importance:** Use a tree-based model to rank which features (if
  any) actually carry signal toward `OrderStatus`.
- **Cross-validation:** Replace the single 80/20 split with k-fold CV for a
  more robust estimate of model performance.
- **Hyperparameter search:** Extend the K sweep into a full
  `GridSearchCV` over K, distance metric, and weighting scheme.

## Skills Demonstrated

- Data loading and inspection (`pandas`, `openpyxl`)
- Data cleaning (handling missing values, dropping non-informative columns)
- Feature engineering (date decomposition, one-hot encoding)
- Feature scaling (`StandardScaler`) and train/test splitting with
  stratification
- Supervised learning with K-Nearest Neighbors (`scikit-learn`)
- Hyperparameter tuning via an elbow-curve sweep
- Model evaluation beyond accuracy: confusion matrix, precision, recall, F1
- Honest interpretation of a low-signal result rather than over-claiming
  model performance

## Author / Contact

Prepared as part of the DecodeLabs AI Internship, Project 2 — Data
Classification Using AI.

📞 +91 89330 06408
✉ decodelabs.tech@gmail.com
🌎 www.decodelabs.tech
📍 Greater Lucknow, India

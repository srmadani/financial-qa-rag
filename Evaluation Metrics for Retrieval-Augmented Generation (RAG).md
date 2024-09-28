This document explains various evaluation metrics used to assess the performance of retrieval systems, especially in the context of answering financial questions based on a 10-K question-answer dataset.

*This material is based on data from [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/03-vector-search/eval/evaluation-metrics.md).*

---

## Introduction

In a Retrieval-Augmented Generation (RAG) system, a retriever finds relevant documents from a collection (like 10-K filings), and a language model generates answers using this information. Evaluating the retriever is crucial because the quality of the retrieved documents directly affects the accuracy of the generated answers.

---

## Metrics Overview

1. [Precision at k (P@k)](#1-precision-at-k-pk)
2. [Recall](#2-recall)
3. [Mean Average Precision (MAP)](#3-mean-average-precision-map)
4. [Normalized Discounted Cumulative Gain (NDCG)](#4-normalized-discounted-cumulative-gain-ndcg)
5. [Mean Reciprocal Rank (MRR)](#5-mean-reciprocal-rank-mrr)
6. [F1 Score](#6-f1-score)
7. [Area Under the ROC Curve (AUC-ROC)](#7-area-under-the-roc-curve-auc-roc)
8. [Mean Rank (MR)](#8-mean-rank-mr)
9. [Hit Rate (HR) or Recall at k](#9-hit-rate-hr-or-recall-at-k)
10. [Expected Reciprocal Rank (ERR)](#10-expected-reciprocal-rank-err)

---

### 1. Precision at k (P@k)

**What it measures:** Out of the top **k** results returned by the retriever, how many are actually relevant?

**Formula:**

$$
P@k = \frac{\text{Number of relevant documents in top } k}{k}
$$

**Example:**

- **Scenario:** You're retrieving documents to answer "What are the company's main revenue sources?"
- **Top 5 retrieved documents (k=5):**
  1. Section on "Revenue Streams" (relevant)
  2. "Executive Profiles" section (not relevant)
  3. "Market Analysis" section (not relevant)
  4. "Revenue Recognition Policies" (relevant)
  5. "Financial Statements" (relevant)
- **Calculation:** 3 relevant documents out of 5.
- **P@5 = 3/5 = 0.6**

---

### 2. Recall

**What it measures:** Out of all the relevant documents available, how many did the retriever find?

**Formula:**

$$
\text{Recall} = \frac{\text{Number of relevant documents retrieved}}{\text{Total number of relevant documents}}
$$

**Example:**

- **Total relevant documents on "Revenue Sources":** 10
- **Retriever found:** 6 relevant documents.
- **Calculation:** 6 out of 10 relevant documents.
- **Recall = 6/10 = 0.6**

---

### 3. Mean Average Precision (MAP)

**What it measures:** The average precision across multiple queries.

**Formula:**

$$
\text{MAP} = \frac{1}{Q} \sum_{q=1}^{Q} \text{Average Precision for query } q
$$

**Example:**

- **Queries and their average precisions:**
  - Query 1: 0.7
  - Query 2: 0.8
  - Query 3: 0.6
- **Calculation:** (0.7 + 0.8 + 0.6) / 3
- **MAP = 0.7**

---

### 4. Normalized Discounted Cumulative Gain (NDCG)

**What it measures:** How well the retriever ranks the documents, giving more importance to higher-ranked positions.

**Formula:**

$$
\text{NDCG} = \frac{\text{DCG}}{\text{IDCG}}
$$

Where:

$$
\text{DCG} = \sum_{i=1}^{p} \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}
$$

- $$ \text{rel}_i $$ is the relevance score at position $$ i $$.
- $$ \text{IDCG} $$ is the ideal DCG with perfect ranking.

**Example:**

- **Relevance scores for top 3 documents:**
  1. Highly relevant (score 3)
  2. Not relevant (score 0)
  3. Moderately relevant (score 2)
- **Interpretation:** NDCG reflects that the most relevant documents should be at the top.

---

### 5. Mean Reciprocal Rank (MRR)

**What it measures:** The average of the reciprocal ranks of the first relevant document for each query.

**Formula:**

$$
\text{MRR} = \frac{1}{Q} \sum_{q=1}^{Q} \frac{1}{\text{Rank of first relevant document in query } q}
$$

**Example:**

- **First relevant document positions:**
  - Query 1: Position 2
  - Query 2: Position 1
  - Query 3: Position 4
- **Calculation:** (1/2 + 1/1 + 1/4) / 3
- **MRR ≈ 0.58**

---

### 6. F1 Score

**What it measures:** The balance between precision and recall.

**Formula:**

$$
F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
$$

**Example:**

- **Precision:** 0.7
- **Recall:** 0.5
- **Calculation:** $$ 2 \times \frac{0.7 \times 0.5}{0.7 + 0.5} $$
- **F1 Score ≈ 0.58**

---

### 7. Area Under the ROC Curve (AUC-ROC)

**What it measures:** The ability of the retriever to distinguish between relevant and irrelevant documents.

**Interpretation:**

- **AUC of 0.5:** No discrimination (random chance).
- **AUC of 1.0:** Perfect discrimination.

**Example:**

- **AUC Score:** 0.85
- **Meaning:** There's an 85% chance that the retriever ranks a relevant document higher than a non-relevant one.

---

### 8. Mean Rank (MR)

**What it measures:** The average position of the first relevant document across all queries.

**Formula:**

$$
\text{Mean Rank} = \frac{\sum_{q=1}^{Q} \text{Rank of first relevant document in query } q}{Q}
$$

**Example:**

- **First relevant document positions:**
  - Query 1: Position 3
  - Query 2: Position 2
  - Query 3: Position 5
- **Calculation:** (3 + 2 + 5) / 3
- **Mean Rank ≈ 3.33**

---

### 9. Hit Rate (HR) or Recall at k

**What it measures:** The proportion of queries where at least one relevant document is retrieved in the top **k** results.

**Formula:**

$$
\text{HR@k} = \frac{\text{Number of queries with a relevant document in top } k}{Q}
$$

**Example:**

- **Total queries:** 20
- **Queries with relevant document in top 5:** 15
- **Calculation:** 15 / 20
- **HR@5 = 0.75**

---

### 10. Expected Reciprocal Rank (ERR)

**What it measures:** The probability that a user finds a relevant document at each position, assuming they might stop searching after finding it.

**Formula:**

$$
\text{ERR} = \sum_{i=1}^{n} \frac{1}{i} \left( \prod_{j=1}^{i-1} (1 - r_j) \right) r_i
$$

- $$ r_i $$ is the relevance probability at position $$ i $$.

**Example:**

- **Relevance probabilities:**
  - Position 1: 0.2
  - Position 2: 0.5
  - Position 3: 0.8
- **Interpretation:** Higher ERR means users are likely to find relevant information sooner.

---

## Conclusion

Understanding these metrics helps evaluate the retriever's performance in a RAG system. By optimizing these metrics, especially when answering financial questions using 10-K filings, we can improve the accuracy and reliability of the system.

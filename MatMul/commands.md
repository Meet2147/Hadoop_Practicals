# 🚀 Matrix Multiplication with Hadoop Streaming and Python

Matrix multiplication is a fundamental operation in data science, machine learning, and scientific computing. But what happens when the matrices are so large that they don’t fit on a single machine? This is where **Hadoop MapReduce** comes in.  

In this post, we’ll implement **matrix multiplication using Python and Hadoop Streaming**, step by step, with working code, sample input, and execution commands.

---

## 🔹 Why Hadoop for Matrix Multiplication?
- **Scalability**: Distributes the computation across multiple nodes.
- **Fault Tolerance**: Handles node failures automatically.
- **Sparsity Handling**: Works efficiently with sparse matrices by only storing nonzero elements.

---

## 🔹 Input Format
We represent both matrices as text, where each line is:

```
matrix_name,row_index,col_index,value
```

Example:

```
A,0,1,2
B,1,0,9
```

- `A` and `B` are matrix names.
- `row_index` and `col_index` specify the position.
- `value` is the numeric entry.

---

## 🔹 Sample Matrices
Let’s multiply:

\[
A = \begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}, \quad
B = \begin{bmatrix}
7 & 8 \\
9 & 10 \\
11 & 12
\end{bmatrix}
\]

Expected result:

\[
C = A \times B =
\begin{bmatrix}
58 & 64 \\
139 & 154
\end{bmatrix}
\]

### Sample Input (`sample_input.txt`)
```text
# matrix,row,col,value
A,0,0,1
A,0,1,2
A,0,2,3
A,1,0,4
A,1,1,5
A,1,2,6
B,0,0,7
B,0,1,8
B,1,0,9
B,1,1,10
B,2,0,11
B,2,1,12
```

---

## 🔹 Mapper Code (`mapper.py`)
```python
#!/usr/bin/env python3
import os, sys

# Matrix dimensions passed via environment variables
MAX_I = int(os.environ["MAX_I"])  # Rows of A
MAX_K = int(os.environ["MAX_K"])  # Cols of B

for raw in sys.stdin:
    line = raw.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split(',')
    if len(parts) != 4:
        continue

    name, r, c, v = parts
    r, c, v = int(r), int(c), float(v)

    if name.upper() == 'A':
        for k_idx in range(MAX_K):
            print(f"{r},{k_idx}\tA,{c},{v}")
    elif name.upper() == 'B':
        for i_idx in range(MAX_I):
            print(f"{i_idx},{c}\tB,{r},{v}")
```

---

## 🔹 Reducer Code (`reducer.py`)
```python
#!/usr/bin/env python3
import sys
from collections import defaultdict

current_key = None
Avals = defaultdict(float)
Bvals = defaultdict(float)

def flush(key, A, B):
    if not key:
        return
    total = 0.0
    for j, a in A.items():
        if j in B:
            total += a * B[j]
    if total != 0.0:
        i, k = key
        print(f"{i} {k} {total}")

for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue
    key_str, payload = line.split('\t', 1)
    i, k = map(int, key_str.split(','))
    src, j_str, v_str = payload.split(',', 2)
    j, v = int(j_str), float(v_str)

    if current_key != (i, k):
        flush(current_key, Avals, Bvals)
        current_key = (i, k)
        Avals.clear(); Bvals.clear()

    if src == 'A':
        Avals[j] += v
    else:
        Bvals[j] += v

flush(current_key, Avals, Bvals)
```

---

## 🔹 Running on Hadoop

### Step 1: Upload input file
```bash
hdfs dfs -mkdir -p /data/matmul/input
hdfs dfs -put -f sample_input.txt /data/matmul/input/
```

### Step 2: Run the job
Make scripts executable:
```bash
chmod +x mapper.py reducer.py
```

Run Hadoop Streaming:
```bash
export STREAMING_JAR=/usr/lib/hadoop-mapreduce/hadoop-streaming.jar

hadoop jar "$STREAMING_JAR" \
  -D mapreduce.job.name="Matrix-Multiplication" \
  -D mapreduce.job.reduces=2 \
  -cmdenv MAX_I=2 \
  -cmdenv MAX_K=2 \
  -files mapper.py,reducer.py \
  -mapper mapper.py \
  -reducer reducer.py \
  -input /data/matmul/input/ \
  -output /data/matmul/output/
```

### Step 3: View results
```bash
hdfs dfs -cat /data/matmul/output/part-*
```

Expected output:
```
0 0 58.0
0 1 64.0
1 0 139.0
1 1 154.0
```

---

## 🔹 Key Takeaways
- Hadoop can distribute even fundamental operations like matrix multiplication across clusters.
- This method is **sparse-friendly** — only nonzero entries are stored and processed.
- Passing dimensions via environment variables (`MAX_I`, `MAX_K`) keeps the mapper generic.
- For huge matrices, a two-stage “join-on-k” MapReduce approach is often more efficient.

---

## 🔹 Final Thoughts
Matrix multiplication in Hadoop may not be as fast as specialized libraries like NumPy or Spark MLlib on small datasets, but it’s an excellent exercise in learning **distributed computing fundamentals**.  

This approach helps you understand **how to break down mathematical operations into MapReduce steps**, which is exactly how large-scale ML pipelines operate under the hood.  

---

✨ Thanks for reading! If you found this useful, consider sharing it with others exploring Hadoop + Python.  

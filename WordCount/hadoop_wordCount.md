
# 🔤 Word Count with Hadoop Streaming (Python)

The classic *Word Count* program is a perfect first MapReduce job. This post gives you a copy‑pasteable mapper and reducer in Python, plus commands to run it on Hadoop Streaming and a quick local test.

---

# 📖 Theory: Hadoop Word Count  

## 🔹 What is Word Count?  
The *Word Count* program is the **“Hello World”** of distributed computing. It takes a large collection of text files as input and counts how many times each word appears across the dataset.  

For example:  

Input:
```
Hello Hadoop
Hello World
```
Output:
```
hello    2
hadoop   1
world    1
```

---

## 🔹 Why Word Count in Hadoop?  
- It’s **simple to understand**: just counting words.  
- It demonstrates **how MapReduce works**: breaking tasks into `map`, `shuffle/sort`, and `reduce`.  
- It can be scaled to **massive datasets** (think terabytes of logs, books, or documents).  

---

## 🔹 MapReduce Workflow in Word Count  

### 1. **Map Phase**  
- Each input line is split into words (tokenization).  
- For each word, emit a `(word, 1)` key-value pair.  

Example (input line: `"Hello Hadoop"`):  
```
("hello", 1)
("hadoop", 1)
```

### 2. **Shuffle and Sort Phase**  
- Hadoop automatically groups all values by key (word).  
- All pairs for `"hello"` are brought together, all pairs for `"hadoop"` are grouped, and so on.  

From multiple mappers, Hadoop ensures:  
```
hello  [1, 1, 1, ...]
hadoop [1, 1, ...]
world  [1, ...]
```

### 3. **Reduce Phase**  
- The reducer sums the list of counts for each word.  
- Produces final `(word, total_count)` output.  

Example:
```
hello  -> 2
hadoop -> 1
world  -> 1
```

---

## 🔹 Advantages of Word Count in Hadoop  
1. **Scalability**: Can process billions of words across clusters.  
2. **Fault tolerance**: If a node fails, Hadoop reassigns tasks.  
3. **Parallelism**: Multiple mappers work on different chunks of data at the same time.  
4. **Real-world relevance**: Same logic is extended for log analysis, indexing, and analytics.  

---

## 🔹 Word Count in Hadoop Ecosystem  
- **HDFS** stores the text files.  
- **MapReduce** (with Python via Hadoop Streaming, or Java) performs the counting.  
- **YARN** manages job scheduling and cluster resources.  
- Output can be stored back in **HDFS** or fed into Hive, Pig, or Spark for further analytics.  

---

## 🔹 Key Takeaway  
The Hadoop Word Count program illustrates:  
- **Mapping** raw data into key-value pairs,  
- **Shuffling/Sorting** to group by key,  
- **Reducing** values to aggregate results.  

This three-step paradigm underpins **all Hadoop jobs** — whether it’s counting words, analyzing logs, or running ML preprocessing on large datasets.  

✨ In short: *Word Count is simple, but it demonstrates the heart of distributed data processing.*  

---

## 🧱 Project layout

```
wordcount/
├─ mapper.py
├─ reducer.py
└─ sample.txt
```

---

## ✍️ Mapper (`mapper.py`)

```python
#!/usr/bin/env python3
import sys
import re

WORD_RE = re.compile(r"[A-Za-z0-9']+")

for raw in sys.stdin:
    line = raw.strip().lower()
    if not line:
        continue
    for word in WORD_RE.findall(line):
        # emit "word\t1"
        print(f"{word}\t1")
```

---

## ➕ Reducer (`reducer.py`)

```python
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue
    try:
        word, count_str = line.split("\t", 1)
        count = int(count_str)
    except ValueError:
        # skip malformed line
        continue

    if current_word is None:
        current_word = word

    if word != current_word:
        # flush previous
        print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = 0

    current_count += count

# flush last key
if current_word is not None:
    print(f"{current_word}\t{current_count}")
```

---

## 🧪 Sample input (`sample.txt`)

```
To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them.
```

Expected top words (roughly): `to`, `the`, `be`, `or`, `of`, ...

---

## 🏃 Run on Hadoop Streaming

1) **Make scripts executable**
```bash
chmod +x mapper.py reducer.py
```

2) **Put data on HDFS**
```bash
hdfs dfs -mkdir -p /data/wordcount/input
hdfs dfs -put -f sample.txt /data/wordcount/input/
```

3) **Run the job** (set your streaming JAR path)
```bash
export STREAMING_JAR=/usr/lib/hadoop-mapreduce/hadoop-streaming.jar

hadoop jar "$STREAMING_JAR"   -D mapreduce.job.name="WordCount"   -D mapreduce.job.reduces=2   -files mapper.py,reducer.py   -mapper mapper.py   -reducer reducer.py   -input /data/wordcount/input/   -output /data/wordcount/output/
```

If the output path exists, clear it first:
```bash
hdfs dfs -rm -r -f /data/wordcount/output/
```

4) **View results**
```bash
hdfs dfs -cat /data/wordcount/output/part-*
```

---

## 🧪 Quick local test (no Hadoop)

Useful for debugging your mapper/reducer logic:
```bash
cat sample.txt | ./mapper.py | sort | ./reducer.py | sort -k2nr | head
```

---

## ⚡ Optional: Combiner for speed

For WordCount, the reducer can also serve as a **combiner** to pre‑aggregate counts on mapper nodes and reduce shuffle size:

```bash
hadoop jar "$STREAMING_JAR"   -D mapreduce.job.name="WordCount+Combiner"   -D mapreduce.job.reduces=2   -files mapper.py,reducer.py   -mapper mapper.py   -combiner reducer.py   -reducer reducer.py   -input /data/wordcount/input/   -output /data/wordcount/output/
```

---

## 🧹 Optional refinements

- **Stopwords:** filter very common words (`the`, `to`, `and`, ...).  
- **Unicode:** switch the regex to `\w+` with the `re.UNICODE` flag for broader language support.  
- **Tokenization:** use `nltk` or `spacy` for language‑aware tokenization (more overhead).  
- **Case handling:** current mapper lowercases; adjust if you want case-sensitive counts.

---

## ✅ TL;DR

- Mapper emits `word \t 1` for each token.  
- Reducer sums counts per word.  
- Add a combiner to shrink shuffle traffic and go faster.  

Happy Hadooping! 🚀

First things first:
1. `python3 -m venv .env`
2. `source .env/bin/activate`
3. `pip3 install -r requirements.txt`


The crawler is designed for asynchronous web scraping and cleaning of data feeds. The following command fetches and cleans the content from each URLs listed in file provided by `--feed-path`, removing unnecessary HTML tags, sripts, styles, and whitespaces. The cleaned content along with the original URLs are saved into `output.parquet`.
```
python3 crawler.py --feed-path=data/feed.txt
```

This command indexes from the parquet file specified by the `--parquet-path` argument, followed by searching fo the content related by the given query `--query` within the indexes using the BM25 scoring mechanism.
```
python3 main.py --parquet-path=output.parquet --query="What is deep learning?"
```

## Theory


Term Frequency, $f(q_i, D)$ is count of how many times a particular query term $q_i$, appears in a document $D$, in the context of BM25, term frequency is used to determine how relevant a term is within a specific document.

Inverse Document Frequency: 
$$IDF(q_i)=\log\left(\frac{N-n(q_i)+0.5}{n(q_i)+0.5}+1\right)$$
where, $N$ is the total number of documents, and $n(q_i)$ is the number of documents that contain the term $q_i$. The constants 0.5 are added to prevent dvision by zero and to reduce the weight of terms that are too rare. 

**BM25 uses IDF to measure how much information a given term provides. It is based on how common or rare the term is across all documents.**

The BM25 score for a document $D$ given a query $Q$ is calculated as:
$$\text{Score}(D, Q) = \sum_{i=1}^nIDF(q_i)\frac{f(q_i,D)(k_1+1)}{f(q_i,D)+k_1(1-b+b\frac{|D|}{\text{avgdl}})}$$

The normalization parameters:

- $k_1$: This parameter controls how much the term frequency $f(q_i, D)$ is scaled. It affects the sensitivity of TF to the BM25 score. A higher $k_1$ increases the influence of T, upto a point dictated by the stauration function. Typical values are between 1.2 and 2.0

- $b$: This parameter controls the degree of length normalization applied to the TF. A value of 0 implies no normalization (making the assumption that all documents are of equal length), while a value of 1 implies full normalization, heavily penalizing or rewarding documents based on their deviation from the average document length. The typical value is 0.75, offering a balance that moderately considers document length.

## TODO

- Make ui for this
- Concurrent crawling and indexing
- Other ranking mechanisms such as PageRank
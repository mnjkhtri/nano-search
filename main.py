import pandas as pd
import argparse
from src.engine import SearchEngine

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet-path")
    parser.add_argument("--query")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    engine = SearchEngine()
    contents_df = pd.read_parquet(args.parquet_path)
    engine.index_from_df(contents_df)
    top_10 = engine.search_top_10(args.query)
    for url, score in top_10: print(url, score)
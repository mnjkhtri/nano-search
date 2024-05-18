import re
import asyncio
import aiohttp
import argparse
import pandas as pd
from bs4 import BeautifulSoup

async def process_feed(feed_url, session):
    try:
        async with session.get(feed_url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, "lxml-xml")
            for script in soup(["script", "style"]): script.extract()
            # Strip away HTML tags:
            text = soup.get_text(separator=' ', strip=True)
            # Clean redisual and embedded HTML tags:
            clean_text = re.sub(r'<[^>]*>', '', text)
            # Strip each line and filter out empty lines in a single operation:
            lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
            # Strip each word and remove extra spaces:
            chunks = [phrase.strip() for line in lines for phrase in line.split(" ")]
            final_text = " ".join(chunk for chunk in chunks if chunk)
            print("Done:", feed_url)
            return final_text
    except Exception as e:
        print(f"Error processing feed {feed_url}: {e}")
        return ""

async def main(feed_file):
    async with aiohttp.ClientSession() as session:
        with open(feed_file, 'r') as file:
            feed_urls = [line.strip() for line in file]
        tasks = [process_feed(feed_url, session) for feed_url in feed_urls]
        cleaned_contents = await asyncio.gather(*tasks)
    print("Done cleaning the contents. Storing in output.parquet...")
    result = {feed_url: content for feed_url, content in zip(feed_urls, cleaned_contents)}
    df = pd.DataFrame(result.items(), columns=["url", "content"])
    df.to_parquet("output.parquet", index=False)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed-path")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.feed_path))

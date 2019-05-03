import feedparser
import asyncio
import time


class feedReader():
    def __init__(self):
        pass

    async def readArticles(self, site):
        try:
            paper = feedparser.parse(site)
            feed = []
            await asyncio.gather(self.printArticles(paper))
        except Exception as e:
            print(e)

    async def printArticles(self, articles):
        with open('/home/pbs/Desktop/feeds', 'w+') as f:
            for article in articles:
                f.write('\n####################################################################\n')
                f.write(str(articles))

async def main():
    tasks = []
    feed = feedReader()
    sites = ['http://feeds.bbci.co.uk/news/rss.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml']
    for site in sites:
        tasks.append(asyncio.ensure_future(feed.readArticles(site)))
    p = await asyncio.gather(*tasks)

s = time.perf_counter()
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except Exception as e:
    print(e)
finally:
    loop.close()
    elapsed = time.perf_counter() - s
    print(f"Executed in {elapsed:0.2f} seconds.")


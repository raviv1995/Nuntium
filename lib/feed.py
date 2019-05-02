import newspaper
import asyncio
import time


class feedReader():
    def __init__(self):
        pass

    async def readArticles(self, site):
        paper = newspaper.build(site, language='en')
        feed = []
        for article in paper.articles:
            try:
                article.download()
                article.parse()
                feed.append(article)
            except Exception as e:
                print(e)
                continue
        return feed

def printArticles(articles):
    with open('/home/pbs/Desktop/feeds', 'w+') as f:
        f.write('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
        for article in articles:
            f.write('\n####################################################################\n')
            f.write(article.title)
            f.write('\n')
            f.write(article.text)

async def main():
    tasks = []
    feed = feedReader()
    sites = ['https://edition.cnn.com/', 'https://www.thehindu.com/', 'https://in.reuters.com/']
    for site in sites:
        tasks.append(asyncio.ensure_future(feed.readArticles(site)))
    p = await asyncio.gather(*tasks)
    i=0
    for c in p:
        print(i)
        i=i+1
        printArticles(c)

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


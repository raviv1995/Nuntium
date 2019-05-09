import feedparser
import asyncio
import re
from datetime import datetime


class feedReader():
    def __init__(self, sites):
        self.sites = sites

    async def _main(self):
        tasks = []
        for site in self.sites:
            tasks.append(asyncio.ensure_future(self.parseArticles(site)))
        feeds = await asyncio.gather(*tasks)
        return feeds

    def main(self):
        loop = asyncio.get_event_loop()
        try:
            feeds = loop.run_until_complete(self._main())
            return feeds
        except Exception as e:
            print(e)
        finally:
            loop.close()

    async def parseArticles(self, site):
        try:
            feeds = []
            paper = feedparser.parse(site)
            articles = paper.get('entries')
            for article in articles:
                articleDict = {'title':article.get('title'), 'summary':self.striphtml(article.get('summary')), 'link':str(article.get('link'))}    
                feeds.append(articleDict)
            return feeds
        except Exception as e:
            print(e)
    
    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)


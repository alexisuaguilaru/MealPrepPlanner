from pathlib import Path
import asyncio

from .ScrapeTopics import MainScrapeListTopics
from .ScrapeListArticles import MainScrapeListArticlesLinks
from .ScrapeArticleContent import MainScrapeArticleContent
from .CleanMetadata import CleanTitle , CleanLastUpdate

from ...Utils import DumpMetadata , SaveMarkdownFile

def MainScraping(NumClicks,MaxArticlesByTopic):
    BasePath = './Datasets/Documents/EatRight'
    base_path = Path(BasePath)
    base_path.mkdir(parents=True,exist_ok=True)

    ListMetadata = []

    LinkPages = [
        'https://www.eatright.org/health/health-conditions',
        'https://www.eatright.org/health/wellness',
    ]

    BaseURL_EatRight = 'https://www.eatright.org'

    for link_page_EatRight in LinkPages:
        list_topics = asyncio.run(MainScrapeListTopics(link_page_EatRight))

        for topic in list_topics:
            list_links_articles = asyncio.run(MainScrapeListArticlesLinks(BaseURL_EatRight+topic['Link'],NumClicks))
            
            for link_article in list_links_articles[:MaxArticlesByTopic]: 
                full_link_article = BaseURL_EatRight+link_article['Link']
                file_name = f'{link_article['Link'].split('/')[-1]}.md'
            
                metadata_page , scraped_content = asyncio.run(MainScrapeArticleContent(full_link_article))

                metadata_article = {
                    'Title': link_article['Title'],
                    'Last Update': CleanLastUpdate(metadata_page),
                    'Source': full_link_article,
                    'File Name': file_name,
                }
                ListMetadata.append(metadata_article)

                SaveMarkdownFile(scraped_content,base_path/metadata_article['File Name'])

    DumpMetadata(ListMetadata,base_path/'metadata.json')
    return ListMetadata
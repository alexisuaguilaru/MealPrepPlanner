import asyncio
import re
import random
from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , BrowserConfig , JsonCssExtractionStrategy
import json

from ...Utils import BasicCrawlerRunConfig , BasicBrowserConfig

async def MainScrapeTechniqueContent(LinkTechnique):
    SessionID = 'Session_Techniques_Larousse'

    ExtractionSchema = {
        'name': 'Technique Content',
        'baseSelector': 'div.single-technica',
        'fields': [
            {'name': 'HTML', 'selector': 'div.container-fluid.bgs-space', 'type': 'html'},
        ]
    }

    Browser = BrowserConfig(
        headless = False,
    )

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        session_id = SessionID,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = LinkTechnique,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(3, 5))
    return CleanMarkdown(result.markdown)

def CleanMarkdown(MarkdownContent):
    PatternMarkdown = r'(### Información adicional.+?)(Lo siento, debes estar \[conectado\])'
    return re.search(PatternMarkdown,MarkdownContent,re.DOTALL).group(1)
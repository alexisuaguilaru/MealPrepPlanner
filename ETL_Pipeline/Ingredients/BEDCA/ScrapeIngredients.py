from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy , BrowserConfig , DefaultTableExtraction
import json

async def MainScrapeIngredients():
    ExtractionSchema = {
        'name': 'Ingredients with Nutritional Facts',
        'baseSelector': 'table#querytable1 tr',
        'fields': [
            {'name': 'SpnName', 'selector': 'td:nth-child(2)', 'type': 'text'},
            {'name': 'EngName', 'selector': 'td:nth-child(3)', 'type': 'text'},
        ]
    }

    CommandInteractions = [
        "document.querySelectorAll('a')[2]?.onclick();",
        "document.querySelectorAll('a#Alfabetica')[0]?.onclick();",
        "document.querySelector('div#alphabet a')?.onclick();",
    ]

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        js_code = CommandInteractions,
        wait_for = 'css:tr.row-b',
        wait_until = 'networkidle',
    )

    async with AsyncWebCrawler() as crawler:
        result: CrawlResult  = await crawler.arun(
            url = 'https://www.bedca.net/bdpub/index.php',
            config = CrawlerConfig,
        )

    return json.loads(result.extracted_content)
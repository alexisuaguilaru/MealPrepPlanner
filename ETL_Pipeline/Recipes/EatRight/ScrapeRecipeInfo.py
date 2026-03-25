import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

FieldWithTimes = [
    {'name': 'Times', 'selector': 'p:nth-of-type(2)', 'type': 'html'},
    {'name': 'Ingredients', 'selector': 'p:nth-of-type(3)', 'type': 'html'},
    {'name': 'Servings', 'selector': 'p:nth-of-type(5)', 'type': 'text'},
    {'name': 'Nutritional Facts', 'selector': 'p:nth-of-type(6)', 'type': 'text'},
    {'name': 'Directions', 'selector': 'ol li', 'type': 'list', 'fields': [{'name': 'direction', 'type': 'text'}]},
]

FieldWithOutTimes = [
    {'name': 'Ingredients', 'selector': 'p:nth-of-type(2)', 'type': 'html'},
    {'name': 'Servings', 'selector': 'p:nth-of-type(4)', 'type': 'text'},
    {'name': 'Nutritional Facts', 'selector': 'p:nth-of-type(5)', 'type': 'text'},
    {'name': 'Directions', 'selector': 'ol li', 'type': 'list', 'fields': [{'name': 'direction', 'type': 'text'}]},
]

async def MainScrapeRecipeInformation(RecipeLink: str):
    ExtractionSchema_TypeExtraction = {
        'name': 'List of Paragraphs',
        'baseSelector': 'section.rtf',
        'fields': [
            {'name': 'Paragraphs', 'selector': 'p', 'type': 'list', 'fields': [
                {'name': 'paragraph', 'type': 'text'}
            ]},
        ]
    }

    ExtractionSchema = {
        'name': 'List of Mealtimes',
        'baseSelector': 'section.rtf',
        'fields': None
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig_EatRight = BasicCrawlerRunConfig.copy()
    del CrawlerConfig_EatRight['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_TypeExtraction),
        **CrawlerConfig_EatRight,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result_TypeExtraction: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

        json_type_extraction = json.loads(result_TypeExtraction.extracted_content)
        if len(json_type_extraction[0]['Paragraphs']) > 5:
            ExtractionSchema['fields'] = FieldWithTimes
        else:
            ExtractionSchema['fields'] = FieldWithOutTimes

        CrawlerConfig.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema)
        result: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    return json.loads(result.extracted_content)
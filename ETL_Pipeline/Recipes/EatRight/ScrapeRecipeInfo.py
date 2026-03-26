import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonXPathExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipeInformation(RecipeLink: str):
    ExtractionSchema = {
        'name': 'List of Mealtimes',
        'baseSelector': "//section[contains(@class,'rtf')]",
        'fields': [
            {'name': 'Times', 'selector': ".//p[contains(text(),'minute') or contains(text(), 'hour')]", 'type': 'text', 'default': '0 minutes'},
            {'name': 'Ingredientes', 'selector': ".//h3[contains(text(),'Ingredient')]/following-sibling::p[1]", 'type': 'html'},
            {'name': 'Servings Nutritional Facts 1', 'selector': ".//h3[contains(text(), 'Nutrition')]/following-sibling::p[1]", 'type': 'html', 'default': ''},
            {'name': 'Servings Nutritional Facts 2', 'selector': ".//h3[contains(text(), 'Nutrition')]/following-sibling::p[2]", 'type': 'html', 'default': ''},
            {'name': 'Directions 1', 'selector': "//ol/li", 'type': 'list', 'fields': [{'name': 'direction', 'type': 'text'}], 'default': []},
            {'name': 'Directions 2', 'selector': ".//h3[contains(text(), 'Direction')]/following-sibling::p[1]", 'type': 'text', 'default': ''},
        ],
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig_EatRight = BasicCrawlerRunConfig.copy()
    del CrawlerConfig_EatRight['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonXPathExtractionStrategy(ExtractionSchema),
        **CrawlerConfig_EatRight,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    formatted_content = json.loads(result.extracted_content)[0]

    formatted_content['Servings Nutritional Facts'] = formatted_content['Servings Nutritional Facts 1']+formatted_content['Servings Nutritional Facts 2']
    del formatted_content['Servings Nutritional Facts 1']
    del formatted_content['Servings Nutritional Facts 2']

    if formatted_content['Directions 1']:
        formatted_content['Directions'] = formatted_content['Directions 1']
    else:
        formatted_content['Directions'] = [{'direction': formatted_content['Directions 2']}]

    return formatted_content
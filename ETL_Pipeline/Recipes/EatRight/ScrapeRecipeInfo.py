import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonXPathExtractionStrategy , CacheMode

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipeInformation(RecipeLink: str):
    SessionID = 'Scrape_Mealtimes_EatRight'

    ExtractionSchema = {
        'name': 'List of Mealtimes',
        'baseSelector': "//section[contains(@class,'rtf')]",
        'fields': [
            {'name': 'Times', 'selector': ".//p[contains(text(),'minute') or contains(text(), 'hour')]", 'type': 'text', 'default': '0 minutes'},
            {'name': 'Ingredients 1', 'selector': ".//h3[contains(text(),'Ingredient')]/following-sibling::p[1]", 'type': 'html', 'default': ''},
            {'name': 'Ingredients 2', 'selector': ".//h3[contains(text(),'Ingredients')]/following-sibling::p[1]", 'type': 'html', 'default': ''},
            {'name': 'Servings Nutritional Facts 1', 'selector': ".//h3[contains(text(), 'Nutrition')]/following-sibling::p[1]", 'type': 'html', 'default': ''},
            {'name': 'Servings Nutritional Facts 2', 'selector': ".//h3[contains(text(), 'Nutrition')]/following-sibling::p[2]", 'type': 'html', 'default': ''},
            {'name': 'Directions 1', 'selector': "//ol/li", 'type': 'list', 'fields': [{'name': 'direction', 'type': 'text'}], 'default': []},
            {'name': 'Directions 2', 'selector': ".//h3[contains(text(), 'Direction')]/following-sibling::p[1]", 'type': 'text', 'default': ''},
        ],
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonXPathExtractionStrategy(ExtractionSchema),
        session_id = SessionID,
        delay_before_return_html = random.uniform(3,5),
        scroll_delay = random.uniform(0.5,1),
        cache_mode = CacheMode.ENABLED,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))
    try:
        formatted_content = json.loads(result.extracted_content)[0]
    except:
        return {}

    formatted_content['Servings Nutritional Facts'] = formatted_content['Servings Nutritional Facts 1']+formatted_content['Servings Nutritional Facts 2']
    del formatted_content['Servings Nutritional Facts 1']
    del formatted_content['Servings Nutritional Facts 2']

    if formatted_content['Directions 1']:
        formatted_content['Directions'] = formatted_content['Directions 1']
    else:
        formatted_content['Directions'] = [{'direction': formatted_content['Directions 2']}]
    del formatted_content['Directions 1']
    del formatted_content['Directions 2']

    formatted_content['Ingredients'] = (formatted_content['Ingredients 1'] or formatted_content['Ingredients 2'])
    del formatted_content['Ingredients 1']
    del formatted_content['Ingredients 2']

    return formatted_content
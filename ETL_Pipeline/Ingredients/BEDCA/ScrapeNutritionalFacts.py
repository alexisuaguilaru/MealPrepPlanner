from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy , BrowserConfig , DefaultTableExtraction
import json

async def MainScrapeIngredientNutritionalFacts(IngredientID: str):
    SessionID = 'Session_IngredientInformation_BEDCA'

    ExtractionSchema = {
        'name': 'Nutritional Facts of a Ingredient',
        'baseSelector': 'table tbody',
        'fields': [
            {'name': 'Nutrient', 'selector': 'td', 'type': 'text'},
            {'name': 'Value', 'selector': 'td:nth-child(2)', 'type': 'text'},
            {'name': 'Measure', 'selector': 'td:nth-child(3)', 'type': 'text'},
        ]
    }

    Command = [
        f"""
        query(2,new Array('f_id','f_ori_name','f_eng_name','sci_name','langual','foodexcode','mainlevelcode','codlevel1',
        'namelevel1','codsublevel','codlevel2','namelevel2','f_des_esp','f_des_ing','photo','edible_portion','f_origen',
        'c_id','c_ori_name','c_eng_name','eur_name','componentgroup_id','glos_esp','glos_ing','cg_descripcion','cg_description',
        'best_location','v_unit','moex','stdv','min','max','v_n','u_id','u_descripcion','u_description','value_type','vt_descripcion',
        'vt_description','mu_id','mu_descripcion','mu_description','ref_id','citation','at_descripcion','at_description','pt_descripcion',
        'pt_description','method_id','mt_descripcion','mt_description','m_descripcion','m_description','m_nom_esp','m_nom_ing',
        'mhd_descripcion','mhd_description'),new Array('f_id','publico'),new Array('EQUAL','EQUAL'),new Array(),new Array('{IngredientID}',1),'componentgroup_id','ASC')
        """
    ]

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        session_id = SessionID,
        js_code = Command,
        wait_for = 'css:tr.row-a',
        wait_until = 'networkidle',
    )

    async with AsyncWebCrawler() as crawler:
        result: CrawlResult  = await crawler.arun(
            url = 'https://www.bedca.net/bdpub/index.php',
            config = CrawlerConfig,
        )
    
    return json.loads(result.extracted_content)
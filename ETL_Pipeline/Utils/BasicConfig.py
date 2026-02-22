import random

HEADLESS = False
BasicBrowserConfig = dict(
    headless = HEADLESS,
    user_agent_mode = 'random',
    enable_stealth = True,
    extra_args = ["--disable-blink-features=AutomationControlled"],
    use_persistent_context = True,
    user_data_dir = './.crawl_data',
)
BasicBrowserConfig_NoPersistentContext = dict(
    headless = HEADLESS,
    user_agent_mode = 'random',
    enable_stealth = True,
    extra_args = ["--disable-blink-features=AutomationControlled"],
)

BasicCrawlerRunConfig = dict(
    delay_before_return_html = random.uniform(3,5),
    scroll_delay = random.uniform(0.5,1),
    simulate_user = True,
    magic = True,
    wait_until = 'networkidle',
)
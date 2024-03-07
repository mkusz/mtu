def test_temp(playwright_page, env_config):
    playwright_page.goto(env_config.url_ui)

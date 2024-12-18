from playwright.sync_api import sync_playwright

def screenshot_twitch():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.twitch.tv")
        page.wait_for_load_state("networkidle")

        page.screenshot(path="twitch_homepage.png", full_page=True)
        browser.close()

if __name__ == "__main__":
    screenshot_twitch()
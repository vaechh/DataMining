import time
from playwright.sync_api import sync_playwright

def parse_twitch_streams():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        try:
            page.goto("https://www.twitch.tv")

            # Ожидаем и вводим в поисковое поле "Minecraft"
            search_box = page.locator('input[autocomplete="twitch-nav-search"]')
            search_box.type("Minecraft", delay=100)

            # Ждем появления результата поиска
            page.wait_for_selector('div.Layout-sc-1xcs6mc-0.auOiD', timeout=20000)

            # Кликаем на результат с тегами
            page.locator('div#search-result-row__0').click()

            # Ожидаем загрузки блока трансляций
            page.wait_for_selector("div.Layout-sc-1xcs6mc-0.dUClxi", timeout=30000)

            stream_cards_container = None
            stream_cards = None
            stream_count = None

            while True:
                stream_cards_container = page.locator("div.ScTower-sc-1sjzzes-0.fwymPs.tw-tower")
                stream_cards = stream_cards_container.locator("div.Layout-sc-1xcs6mc-0.dUClxi")
                stream_count = stream_cards.count()
                
                stream_cards.element_handles()[-1].scroll_into_view_if_needed()
                time.sleep(4)

                new_stream_cards_container = page.locator("div.ScTower-sc-1sjzzes-0.fwymPs.tw-tower")
                new_stream_cards = stream_cards_container.locator("div.Layout-sc-1xcs6mc-0.dUClxi")
                new_stream_count = stream_cards.count()

                print(stream_count)
                print(new_stream_count)
                if new_stream_count > stream_count:
                    continue
                else:
                    break

            print(f"Найдено {stream_count} трансляций.")
            print("Доступные трансляции:")
            for idx in range(stream_count):
                try:
                    card = stream_cards.nth(idx)

                    # Заголовок трансляции
                    title = card.locator("h3.CoreText-sc-1txzju1-0.MveHm").text_content(timeout=5000) or "Неизвестно"

                    # Имя стримера
                    streamer = card.locator("p[data-a-target='preview-card-channel-link']").text_content(timeout=5000) or "Неизвестно"

                    # Количество зрителей
                    viewers = card.locator(".ScMediaCardStatWrapper-sc-anph5i-0").text_content(timeout=5000) or "Неизвестно"

                    # Тэги
                    tag_placers = card.locator(".InjectLayout-sc-1i43xsx-0.gNgtQs")
                    tags = tag_placers.locator(".InjectLayout-sc-1i43xsx-0").all_text_contents()
                    tags_text = ", ".join(tags) if tags else "Неизвестно"

                    print(f"{idx + 1}. Заголовок: {title}\n   Стример: {streamer}\n   Зрителей: {viewers}\n   Тэги: {tags_text}")
                except Exception as inner_e:
                    print(f"Не удалось получить данные для трансляции {idx + 1}: {inner_e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            # Закрываем браузер
            browser.close()

# Запускаем функцию
if __name__ == "__main__":
    parse_twitch_streams()

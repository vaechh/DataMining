from playwright.sync_api import sync_playwright

def parse_twitch_streams():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        try:
            page.goto("https://www.twitch.tv")

            page.wait_for_selector("div.ScTower-sc-1sjzzes-0.fwymPs.tw-tower", timeout=60000)

            stream_cards_container = page.locator("div.ScTower-sc-1sjzzes-0.fwymPs.tw-tower")
            stream_cards = stream_cards_container.locator("div.OBUFH.ScTransitionBase-sc-hx4quq-0.tw-transition")
            stream_count = stream_cards.count()

            print("Доступные трансляции:")
            for idx in range(stream_count):
                try:
                    card = stream_cards.nth(idx)

                    # Заголовок трансляции
                    title = card.locator("button[data-test-selector='StreamTitle'] h3").text_content(timeout=5000) or "Неизвестно"

                    # Имя стримера
                    streamer = card.locator("p[data-a-target='preview-card-channel-link']").text_content(timeout=5000) or "Неизвестно"

                    # Количество зрителей
                    viewers = card.locator(".ScMediaCardStatWrapper-sc-anph5i-0").text_content(timeout=5000) or "Неизвестно"

                    # Тэги
                    tag_placers = card.locator(".InjectLayout-sc-1i43xsx-0.gNgtQs")
                    tag_elements = tag_placers.locator(".InjectLayout-sc-1i43xsx-0")  # Находим все подходящие элементы
                    tags = [tag.text_content(timeout=5000) for tag in tag_elements.all()]  # Собираем текст всех элементов
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

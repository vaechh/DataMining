from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def parse_twitch_streams():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        try:
            page.goto("https://www.twitch.tv")

            # Ожидание загрузки контейнера с трансляциями
            page.wait_for_selector("div.ScTower-sc-1sjzzes-0.fwymPs.tw-tower", timeout=60000)

            # Получаем HTML контент страницы
            html_content = page.content()

            # Передаем HTML в BeautifulSoup для парсинга
            soup = BeautifulSoup(html_content, "html.parser")

            # Находим контейнер с карточками трансляций
            stream_cards_container = soup.find_all("div", class_="ScTower-sc-1sjzzes-0 fwymPs tw-tower")

            idx = 0
            print("Доступные трансляции:")
            for container in stream_cards_container:
                # Для каждого контейнера ищем карточки трансляций
                stream_cards = container.find_all("div", class_="OBUFH ScTransitionBase-sc-hx4quq-0 tw-transition")

                for card in stream_cards:
                    try:
                        # Заголовок трансляции
                        title = card.find("button", {"data-test-selector": "StreamTitle"})
                        title = title.find("h3").get_text() if title else "Неизвестно"

                        # Имя стримера
                        streamer = card.find("p", {"data-a-target": "preview-card-channel-link"})
                        streamer = streamer.get_text() if streamer else "Неизвестно"

                        # Количество зрителей
                        viewers = card.find("div", class_="ScMediaCardStatWrapper-sc-anph5i-0")
                        viewers = viewers.get_text() if viewers else "Неизвестно"

                        # Тэги
                        tag_elements = card.find_all("div", class_="InjectLayout-sc-1i43xsx-0")
                        tags = [tag.get_text() for tag in tag_elements]
                        tags_text = ", ".join(tags) if tags else "Неизвестно"

                        idx = idx + 1
                        print(f"{idx}. Заголовок: {title}\n   Стример: {streamer}\n   Зрителей: {viewers}\n   Тэги: {tags_text}")
                    except Exception as inner_e:
                        print(f"Не удалось получить данные для трансляции {idx}: {inner_e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            # Закрываем браузер
            browser.close()

# Запускаем функцию
if __name__ == "__main__":
    parse_twitch_streams()

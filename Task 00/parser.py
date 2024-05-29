import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import logging

logging.basicConfig(level = logging.INFO, filename = "news_articles_log.log", filemode = "w", format = "%(asctime)s %(levelname)s %(message)s")

# указывает начальный адрес для поиска статей
url = "https://www.nytimes.com/section/politics"
# указываем ключевые слова для поиска в статьях
keywords = ["Trump", "Biden"]
# время на выполнение скрипта
time_for_parsing = 4 * 60 * 60

# функция для сбора новостей
def collect_news():
    # делаем запрос в начальному адресу извлекая его текстовые данные
    response = requests.get(url).text
    # обрабатываем полученный текст
    data = BeautifulSoup(response, "html.parser")
    # список для статей с ключевыми словами
    news = []
    articles = data.find_all("article")

    # цикл для поиска по найденным статьям
    for article in articles:
        # заголовок статьи
        title = article.find("h3", class_ = "css-1j88qqx e15t083i0")
        # краткое описание
        description = article.find("p", class_ = "css-1pga48a e15t083i1")
        # автор статьи
        author = article.find("span", class_ = "css-1n7hynb")

        # если Заголовок и Краткое описание - не пустые, то-есть True
        if title and description:
            # "извлекаем" строки из html-разметки
            # параметр strip = True для удаления пробелов в начале и конце извлекаемых строк
            title_text = title.get_text(strip = True)
            description_text = description.get_text(strip = True)
            author_text = author.get_text(strip = True)

            # ищем ключевые слова в заголовке статьи, преобразуем в кортеж и добавляем в список news
            for keyword in keywords:
                if keyword in title_text:
                    news.append((title_text, description_text, author_text))

    return news


# Главная функция для выполнения скрипта
def main():
    # время запуска скрипта
    start_time = datetime.now()
    # расчет длительности времени работы скрипта
    end_time = start_time + timedelta(seconds = time_for_parsing)
    # список уже найденных статей - чтобы не повторялись
    seen_articles = []

    # цикл для записи статей в лог и добавления их в список уже найденных
    while start_time < end_time:
        logging.info(f"\n\tНовые статьи на сайте New york Times с ключевыми словами: {keywords[0]} и {keywords[1]}\n")
        news = collect_news()

        for title, description, author in news:
            if title not in seen_articles:
                logging.info(f"Заголовок статьи: {title}")
                logging.info(f"Краткое описание: {description}")
                logging.info(f"Автор: {author}\n")
                seen_articles.append(title)

        # задержка в 10 минут для проверки сайта на новые статьи
        time.sleep(600)

if __name__ == "__main__":
    main()

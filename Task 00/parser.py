import requests
from bs4 import BeautifulSoup

# указывает начальный адрес для поиска статей
url = "https://www.nytimes.com/section/politics"

# указываем ключевые слова для поиска в статьях
keywords = ["Trump", "Biden"]

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

            for keyword in keywords:
                if keyword in title_text:
                    news.append((title_text, description_text, author_text))

    print(news)


collect_news()

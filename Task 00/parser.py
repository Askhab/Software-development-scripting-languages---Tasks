import requests
from bs4 import BeautifulSoup

# указывает начальный адрес для поиска статей
url = "https://www.nytimes.com/section/politics"
response = requests.get(url).text

data = BeautifulSoup(response, "html.parser")

for article in data.find_all("div", class_ = "css-dde3aw"):
    title = article.p.a.text
    link = "https://www.nytimes.com" + article.a["href"]
    print(title, link)

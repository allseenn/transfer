import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

start_time = time.time()
ua = UserAgent()
url = 'https://irecommend.ru'
path = '/content/sait-geekbrains'
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

session = requests.session()


all_books = []
for i in range(10):
    page = f'?page={i}'
    response = session.get(url+path+page, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a', {'class': 'reviewTextSnippet'})
    for link in links:
        yell_link = url+link.get('href')
        yell_page = session.get(yell_link, headers=headers)
        yell_soup = BeautifulSoup(yell_page.text, "html.parser")
        yell_div = yell_soup.find('div', {'itemprop': 'reviewBody'})
        yell_text = yell_div.getText().replace("\n", "").strip()
    all_books.append(yell_text)
    print("\033c")
    print(f"Обрабатываем страницу № {i}, прошло {time.time() - start_time:.2f} секунд")
filename = 'books.json'
with open(filename, 'w') as file:
    json.dump(all_books, file)

end_time = time.time()
print(f"Обработано за {end_time - start_time:.2f} секунд {len(all_books)} книг, сохранено в {filename}")

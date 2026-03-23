from bs4 import BeautifulSoup
import requests

url = ('https://raw.githubusercontent.com/', "joelgrus/data/master/getting-data.html")
html = requests.get(''.join(url)).text
soup = BeautifulSoup(html, 'html.parser')

import_paragraphs = soup('p', {'class': 'important'})

spans_inside_divs = [span 
    for div in soup('div')
    for span in div('span')]

print(spans_inside_divs)

# url = "https://moodle.unicentro.br/"
# html = requests.get(url).text
# tft = BeautifulSoup(html, 'html.parser')
# print (tft)
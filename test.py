
from bs4 import BeautifulSoup

page_html = "<div id=\"pagination\"><a href=\"#/\" x-page=\"1\"><span class=\"arrow\">|«</span></a><a href=\"#/\" x-page=\"1\"><span class=\"arrow\">«</span></a><span class=\"active-page\">1</span><a href=\"#/page/2/\" x-page=\"2\"><span>2</span></a><a href=\"#/page/3/\" x-page=\"3\"><span>3</span></a><a href=\"#/page/2/\" x-page=\"2\"><span class=\"arrow\">»</span></a><a href=\"#/page/3/\" x-page=\"3\"><span class=\"arrow\">»|</span></a></div>"
pagination = BeautifulSoup(page_html, "html.parser")

#rows = pagination.find_all('span')[2:-2]
rows = pagination.find_all('a')[2:-2]
for row in rows:
    print (row['href'])

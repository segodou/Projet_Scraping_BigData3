import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import datetime
from dateutil.relativedelta import relativedelta


with open('scrapingData.csv', 'w', encoding="utf-8") as output:
    output.write('name,date_of_published,author,number_of_comments,points\n')
    for i in range(1,6):
        url = 'https://news.ycombinator.com/news?p=' + str(i)

        response = requests.get(url)            # Je récupère mon contenu dans un objet

        if response.ok:                         # Je vérifie si tout a bien fonctionné       
            print("Page : " + str(i))
            soup = BeautifulSoup(response.text, 'html5lib')              # récupéré le code html avec beautifulsoup pour le passer
            
            table = soup.find('table', attrs={'class': 'itemlist'})         # sélectione de la table contenant les infos
                
            results_title = table.find_all('tr' , attrs={'class': 'athing'})       # sélectionne de la tr contenant les liens de chaque publication
            results_infos = table.find_all('td', attrs={'class': 'subtext'})
            for i in range(30):
                title = (results_title[i].find('a', attrs={'class': 'titlelink'})).text
                
                try:
                    points = (results_infos[i].find('span', attrs={'class': 'score'})).text.split(" ")[0]
                    author = (results_infos[i].find('a', attrs={'class': 'hnuser'})).text
                    items = results_infos[i].find_all('a')[1:4:2]
                    date_published = items[0].text
                    val, unit = date_published.split()[:2]
                    date_published = (datetime.datetime.now() - relativedelta(**{unit:int(val)})).strftime("%Y-%m-%d")
                    numbers_of_comments = items[1].text.replace(u'\xa0', ' ').encode('utf-8').decode()
                    numbers_of_comments = numbers_of_comments.split(" ")[0]
                except:
                    points = " "
                    author = " "
                    numbers_of_comments = " "
                    #continue
                
                if author == " ":
                    author = "none"
                if points == " ":
                    points = '0'
                if numbers_of_comments == 'discuss' or numbers_of_comments == " ":
                    numbers_of_comments = '0'
                print("{} published by {}, {} with {} comment(s) and {} point(s)".format(title,author,date_published,numbers_of_comments,points))
                output.write(title +','+ date_published +','+ author+','+ numbers_of_comments +','+ points +'\n')

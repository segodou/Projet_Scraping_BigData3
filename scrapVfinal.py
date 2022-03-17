import requests
from bs4 import BeautifulSoup
import datetime
import time
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass

# Création de la dataclasse
@dataclass
class Post:
    title : str
    date_published: str
    author : str
    commments : str
    points : str
    
    def get_all(self):
        return (f"{self.title},{self.date_published},{self.author},{self.commments},{self.points}\n")

# La boucle pour faire tourné le programme tous les 1h
while True:
    #création du fichier csv 
    with open('scrapingData.csv', 'w', encoding="utf-8") as output:
        #header du fichier
        output.write('name,date_of_published,author,number_of_comments,points\n')
        for i in range(1,6):
            url = 'https://news.ycombinator.com/news?p=' + str(i)
            # Je récupère mon contenu dans un objet
            response = requests.get(url)           
            # Je vérifie si tout a bien fonctionné 
            if response.ok:                               
                print("Page : " + str(i))
                # récupéré le code html avec beautifulsoup pour le passer
                soup = BeautifulSoup(response.text, 'html5lib') 
                             
                # sélectione de la table contenant les infos
                table = soup.find('table', attrs={'class': 'itemlist'})         
                 # sélectionne de la tr et td contenant le title et les infos qu'on recherche    
                results_title = table.find_all('tr' , attrs={'class': 'athing'})      
                results_infos = table.find_all('td', attrs={'class': 'subtext'})
                
                # On parcourt les 30 publication de chaque page
                for i in range(30):
                    title = (results_title[i].find('a', attrs={'class': 'titlelink'})).text
                    # Evitez que le programme s'arrete si les balises recherchés n'existe pas
                    try:
                        points = (results_infos[i].find('span', attrs={'class': 'score'})).text.split(" ")[0]
                        author = (results_infos[i].find('a', attrs={'class': 'hnuser'})).text
                        items = results_infos[i].find_all('a')[1:4:2]
                        date_published = items[0].text
                        val, unit = date_published.split()[:2]
                        date_published = (datetime.datetime.now() - relativedelta(**{unit:int(val)})).strftime("%Y-%m-%d %H-%M")
                        numbers_of_comments = items[1].text.replace(u'\xa0', ' ').encode('utf-8').decode()
                        numbers_of_comments = numbers_of_comments.split(" ")[0]
                    except:
                        points = " "
                        author = " "
                        numbers_of_comments = " "
                        #continue
                    # vérifiez si les variales sont nuls
                    if author == " ":
                        author = "none"
                    if points == " ":
                        points = '0'
                    if numbers_of_comments == 'discuss' or numbers_of_comments == " ":
                        numbers_of_comments = '0'
                    # On crée un objet post avec ces attributs
                    post = Post(title,date_published,author,numbers_of_comments,points)
                    # On écrit la ligne correspond à notre objet dans le fichier csv 
                    output.write(post.get_all())
        print("Le programme va se réexécuter dans une heure")
    # Temps d'attente du programme
    time.sleep(3600)
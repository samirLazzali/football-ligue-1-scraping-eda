from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd


# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=option)
# Go to desired website


def getWebDriver(urlToGet):
        
    #browser.get("https://www.oddsportal.com/soccer/france/ligue-1/results")
    #browser.get("https://www.oddsportal.com/soccer/france/ligue-1-2003-2004/results/")
    browser.get(urlToGet)
    #no data available url 
    #browser.get("https://www.oddsportal.com/soccer/france/ligue-1-2002-2003/results/")


    # Wait 20 seconds for page to load
    timeout = 20
    try:
        # Here we want to reach tournamentTable div
        # Go from 'display : none' to 'display : block' when information are loaded
        
        #Dev : 
        WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH,"//div[@id='tournamentTable'][contains(@style, 'display: block')]")))
        
    except TimeoutException:    
        print("Timed out waiting for page to load")
        browser.quit()
        
    # let's first find out if there is data for this specific year or not
    try:
        if(browser.find_element_by_id('emptyMsg')):
            print ('No data available')
            exit()
    except Exception:
        print ('Data available')
    return browser
    



# prend season en param ? 
def parseTable(tournament_tbl_soup):
    # get all tr
    # except first one isn't usefull 'soccer ligue 1 2003/2004' :
    rows = tournament_tbl_soup.find_all('tr')[1:]
    date = None
    data = []
    for row in rows:
        row_data = []
        cols=row.find_all('td')
        if(not cols):
            # TODO Create a fuction to transalte litteral day to interger
            # then create Date and extract day
            date = row.find('span').text
            #print(date)
        elif (cols[0].text) :
            #print("Date     : "+date)

            # create date ? 
            hours =  cols[0].text
            teams = cols[1].text.split(" - ")
            team_a =  teams[0]
            team_b = teams[1]
            score = cols[2].text.split(":")
            #print(score)
            score_a =  int(score[0])
            'score : "1:2 pen.", "1:2", "1:2 ET	"'
            if(len(score[1].split("\xa0")) == 2):
                score_b = int(score[1].split("\xa0")[0])
                print(teams)
                print(score[1].split("\xa0")[1])
            else : 
                score_b = int(score[1])
            odds_a = cols[3].find('a').text
            odds_draw = cols[4].find('a').text
            odds_b = cols[5].find('a').text
            outcome = 'HOME'
            
            if(score_b > score_a):
                outcome = 'AWAY'
            elif(score_b == score_a) :
                outcome = 'DRAW'
            row_data = [date, hours, team_a, team_b, score_a, score_b, odds_a, odds_b, odds_draw, outcome, 'season ?', 'date/day ?']
            data.append(row_data)
    return data #return un df qui contient direcement la season a append au df global ? 


def getPagesUrl(tournament_tbl_soup):
    pagination = tournament_tbl_soup.find(id="pagination")
    pages = [ x['href'] for x in pagination.find_all('a')[2:-2] ]
    return pages # append host ? 

def getSeasonsUrl (seasons):
    # the first one is not about season
    # last 5 season does not have data 
    # ('no data' can be managed, trim them just help to make less request)
    rows = [ "https://www.oddsportal.com" + x['href'] for x in seasons.find_all('a')[1:-5] ]
    rows = ['https://www.oddsportal.com/soccer/france/ligue-1-2018-2019/results/', 'https://www.oddsportal.com/soccer/france/ligue-1-2017-2018/results/']
    return rows #also return name of season to append au df ? {'2003-2004' : 'https://...'}

def main():
    print("""
    1) INIT - Acceder à l'url d'oringine 2003/2004
        a) Créer la fonction getSeason to retreive all season url (trim before 2003 ?)
           Et retourner un tableau des saisons et retourner toutes les urls à scraper 
        b) Scraper le nombre de page de la saison en cours
        c) Récup les pages sous forme de tableau 
            Recrer url pour la saison pour chaque page 
            Recup les données et append au chunk de la saison init
            Ajouté la saison au chunk et append au master
        d) repeter pour chaque saison 
        eecrire le master en csv/numpy 

    """)
           
    #browser.get("https://www.oddsportal.com/soccer/france/ligue-1/results")
    #urlToGet = "https://www.oddsportal.com/soccer/france/ligue-1-2003-2004/results/"
    #no data available url 
    #browser.get("https://www.oddsportal.com/soccer/france/ligue-1-2002-2003/results/")

    # local : 
    #urlToGet = "file:///home/sam/Documents/cours/python/football-ligue-1-scraping-eda-master/2003-2004.html"
    urlToGet ="https://www.oddsportal.com/soccer/france/ligue-1/results/"
    browser = getWebDriver(urlToGet)
    # Selenium is usefull to get the page with dynamic behaviour, BeautifulSoup is better to parse html
    seasons_html = browser.find_element_by_class_name('main-menu2.main-menu-gray').get_attribute("innerHTML")
    seasons_soup = BeautifulSoup(seasons_html, "html.parser")
    seasons_url = getSeasonsUrl(seasons_soup)
    print(seasons_url)
    columns = ['date', 'hours', 'team_a', 'team_b', 'score_a', 'score_b', 'odds_a', 'odds_b', 'odds_draw', 'outcome', 'season ?', 'date/day ?']
    df = pd.DataFrame([], columns = columns) 

    for season_url in seasons_url:
        #print(season_url)
        browser = getWebDriver(season_url)
        tournament_tbl_html = browser.find_element_by_id('tournamentTable').get_attribute("innerHTML")
        tournament_tbl_soup = BeautifulSoup(tournament_tbl_html, "html.parser")
        pages_url = getPagesUrl(tournament_tbl_soup)
        df.append(pd.DataFrame(parseTable(tournament_tbl_soup), columns = columns))
        #print (pd.DataFrame(parseTable(tournament_tbl_soup), columns = columns))
        print(df)
        exit()
        for page in pages_url:
            #print(season_url + page)
            browser = getWebDriver(season_url + page)
            tournament_tbl_html = browser.find_element_by_id('tournamentTable').get_attribute("innerHTML")
            tournament_tbl_soup = BeautifulSoup(tournament_tbl_html, "html.parser")
            df.append(pd.DataFrame(parseTable(tournament_tbl_soup), columns = columns)) 

    print(df)
    exit()

if __name__ == "__main__":
    main()
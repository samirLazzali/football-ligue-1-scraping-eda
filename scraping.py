from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime
import time

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

    """ 
    # let's first find out if there is data for this specific year or not
    try:
        if(browser.find_element_by_id('emptyMsg')):
            print ('No data available')
            exit()
    except Exception:
        #print ('Data available')
    """
    return browser
    
def month_to_num(str_month):
    return {
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9, 
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
    }[str_month]


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
            splited_date = row.find('span').text.split(" ")
            if(splited_date[0] == 'Today,' or splited_date[0] == 'Yesterday,'):
                print('today')
                # date du jour a clater dans splited date 
                today = datetime.datetime.now()
                #['27', 'Feb', '2010']
                splited_date = [splited_date[1], splited_date[2],today.strftime('%Y'),]
        elif (cols[0].text) :
            if(cols[2].text == "award."):
                print('Skip this one, awarded between :',team_a,'and',team_b)
                continue
            
            if(not cols[3].find('a') or not cols[4].find('a') or not cols[5].find('a')):
                print('Skip this one, strange odds ')
                continue

            hours_str =  cols[0].text
            hours = cols[0].text.split(":")
            date = datetime.datetime(int(splited_date[2]),month_to_num(splited_date[1]),int(splited_date[0]), int(hours[0]),int(hours[1]))
            teams = cols[1].text.split(" - ")
            team_a =  teams[0]
            team_b = teams[1]
            score = cols[2].text.split(":")
            score_a =  int(score[0])
            # some score are : 1:2ET or 1:2pen.
            # Une idée pourrait etre d'aller recueprer l'url des match 
            # et aller recuperer le score au mi-temps + la consitution de l'equipe (et le nom de l'arbitre)
            if(len(score[1].split("\xa0")) == 2):
                score_b = int(score[1].split("\xa0")[0])
                print(teams)
                print(date)
                print(score[1].split("\xa0")[1])
                # TODO je recupere aussi les ET et pen. ? 
            else : 
                score_b = int(score[1])
          
            odds_a = cols[3].find('a').text
            odds_draw = cols[4].find('a').text
            odds_b = cols[5].find('a').text
            row_data = [date, hours_str, team_a, team_b, score_a, score_b, odds_a, odds_b, odds_draw, date.strftime("%A")]
            data.append(row_data)
    return data 


def getPagesUrl(tournament_tbl_soup):
    pagination = tournament_tbl_soup.find(id="pagination")
    pages = [ x['href'] for x in pagination.find_all('a')[2:-2] ]
    return pages # append host ? 

def getSeasonsUrl (seasons):
    # the first one is not about season
    # last 5 season does not have data 
    # ('no data' can be managed, trim them just help to make less request)
    data_season = {}
    for x in seasons.find_all('a')[:-5]:
        data_season[x.text] = "https://www.oddsportal.com" + x['href']
    
    #print (data_season)
    
    """
    data_season = {
        '2004/2005': 'https://www.oddsportal.com/soccer/france/ligue-1-2009-2010/results/#/page/3/',
        }
    """
    
    return data_season #also return name of season to append au df ? {'2003-2004' : 'https://...'}


def main():
    start = datetime.datetime.now()
    """
        Idées :
        - Calculer le nombre de but marqué pour une équipe depuis le debut de la competition au moment du match 
        - Comper les victoires/defaite de l'équipe a/b au moment du match
    """
    # local : 
    #urlToGet = "file:///home/sam/Documents/cours/python/football-ligue-1-scraping-eda-master/2003-2004.html"
    
    urlToGet ="https://www.oddsportal.com/soccer/france/ligue-1/results/"
    print('parsing init : ',urlToGet)
    browser = getWebDriver(urlToGet)
    # Selenium is usefull to get the page with dynamic behaviour, BeautifulSoup is better to parse html
    seasons_html = browser.find_element_by_class_name('main-menu2.main-menu-gray').get_attribute("innerHTML")
    seasons_soup = BeautifulSoup(seasons_html, "html.parser")
    seasons_url = getSeasonsUrl(seasons_soup)
    columns = ['date', 'hours', 'team_a', 'team_b', 'score_a', 'score_b', 'odds_a', 'odds_b','odds_draw', 'day']
    df = pd.DataFrame([], columns = columns) 
    for (season_name,season_url) in seasons_url.items():
        print('parse : ',season_url)
        browser = getWebDriver(season_url)
        tournament_tbl_html = browser.find_element_by_id('tournamentTable').get_attribute("innerHTML")
        tournament_tbl_soup = BeautifulSoup(tournament_tbl_html, "html.parser")
        pages_url = getPagesUrl(tournament_tbl_soup)
        df_parse_table = pd.DataFrame(parseTable(tournament_tbl_soup), columns = columns)
        df_parse_table['season'] = season_name
        print(season_name, 'page : 1 => ',df_parse_table.shape[0],'games')
        df = df.append(df_parse_table,sort=True)
        #break
        for page in pages_url:
            print('parse : ',season_url + page)
            browser = getWebDriver(season_url + page)
            tournament_tbl_html = browser.find_element_by_id('tournamentTable').get_attribute("innerHTML")
            tournament_tbl_soup = BeautifulSoup(tournament_tbl_html, "html.parser")
            df_parse_table = pd.DataFrame(parseTable(tournament_tbl_soup), columns = columns)
            df_parse_table['season'] = season_name
            print(season_name, 'page :',page[-2:-1],' => ',df_parse_table.shape[0],'games')
            df = df.append(df_parse_table,sort=True)
            print('total :', df.shape[0])
        #break


    print(df)
    package_dir = os.path.dirname(os.path.abspath(__file__))
    #file_name  = datetime.datetime(2018, 6, 1).strftime("%B")
    file_name = "exctract"
    thefile = os.path.join(package_dir, file_name+'.csv')
    print(thefile)
    df.to_csv (thefile, index = None, header=True) #Don't forget to add '.csv' at the end of the path
    diff = (datetime.datetime.now() - start).total_seconds()
    print ("Scraping done in : ", diff,'s')
    print('exit')
    exit()

if __name__ == "__main__":
    main()
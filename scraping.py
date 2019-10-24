from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=option)

# Go to desired website
#browser.get("https://www.oddsportal.com/soccer/france/ligue-1/results")
browser.get("https://www.oddsportal.com/soccer/france/ligue-1-2003-2004/results/")

#no data available url 
#browser.get("https://www.oddsportal.com/soccer/france/ligue-1-2002-2003/results/")

# Wait 20 seconds for page to load
timeout = 20
try:
    # Here we want to reach tournamentTable div
    # Go from 'display : none' to 'display : block' when information are loaded
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

# Selenium is usefull to get the page with dynamic behaviour 
# BeautifulSoup is better to parse html
tournament_tbl_html = browser.find_element_by_id('tournamentTable').get_attribute("innerHTML")
tournament_tbl_soup = BeautifulSoup(tournament_tbl_html, "html.parser")

# get all tr
# except first one isn't usefull 'soccer ligue 1 2003/2004' :
rows = tournament_tbl_soup.find_all('tr')[1:]
date = None
for row in rows:
    cols=row.find_all('td')
    if(not cols):
        # TODO Create a fuction to transalte litteral day to interger
        # then create Date and extract day
        date = row.find('span').text
    elif (cols[0].text) : 
        print("Date     : "+date)
        print("Hours    : " + cols[0].text)
        teams = cols[1].text.split(" - ")
        print("TeamA    : " + teams[0])
        print("TeamB    : " + teams[1])
        score = cols[2].text.split(":")
        print("ScoreA   : " + score[0])
        print("ScoreB   : " + score[1])
        print("OddsA    : " + cols[3].find('a').text)
        print("OddsDraw : " + cols[4].find('a').text)
        print("OddsB    : " + cols[5].find('a').text)
        print("")

exit()

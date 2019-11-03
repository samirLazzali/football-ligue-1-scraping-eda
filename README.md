# football-ligue-1-scraping-eda

### Description
Analyse des matches de ligue 1 depuis la saison 2003/2004. Le but est d'en apprendre plus sur les cotes fixées par les bookmakers. Sont-elles correctes ? Est ce possible de prédire les matches de ligue 1 ? Si les résultats de ce projet son concluant, il pourrait être intéressant de mettre en place 
des indicateurs afin d'aider les parieurs et éventuellement s'étendre à d'autres ligues


### Install 
pip install -r requirements.txt

# Data

```
date : date de la rencontre (2019-10-26 18:00:00)
day : jour de la rencontre (Saturday)
hours : heure de la rencontre(18:00)
odds_a : cote de la premiere equipe(2.36)
odds_b : cote de la seconde equipe (3.19)
odds_draw : cote null (3.27)
outcome_effectif : Vinqueur au score (HOME - AWAY - DRAW)
outcome_odds : Cote la plus petite, represente le score du bookmaker (HOME - AWAY - DRAW)
prediction_odds : Le bookmaker avait il juste ? (1)
score_a : Score de l'équipe A(2) 
score_b : Score de l'équipe B (0)
season : Saison (2019/2020)
team_a : Equipe A(Brest)
team_b : Equipe B (Dijon)

```

### Resources

We will leverage these Resources
* [Selenium](https://pypi.python.org/pypi/selenium)
* [ChromeDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* [Selenium-Python ReadTheDocs](http://selenium-python.readthedocs.io/)
* Fork from : [Selenium-Webscraping-Example](https://github.com/TheDancerCodes/Selenium-Webscraping-Example)

import re
import requests
from bs4 import BeautifulSoup

# Header information
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}

""" ===========================================================================
PROCEDURE:
    get_weather
PARAMETERS:
    None - no parameters
PURPOSE:
    accesses weather.com and scrapes weather data of interest for Grinnell, IA
PRODUCES:
    weather_info, a tuple holding 10 different weather data
=========================================================================== """
def get_weather():

    # Get URL of interest
    url = "https://weather.com/weather/today/l/6ed841aa19e860661a182534bea28f9508358831f8de4cb3dc763bcf6873def5"

    # Get html using requests.get()
    req = requests.get(url, headers=headers)

    # Check for any errors in request responses
    req.raise_for_status()

    # Make a beautiful soup with the attained html
    soup = BeautifulSoup(req.text, features="html.parser")

    # =========================================================================
    # 01. Find element containing current temperature value
    cur_temp = soup.find("span", class_="CurrentConditions--tempValue--3KcTQ")

    # Attain temp in farenheit and also convert to celsius
    cur_temp_f = cur_temp.get_text()[:-1]
    cur_temp_c = round( (int(cur_temp_f) - 32) * (5/9) )

    # =========================================================================
    # 02. Attain timestamp of the temperature measurement
    cur_time = soup.find("div", class_="CurrentConditions--timestamp--1SWy5")
    cur_time_str = cur_time.get_text()[6:]

    # =========================================================================
    # 03. Attain other condition information
    cond = soup.find("div", class_="CurrentConditions--phraseValue--2xXSr")
    cond_str = cond.get_text()

    # Details
    det = soup.find_all("div", class_="WeatherDetailsListItem--wxData--23DP5")
    wind_str  = det[1].get_text()  # Wind info
    humid_str = det[2].get_text()  # Humidity info

    # Precipitation
    precip = soup.find("div", class_="CurrentConditions--precipValue--RBVJT")


    # If precipitation information exists
    if precip:
        precip_str = precip.get_text()
        cond_precip_str = cond_str + ", &nbsp" + precip_str
    else:
        cond_precip_str = cond_str

    # =========================================================================
    # 04. Attain forecast throughout the day
    forecast = soup.find("div", class_="TodayWeatherCard--TableWrapper--13jpa")
    day = forecast.find_all("div", class_="Column--temp--2v_go")

    mng = day[0].get_text()[:-1]+"°F"  # Morning
    afn = day[1].get_text()[:-1]+"°F"  # Afternoon
    evn = day[2].get_text()[:-1]+"°F"  # Evening
    ovn = day[3].get_text()[:-1]+"°F"  # Overnight

    # =========================================================================

    weather_info = (cur_time_str, cur_temp_f, cur_temp_c, cond_precip_str, 
                    wind_str, humid_str, mng, afn, evn, ovn)

    return weather_info

""" ===========================================================================
PROCEDURE:
    get_covid_cases
PARAMETERS:
    None - no parameters
PURPOSE:
    accesses the New York Times COVID-19 section and scrapes relevant data 
    regarding COVID-19 cases in Iowa and its neighboring states 
PRODUCES:
    covid_info, a tuple holding 5 different COVID-19 data
=========================================================================== """
def get_covid_cases():

    # Get URL of interest
    url = "https://www.nytimes.com/interactive/2020/us/iowa-coronavirus-cases.html"

    # Get html using requests.get()
    req = requests.get(url, headers=headers)

    # Check for any errors in request responses
    req.raise_for_status()

    # Make a beautiful soup with the attained html
    soup = BeautifulSoup(req.text, features="html.parser")

    # =========================================================================
    # 01. Attain COVID cases information
    counts = soup.find("tr", class_="counts__row")
    tot_cases = counts.find_all("td")[1].get_text()
    num_cases = counts.find_all("td")[2].get_text()

    # =========================================================================
    # 02. Attain updated date information
    cnt_header = soup.find("thead", class_="counts__header")
    cnt_date   = cnt_header.find_all("th")[2].get_text()[3:]

    # =========================================================================
    # 03. Attain summary paragraph
    story = soup.find("div", class_="g-story")
    story_p = story.find_all("p", class_="g-body")[0].get_text().strip()

    # =========================================================================
    # 04. Attain new cases in neighboring states
    url_temp = """
    https://www.nytimes.com/interactive/2020/us/{}-coronavirus-cases.html"""

    states = ["minnesota", "wisconsin", "illinois", "missouri", "nebraska", 
              "south-dakota"]

    # =========================================================================

    # Create an empty dictionary to add key/value below
    covid_states = {}

    for state in states:

        # Follow the same step as before
        res = requests.get(url_temp.format(state), headers=headers)
        res.raise_for_status()
        soup2 = BeautifulSoup(res.text, features="html.parser")

        counts = soup2.find("tr", class_="counts__row")
        new_cases = counts.find_all("td")[2].get_text()

        # Add to the dictionary (key:state, value:new_cases)
        covid_states[state.title()] = new_cases

    covid_info = (num_cases, cnt_date, tot_cases, story_p, covid_states)
    
    return covid_info

""" ===========================================================================
PROCEDURE:
    get_us_headlines
PARAMETERS:
    None - no parameters
PURPOSE:
    accesses the New York Times main page and scrapes three different top 
    U.S. headline news displayed there
PRODUCES:
    us_headlines, a list of three tuples, each of which holds the news title, 
    one-line description, and a link to the page
=========================================================================== """
def get_us_headlines():

    # =========================================================================
    # 01. Attain Headline information from NYT

    # Get URL of interest
    url = "https://www.nytimes.com/"

    # Get html using requests.get()
    req = requests.get(url, headers=headers)

    # Check for any errors in request responses
    req.raise_for_status()

    # Make a beautiful soup with the attained html
    soup = BeautifulSoup(req.text, features="html.parser")

    # Attain headline information clump 
    boxes  = soup.find_all("div", class_="css-6p6lnl")[0:3]

    # =========================================================================
    
    # Create an empty list to append headline news below
    us_headlines = []

    for idx, box in enumerate(boxes):

        # Get headline
        headline = box.h2.get_text()

        # Get link
        link = box.a["href"]

        # If href is only partial, attach to the url
        if link[0:5] != "https":
            link = url[0:-1] + box.a["href"]

        # Get one-line summary of headline
        # special case only for NYT
        if box.li:
            desc = box.li.get_text()
        elif box.p:
            desc = box.p.get_text()
        else:
            desc = ""

        us_headlines.append((headline, desc, link))

    return us_headlines

""" ===========================================================================
PROCEDURE:
    get_world_headlines
PARAMETERS:
    None - no parameters
PURPOSE:
    accesses BBC World News and scrapes three different top world headline 
    news displayed there
PRODUCES:
    world_headlines, a list of three tuples, each of which holds the news 
    title, one-line description, and a link to the page
=========================================================================== """
def get_world_headlines():

    # 02. Attain Headline information from BBC
    # Get URL of interest
    url = "https://www.bbc.com/news/world"

    # Get html using requests.get()
    req = requests.get(url, headers=headers)

    # Check for any errors in request responses
    req.raise_for_status()

    # Make a beautiful soup with the attained html
    soup = BeautifulSoup(req.text, features="html.parser")

    # Attain headline information clump 
    boxes  = soup.find_all("div", class_="gs-c-promo-body")[1:4]
    
    # =========================================================================
    
    # Create an empty list to append headline news below
    world_headlines = []

    for idx, box in enumerate(boxes):

        # Get headline
        headline = box.h3.get_text()

        # Get link
        link = "https://www.bbc.com" + box.a["href"]

        # Get one-line summary of headline
        desc = box.p.get_text()

        world_headlines.append((headline, desc, link))

    return world_headlines
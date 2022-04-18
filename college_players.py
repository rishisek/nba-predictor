from bs4 import BeautifulSoup
import requests
import pandas as pd
from progressbar import ProgressBar
pbar = ProgressBar()
from tqdm import tqdm

bigten = ['Chicago', 'Kentucky', 'Kansas', 'Nebraska', 'Iowa', 'Rutgers', 'Indiana', 'Michigan State', 'Maryland', 'Ohio State', 'Penn State', 'Minnesota', 'Purdue', 'Illinois', 'Wisconsin', 'Michigan', 'Northwestern']

url = "https://www.sports-reference.com/cbb/players"

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

def getAndParseUrl(url):
    results = requests.get(url)
#     time.sleep(1)
    soup = BeautifulSoup(results.text, 'html.parser')
    return soup

root_url = url[:32]

letter_link = []
for links in tqdm(string.ascii_lowercase):
    results = soup.find('a', {'href': f"/cbb/players/{links}-index.html"})['href']
    letter_link.append(results)

full_url = []
for link in tqdm(letter_link):
    letters_url = root_url + link
    full_url.append(letters_url)

parsed_letters = []
for urls in tqdm(full_url):
    soup = getAndParseUrl(urls)
#     print(soup)
    parsed_letters.append(soup)

# print(parsed_letters)

def p_parsing(page_number):
    player_time = []
    soup = parsed_letters[page_number].find_all('p')[1:]
    for text in soup:
        t = text.find_all('a')
        try:
            times = text.small.text[1:10]
            played = text.a['href']
            schools = t[1:]
            schools_ls = []
            for school in schools:
                schools_ls.append(school.text)
            # if len(schools_ls) > 1:
            #     print(schools_ls)
#             take only dates after 2003
            if int(times[:4]) >= 2003 and len(list(set(schools_ls) & set(bigten))) > 0:
                player_time.append(root_url + played)
        except:
            pass
    return player_time

# print(p_parsing(0))
full_list = []
for i in tqdm(range(0,26)):
    full_list.extend(p_parsing(i))

# players_site = []
# for dic in tqdm(full_list):
#     urls = dic['url']
#     players_site.append(urls)

rest_of_players = []
for url in tqdm(full_list):
    soup = getAndParseUrl(url)
    rest_of_players.append(soup)

def stat_compiler(list_soups):
    list1 = []
    for exp in list_soups:
        name = exp.h1.text[1:len(exp.h1.text) - 1]
        try:
            height = exp.find('span', {'itemprop': "height"}).text
        except:
            height = "Unknown"
        try:
            weight = exp.find('span', {'itemprop': "weight"}).text[:3]
        except:
            weight = "Unknown"
        try:
            position = exp.p.strong.nextSibling.strip()
        except:
            position = "Unknown"
        # school = exp.find('td', attrs={"data-stat": "school_name"}).text

        totals = exp.find_all('table', id='players_per_game')[0].find('tfoot').find_all('td')[2:]

        games = int(totals[0].text)
        # games_started = int(exp.find('td', attrs={"data-stat": "gs"}).text)
        try:
            minutes_per = int(totals[2].text)
        except:
            minutes_per = 0
        # try:
        #     field_pct = float(exp.find('td', attrs={"data-stat": "fg_pct"}).text)
        # except:
        #     field_pct = 0.0
        try:

            two_pct = float(totals[8].text)
        except:
            two_pct = 0.0
        try:

            three_pct = float(totals[11].text)
        except:
            three_pct = 0.0
        try:
            free_pct = float(totals[14].text)
        except:
            free_pct = 0.0
        field_goal = float(totals[3].text)
        field_attmp = float(totals[4].text)
        two_ptrs = float(totals[6].text)
        # two_pattmp = float(exp.find('td', attrs={"data-stat": "fg2a_per_g"}).text)
        three_ptrs = float(totals[9].text)
        # three_pattmp = float(exp.find('td', attrs={"data-stat": "fg3a_per_g"}).text)
        free_throws = float(totals[12].text)
        # free_attmp = float(exp.find('td', attrs={"data-stat": "fta_per_g"}).text)
        tot_reb = float(totals[17].text)
        assist = float(totals[18].text)
        steals = float(totals[19].text)
        blocks = float(totals[20].text)
        points = float(totals[23].text)
        try:
            fouls = float(totals[22].text)
        except:
            fouls = 0

        advanced = exp.find_all('table', id='players_advanced')[0].find('tfoot').find_all('td')[2:]
        
        
        try:
            oreb = float(advanced[9].text)
        except:
            oreb = 0.0
        try:
            dreb = float(advanced[10].text)
        except:
            dreb = 0.0
        try:
            tov = float(advanced[15].text)
        except:
            tov = 0.0
        try:
            usg = float(advanced[16].text)
        except:
            usg = 0.0
        try:
            per = float(advanced[3].text)
        except:
            per = 0.0
        try:
            ws = float(advanced[20].text)
        except:
            ws = 0.0
        try:
            bpm = float(advanced[25].text)
        except:
            bpm = 0.0
        if position != "":
            position = position.strip('\n')

        dict1 = {'name': name,
                'height': height,
                'weight': weight, 
                'position': position,
                'games_played': games, 
                # 'games_started': games_started, 
                'min_per': minutes_per,
                'field_goal': field_goal, 
                'field_attmps': field_attmp, 
                # 'field_pct': field_pct,
                'two_pointer': two_ptrs, 
                # 'two_pattamps': two_pattmp, 
                'two_pct': two_pct,
                'three_ptrs': three_ptrs, 
                # 'three_pattmp': three_pattmp, 
                'three_pct': three_pct,
                'free_throws': free_throws, 
                # 'free_attmps': free_attmp, 
                'free_pct': free_pct,
                'assists': assist, 
                'steals': steals, 
                'blocks': blocks, 
                'points': points, 
                'personal_fouls': fouls,
                'usg': usg,
                'off_reb': oreb, 
                'def_reb': dreb,
                'total_reb': tot_reb, 
                'player_eff': per, 
                'tv_per_game': tov,
                'ws': ws,
                'bpm': bpm}
        list1.append(dict1)
    return list1

player_list = stat_compiler(rest_of_players)

df = pd.DataFrame.from_dict(player_list)

df.to_csv('players_stats.csv')

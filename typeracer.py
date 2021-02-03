from requests import get 
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_history(username):
	url = f'https://data.typeracer.com/pit/race_history?user={username}&n=100&startDate='
	headers = {'User-Agent': "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
						 "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
	response = get(url, headers=headers, timeout=20)
	assert response.status_code == 200 # Test to see if we received data
	soup = BeautifulSoup(response.content, 'lxml')
	return soup

date_converter = {'Jan.': 'January', 'Feb.': 'February', 'Aug.': 'August', 'Sept.': 'September',
'Oct.': 'October', 'Nov.': 'November', 'Dec.': 'December'}

def graph_history(soup):
	info_table = soup.find('table', {'class': 'scoresTable'})
	scores = pd.DataFrame(columns={'Race#', 'Date', 'WPM', 'Accuracy'})
	values = info_table.get_text().split()[8:]
	for i in range(len(values))[::9]:
		racenum, wpm, _, accuracy, _, _, *date = values[i:i+9]
		if date[0] in date_converter:
			date[0] = date_converter[date[0]]
		scores = scores.append({'Race#': racenum, 'Date': datetime.strptime(' '.join(date), '%B %d, %Y'), 'WPM': wpm, 'Accuracy': accuracy}, ignore_index=True)
	scores = scores.set_index(['Date']).sort_index(ascending=False)
	return scores

print(graph_history(get_history('itypesomewhatalot')))
	
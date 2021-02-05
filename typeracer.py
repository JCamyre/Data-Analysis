from requests import get 
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np

months = mdates.MonthLocator()

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
		accuracy = float(accuracy[:-1])
		wpm = int(wpm)
		if date[0] in date_converter:
			date[0] = date_converter[date[0]]
		scores = scores.append({'Race#': racenum, 'Date': datetime.strptime(' '.join(date), '%B %d, %Y'), 'WPM': wpm, 'Accuracy': accuracy}, ignore_index=True)
	scores = scores.set_index(['Date']).sort_index(ascending=False)
	return scores

data = graph_history(get_history('itypesomewhatalot'))[:100]
fig, ax = plt.subplots()
ax.plot(data['Race#'], 'WPM', data=data)	

# ax.xaxis.set_major_locator(months)
# datemin = np.datetime64(data.index[-1], 'Y')
# datemax = np.datetime64(data.index[0], 'Y') + np.timedelta64(1, 'Y')
# ax.set_xlim(datemin, datemax)

ax.set_ylabel('WPM')
ax.set_ylim(data['WPM'].min()-20, data['WPM'].max()+20)
# Have x-axis for race #, then have a secondary one for date
# 

# plt.subplot(2, 1, 2)
# plt.plot(data.index, data['Accuracy'], 'o-')
# plt.title('Accuracy over time')

plt.show()

from requests import get 
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def get_history(username):
	url = f'https://data.typeracer.com/pit/race_history?user={username}&n=100&startDate='
	headers = {'User-Agent': "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
						 "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
	response = get(url, headers=headers, timeout=20)
	assert response.status_code == 200 # Test to see if we received data
	soup = BeautifulSoup(response.content, 'lxml')
	return soup

def graph_history(soup):
	info_table = soup.find('table', {'class': 'scoresTable'})
	scores = pd.DataFrame(columns={'Race #', 'Date', 'WPM', 'Accuracy', 'Position'})
	print(info_table.get_text().split())


graph_history(get_history('itypesomewhatalot'))
	
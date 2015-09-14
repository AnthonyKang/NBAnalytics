from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import re
from string import ascii_lowercase


def getPlayerLinks():
	
	playerLinks = {}
	
	for c in ascii_lowercase:
		links = []
		html = urlopen("http://www.basketball-reference.com/players/"+c+"/")
		soup = BeautifulSoup(html, 'lxml')
		for a in soup.find_all('a', href=re.compile("/players/"+c+"/")):
			links.append("http://www.basketball-reference.com"+a['href'])
		playerLinks[c] = links
		

	return playerLinks

def main():
	playerLinks = getPlayerLinks()
	print(playerLinks['z'])

if __name__ == "__main__":
	main()
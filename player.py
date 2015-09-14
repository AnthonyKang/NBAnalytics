from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import re


class Player:

	def __init__(self, url):
		#self.name = name
		self.url = url
		self.html = urlopen(self.url).read()
		self.soup = BeautifulSoup(self.html, "lxml")
		self.curryear = datetime.now().year
		
		self.draftYear = self.soup.find_all(string=re.compile("Draft"))[1][0:4]
		self.totals_labels = ["Season", "Age", "Tm", "Lg", "Pos", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]


	def getTotals(self):
		totals_table = []
		for i in range(int(self.draftYear),int(self.curryear)+1):
			totals_table.append(self.soup.find(id="totals." + str(i)))
		
		print(totals_table)
		


def main():
	russelWestbrook = Player("http://www.basketball-reference.com/players/w/westbru01.html")
	russelWestbrook.getTotals()
	stephenCurry = Player("http://www.basketball-reference.com/players/c/curryst01.html")
	stephenCurry.getTotals()


if __name__ == "__main__":
	main()



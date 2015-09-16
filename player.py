from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import re
from crawler import *

totals_labels = ["Season", "Age", "Tm", "Lg", "Pos", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
advanced_labels = totals_labels[0:5] + ["G", "MP", "PER", "TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%", "STL%", "BLK%", "TOV%", "USG%", "__", "OWS", "DWS", "WS", "WS/48", "__", "OBPM", "DBPM", "BPM", "VORP"]
print(len(advanced_labels))
print(len(["PER", "TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%", "STL%", "BLK%", "TOV%", "USG%", "__", "OWS", "DWS", "WS", "WS/48", "__", "OBPM", "DBPM", "BPM", "VORP"]))
class Player:

	def __init__(self, url):
		#self.name = name
		self.url = url
		self.html = urlopen(self.url).read()
		self.soup = BeautifulSoup(self.html, "lxml")
		self.curryear = datetime.now().year
			
		self.draftYear = self.soup.find_all(string=re.compile("[0-9]+ NBA Draft"))[0][0:4]
		
		self.totals_labels = ["Season", "Age", "Tm", "Lg", "Pos", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
		self.poss_labels = self.totals_labels + ["","ORtg", "DRtg"]
		self.advanced_labels = self.totals_labels[0:5] + ["PER", "TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%", "STL%", "BLK%", "TOV%", "USG%", "", "OWS", "DWS", "WS", "WS/48", "", "OBPM", "DBPM", "BPM", "VORP"]

	def getTotals(self, tableName):
		#tableName = "totals", "per_minute", "per_game", "per_poss", "advanced"
		totals_table = []
		for i in range(int(self.draftYear)+1,int(self.curryear)+1):
			total = {}

			year = self.soup.find(id=tableName + "." + str(i))
			table_data = year.find_all('td')

			if tableName == 'per_poss':
				labels = self.poss_labels
			elif tableName == 'advanced':
				labels = advanced_labels
			else:
				labels = self.totals_labels

			print(table_data)
			print(len(labels))
			for j in range(0,len(labels)):
				if j == 0 or j == 2 or j == 3:
					total[labels[j]] = table_data[j].find('a').contents[0]
				else:
					if len(table_data[j].contents) > 0:
						total[labels[j]] = table_data[j].contents[0]
					#if tableName == 'per_poss':
					#	print(table_data[j].contents)
					#	if j != 29:
					#		total[labels[j]] = table_data[j].contents[0]
					#else:
					#	total[labels[j]] = table_data[j].contents[0]

			totals_table.append(total)

		return totals_table


		


def main():
	russelWestbrook = Player("http://www.basketball-reference.com/players/w/westbru01.html")
	#russelWestbrook.getTotals("per_minute")
	stephenCurry = Player("http://www.basketball-reference.com/players/c/curryst01.html")
	print(stephenCurry.getTotals("advanced"))



if __name__ == "__main__":
	main()



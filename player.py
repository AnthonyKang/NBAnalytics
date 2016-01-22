from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import re
from crawler import *
import json

totals_labels = ["Season", "Age", "Tm", "Lg", "Pos", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
advanced_labels = totals_labels[0:5] + ["G", "MP", "PER", "TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%", "STL%", "BLK%", "TOV%", "USG%", "__", "OWS", "DWS", "WS", "WS/48", "__", "OBPM", "DBPM", "BPM", "VORP"]
poss_labels = totals_labels + ["","ORtg", "DRtg"]
shooting_labels = advanced_labels[0:7] + ["FG%", "Dist", "FGA_2P", "FGA_0-3","FGA_10-16", "FGA_16<3", "3P", "FG_2P","FG_0-3","FG_3-10","FG_10-16","FG_16<3","3P","DunksAstd", "DunksPer", "DunksMd", "CornerAstd", "Corner3A", "Corner3P", "HeavesAtt", "HeavesMd"]


class Player:

	def __init__(self, url):
		#self.name = name
		self.url = url
		self.html = urlopen(self.url).read()
		self.soup = BeautifulSoup(self.html, "lxml")
		self.currYear = datetime.now().year
		self.playerName = self.soup.find_all('h1')[0].string
		self.draftYear = self.soup.find_all(string=re.compile("[0-9]+ NBA Draft"))[0][0:4]
		
	
	def getTotals(self, tableName):
		#tableName = "totals", "per_minute", "per_game", "per_poss", "advanced", "shooting"
		totals_table = []
		for i in range(int(self.draftYear)+1,int(self.curryear)+1):
			total = {}

			year = self.soup.find(id=tableName + "." + str(i))
			table_data = year.find_all('td')

			if tableName == 'per_poss':
				labels = poss_labels
			elif tableName == 'advanced':
				labels = advanced_labels
			elif tableName == 'shooting':
				labels = shooting_labels
			else:
				labels = totals_labels

			#print(table_data)
			#print(len(labels))
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

	def getGameLog(self, year):

		print(self.url[:-5])
		html = urlopen(self.url[:-5] + '/gamelog/' + str(year) + '/')
		print(self.url[:-5] + '/gamelog/' + str(year) + '/')
		soup = BeautifulSoup(html, 'lxml')
		table = soup.find(id='pgl_basic')
		header_tags = table.find_all('th')
		headers = []
		for th in header_tags[0:31]:
			headers.append(th.get_text())
		headers[5] = 'away'
		headers[7] = 'W/L'

		games = []
		stats = []
		for game in table.find_all(id=re.compile('pgl_basic.[0-9]+')):
			for stat in game.find_all('td'):
				stats.append(stat.get_text())
			games.append(tuple(stats))
			stats = []

		return (headers, games)
		#game = table.find(id=re.compile('pgl_basic.[0-9]+'))
		#stat = game.find_all('td')
		#print(stat)

def writeTSV(table, tableName, fileName):
	FILEOUT = open(fileName+".json", 'w+')
	
	if tableName == 'per_poss':
		labels = poss_labels
	elif tableName == 'advanced':
		labels = advanced_labels
	elif tableName == 'shooting':
		labels = shooting_labels
	else:
		labels = totals_labels

	FILEOUT.write('[')
	for year in table:
		#for keys in labels:
		#	FILEOUT.write(keys +'\t' + year[keys]+'\n')
		json.dump(year,FILEOUT)
		FILEOUT.write(',')
		FILEOUT.write('\n')
	FILEOUT.write(']')
			

		


def main():
	#russelWestbrook = Player("http://www.basketball-reference.com/players/w/westbru01.html")
	#russelWestbrook.getTotals("per_minute")
	stephenCurry = Player("http://www.basketball-reference.com/players/c/curryst01.html")
	#shooting = stephenCurry.getTotals("shooting")
	#writeTSV(shooting, "shooting", "curry_shooting")
	headers, games = stephenCurry.getGameLog(2015)
	print(stephenCurry.playerName)
	print(len(games))

if __name__ == "__main__":
	main()



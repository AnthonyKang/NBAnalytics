import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from player import *

class DbManager:

	def __init__(self, dbName):
		self.dbName = dbName
		self.client = MongoClient()


	def insertGameLog(self):

		# select a player
		player = Player('http://www.basketball-reference.com/players/w/westbru01.html')

		
		# initialize the players and gameLogs databases
		gameLogDb = self.client.gameLogs
		
		yearIdList = []
		# for the each the player has played
		for i in range(int(player.draftYear) + 1, int(player.currYear) + 1):
		#for i in range(2009,2010):
			yearLogHeaders , yearAllGames = player.getGameLog(i)
			yearId = ObjectId()
			
			# for each game of the year
			gameIdList = []
			for game in yearAllGames:
			 	
				# create a game Id as well as game object
			 	gameStatDic = {}
			 	gameId = ObjectId()

			 	# insert stats in to game object
			 	for stat in range(len(game)):
			 		gameStatDic[yearLogHeaders[stat]] = game[stat]

			 	# give each game a game Id
			 	gameStatDic['_id'] = gameId
			 	gameStatDic['name'] = player.playerName

			 	# insert game in to database
			 	gameLogDb.games.insert_one(gameStatDic)

			 	# save ObjectIds of each game to associate with the year
			 	gameIdList.append(gameId)

			# insert the year in to the database
			year = {
				'_id' : yearId,
				'type' : 'gameLog',
				'name' : player.playerName,
				'games' : gameIdList
			}

			gameLogDb.years.insert_one(year)

			# save yearIds of each year to associate with player
			yearIdList.append(yearId)

		# insert player in to gamelogs datbase
		playerEntry = {
			'name' : player.playerName,
			'years' : yearIdList
		}

		gameLogDb.players.insert_one(playerEntry)

						



	





def main():
	# client = MongoClient()

	# playersDb = client.players
	# gameLogDb = client.gameLogs

	# newId = ObjectId()
	# stephCurryGameLog = {
	# 	'_id' : newId,
	# 	'year' : '20162015'
	# 	'games' : [1,2,3,4]
	# }

	# playersDb.gameLogs.insert_one(stephCurryGameLog)



	# StephCurry = {
	# 	'playerName' : 'Stephen Curry',
	# 	'gameLog' : newId
	# }

	# playersDb.players.insert_one(StephCurry)
	# playersDb.players.update_one({'playerName' : 'Stephen Curry'}, {'$set': {'gameLog' : newId}})

	myDb = DbManager('gameLogs')
	myDb.insertGameLog()



if __name__ == "__main__":
	main()
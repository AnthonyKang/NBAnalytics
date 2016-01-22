import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

class DbManager:

	def __init__(self, dbName):
		self.dbName = dbName
		self.client = MongoClient()


	def insertGameLog(self, stats):

		# create a id for the new year
		newId = ObjectId()

		for stat in stats







def main():
	client = MongoClient()

	playersDb = client.players
	gameLogDb = client.gameLogs

	newId = ObjectId()
	stephCurryGameLog = {
		'_id' : newId,
		'year' : '20162015'
	}

	playersDb.gameLogs.insert_one(stephCurryGameLog)



	StephCurry = {
		'playerName' : 'Stephen Curry',
		'gameLog' : newId
	}

	playersDb.players.insert_one(StephCurry)
	playersDb.players.update_one({'playerName' : 'Stephen Curry'}, {'$set': {'gameLog' : newId}})



if __name__ == "__main__":
	main()
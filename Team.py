
class team:

	def __init__(self,name,index):
		self.index = index
		self.name = name
		self.gamesList = []
		self.points = 0
		## Scored and Conceded
		self.hScored_first = 0
		self.hConceded_first = 0
		self.hScored_second = 0
		self.hConceded_second = 0
		self.aScored_first = 0
		self.aConceded_first = 0
		self.aScored_second = 0
		self.aConceded_second = 0
		## Diffs
		self.hRate_first = 0
		self.hRate_second = 0
		self.aRate_first = 0
		self.aRate_second = 0
		## Shots
		self.hShots = 0
		self.aShots = 0
		self.hShotsT = 0
		self.aShotsT = 0
		## Corners
		self.hCorners = 0
		self.aCorners = 0


	def addGame(self,game):
		self.gamesList.append(game)

	def pointsCalc_home(self,game):
		if game.hScore > game.aScore:
			self.points +=3
		elif game.hScore == game.aScore:
			self.points +=1

	def pointsCalc_away(self,game):
		if game.hScore < game.aScore:
			self.points +=3
		elif game.hScore == game.aScore:
			self.points +=1

	def getRatesDiffs(self):
		hDiff_first = 0
		hDiff_second = 0
		aDiff_first = 0
		aDiff_second = 0
		totalHGames = 0
		totalAGames = 0
		for game in reversed(self.gamesList): # for every game in record	
			home = 0
			if(self.index == game.hIndex): # discover if team played home or away
				home = 1
			elif (self.index != game.aIndex):
				print("ERROR: This team didnt took part on this game")

			# Register diff of goals between teams at first and second half
			if home == 1 and totalHGames < 200:
				totalHGames += 1
				hDiff_first += game.hInt - game.aInt
				hDiff_second += (game.hScore-game.hInt) - (game.aScore-game.aInt)
			elif totalAGames < 200:
				totalAGames += 1
				aDiff_first += -game.hInt + game.aInt
				aDiff_second += -(game.hScore-game.hInt) + (game.aScore-game.aInt)

		self.hRate_first = hDiff_first / totalHGames
		self.hRate_second = hDiff_second / totalHGames
		self.aRate_first =  aDiff_first / totalAGames
		self.aRate_second = aDiff_second / totalAGames

	def getGoalsData(self):
		hScored_first = 0
		hScored_second = 0
		aScored_first = 0
		aScored_second = 0
		hConceded_first = 0
		hConceded_second = 0
		aConceded_first = 0
		aConceded_second = 0
		totalHGames = 0
		totalAGames = 0
		for game in reversed(self.gamesList): # for every game in record	
			home = 0
			if(self.index == game.hIndex): # discover if team played home or away
				home = 1
			elif (self.index != game.aIndex):
				print("ERROR: This team didnt took part on this game")

			# Register diff of goals between teams at first and second half
			if home == 1:
				totalHGames += 1
				hScored_first += game.hInt	
				hConceded_first += game.aInt
				hScored_second += (game.hScore-game.hInt)
				hConceded_second += (game.aScore-game.aInt)
			else:
				totalAGames += 1
				aScored_first += game.aInt	
				aConceded_first += game.hInt
				aScored_second += (game.aScore-game.aInt)
				aConceded_second += (game.hScore-game.hInt)

		self.hScored_first = hScored_first / totalHGames
		self.hScored_second = hScored_second / totalHGames
		self.hConceded_first = hConceded_first / totalHGames
		self.hConceded_second = hConceded_second / totalHGames
		
		self.aScored_first = aScored_first / totalAGames
		self.aScored_second = aScored_second / totalAGames
		self.aConceded_first = aConceded_first / totalAGames
		self.aConceded_second = aConceded_second / totalAGames


	def getCornersData(self):
		hCorners = 0
		aCorners = 0
		totalHGames = 0
		totalAGames = 0
		for game in reversed(self.gamesList): # for every game in record	
			home = 0
			if(self.index == game.hIndex): # discover if team played home or away
				home = 1
			elif (self.index != game.aIndex):
				print("ERROR: This team didnt took part on this game")

			# Register diff of goals between teams at first and second half
			if home == 1:
				totalHGames += 1
				hCorners += game.hCorners
			else:
				totalAGames += 1
				aCorners += game.aCorners

		self.hCorners = hCorners / totalHGames
		self.aCorners = aCorners / totalAGames

	def getShotsData(self):
		hShots = 0
		aShots = 0
		hShotsT = 0
		aShotsT = 0
		totalHGames = 0
		totalAGames = 0
		for game in reversed(self.gamesList): # for every game in record	
			home = 0
			if(self.index == game.hIndex): # discover if team played home or away
				home = 1
			elif (self.index != game.aIndex):
				print("ERROR: This team didnt took part on this game")

			# Register diff of goals between teams at first and second half
			if home == 1:
				totalHGames += 1
				hShots += game.hShots
				hShotsT += game.hShotsTarget
			else:
				totalAGames += 1
				aShots += game.aShots
				aShotsT += game.aShotsTarget

		self.hShots = hShots / totalHGames
		self.aShots = aShots / totalAGames
		self.hShotsT = hShotsT / totalHGames
		self.aShotsT = aShotsT / totalAGames

	def getFoulsData(self):
		hFouls = 0
		aFouls = 0
		totalHGames = 0
		totalAGames = 0
		for game in reversed(self.gamesList): # for every game in record	
			home = 0
			if(self.index == game.hIndex): # discover if team played home or away
				home = 1
			elif (self.index != game.aIndex):
				print("ERROR: This team didnt took part on this game")

			# Register diff of goals between teams at first and second half
			if home == 1:
				totalHGames += 1
				hFouls += game.hFouls
			else:
				totalAGames += 1
				aFouls += game.aFouls

		self.hFouls = hFouls / totalHGames
		self.aFouls = aFouls / totalAGames

	def getCardsData(self):
		hYellow = 0
		aYellow = 0
		hRed = 0
		aRed = 0
		totalHGames = 0
		totalAGames = 0
		for game in reversed(self.gamesList): # for every game in record	
			home = 0
			if(self.index == game.hIndex): # discover if team played home or away
				home = 1
			elif (self.index != game.aIndex):
				print("ERROR: This team didnt took part on this game")

			# Register diff of goals between teams at first and second half
			if home == 1:
				totalHGames += 1
				hYellow += game.hYellow
				hRed += game.hRed
			else:
				totalAGames += 1
				aYellow += game.aYellow
				aRed += game.aRed

		self.hYellow = hYellow / totalHGames
		self.aYellow = aYellow / totalAGames
		self.hRed = hRed / totalHGames
		self.aRed = aRed / totalAGames
import sys

class game:
	def __init__(self,hIndex,aIndex,row):
		self.hIndex = hIndex
		self.aIndex = aIndex
		self.hScore = int(row[5])
		self.aScore = int(row[6])
		self.hInt = int(row[8])
		self.aInt = int(row[9])
		## new data
		if "E" in sys.argv[1]:
			i = 1
		else:
			i = 0

		self.hShots = int(row[11+i])
		self.aShots = int(row[12+i])
		self.hShotsTarget = int(row[13+i])
		self.aShotsTarget = int(row[14+i])
		self.hFouls = int(row[15+i])
		self.aFouls = int(row[16+i])
		self.hCorners = int(row[17+i])
		self.aCorners = int(row[18+i])
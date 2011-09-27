#!/usr/bin/python
import sys

DEBUG = 0

class Place:
	EMPTY = 0
	WHITE = 1
	BLACK = 2
	def __init__(self):
		self.state = self.EMPTY
	def CheckPlace(self):
		return self.state
	def SetPlace(self, value):
		assert((value == self.EMPTY) or (value == self.WHITE) or (value == self.BLACK))
		self.state = value
	def Print(self):
		sys.stdout.write("[")
		if self.state == self.EMPTY:
			sys.stdout.write(" ")
		elif self.state == self.WHITE:
			sys.stdout.write("W")
		else:
			sys.stdout.write("B")
		sys.stdout.write("] ")

class Quad:
	CW = 0
	CCW = 1
	def __init__(self):
		self.places = [[Place(), Place(), Place()], [Place(), Place(), Place()], [Place(), Place(), Place()]]
	def Rotate(self, direction):
		assert((direction == self.CW) or (direction == self.CCW))
		tempPlaces = Quad()
		pos = [0, 0]
		if direction == self.CW:
			row = 2
			while row >= 0:
				col = 0
				while col <= 2:
					tempPlaces.places[pos[0]][pos[1]].SetPlace(self.places[row][col].CheckPlace())
					#print "tempPlaces[", pos[0], ",", pos[1], "] = places[", row, ",", col,"] = ", self.places[row][col].CheckPlace()
					col += 1
					pos[0] += 1
				row -= 1
				pos[0] = 0
				pos[1] += 1
		else:
			row = 0
			while row <= 2:
				col = 2
				while col >= 0:
					tempPlaces.places[pos[0]][pos[1]].SetPlace(self.places[row][col].CheckPlace())
					col -= 1
					pos[0] += 1
				row += 1
				pos[0] = 0
				pos[1] += 1
		self.places = tempPlaces.places
	def PrintLine(self, line):
		assert ((line >= 0) and (line <= 2))
		for p in self.places[line]:
			p.Print()
	def CheckPlace(self, row, col):
		assert (((row >= 0) and (row <= 2)) and ((col >= 0) and (col <= 2)))
		return self.places[row][col].CheckPlace()
	def SetPlace(self, row, col, value):
		assert (((row >= 0) and (row <= 2)) and ((col >= 0) and (col <= 2)))
		self.places[row][col].SetPlace(value)

class Board:
	def __init__(self):
		self.quads = [[Quad(), Quad()], [Quad(), Quad()]]
	
	def Print(self):
		print "*   1   2   3  |  4   5   6"
		print ""
		row = 0
		while row <= 1:
			line = 0
			while line <= 2:
				L = (row * 3) + line + 1
				L = str(L)
				sys.stdout.write(L + "  ")
				self.quads[row][0].PrintLine(line)
				sys.stdout.write("| ")
				self.quads[row][1].PrintLine(line)
				sys.stdout.write("\n")
				if line != 6:
					print "               |"
				line += 1
			if row == 0:
				print "    -----------+-----------"
				print "               |"
			row += 1
	
	def CheckPlace(self, row, col):
		assert (((row >= 0) and (row <= 5)) and ((col >= 0) and (col <= 5)))
		return self.quads[row / 3][col / 3].CheckPlace(row % 3, col % 3)
	
	def SetPlace(self, row, col, value):
		assert (((row >= 0) and (row <= 5)) and ((col >= 0) and (col <= 5)))
		self.quads[row / 3][col / 3].SetPlace(row % 3, col % 3, value)
	
	def SetPlace2(self, qrow, qcol, row, col, value):
		assert (((qrow >= 0) and (qrow <= 2)) and ((qcol >= 0) and (qcol <= 2)))
		self.quads[qrow][qcol].SetPlace(row, col, value)
	
	def Rotate(self, quadrant, direction):
		direction -= 1
		assert ((quadrant >= 1) and (quadrant <= 4))
		assert ((direction == Quad.CW) or (direction == Quad.CCW))
		if quadrant == 1:
			self.quads[0][1].Rotate(direction)
		elif quadrant == 2:
			self.quads[0][0].Rotate(direction)
		elif quadrant == 3:
			self.quads[1][0].Rotate(direction)
		else:
			self.quads[1][1].Rotate(direction)
	
	def FindFive (self, row, col, direction, color, num):
		winner = 0
		isWon = []
		if (direction == 0):
			if DEBUG > 10: print "Beginning..."
			color = self.CheckPlace(0, 0)
			if DEBUG > 10: print "Color:", color
			num = 1
			# search horiz
			if DEBUG > 10: print "Start Horiz"
			isWon += self.FindFive(0, 1, 1, color, num)
			if DEBUG > 10: print "End Horiz"
			# search vert
			if DEBUG > 10: print "Start Vert"
			isWon += self.FindFive(1, 0, 2, color, num)
			if DEBUG > 10: print "End Vert"
		else:
			if DEBUG > 10: print "Continuing..."
			if DEBUG > 7: print "Row:", row, "\tCol", col, "\tColor:", self.CheckPlace(row, col)
			if self.CheckPlace(row, col) == color:
				num += 1
				if num == 5:
					winner = color
			else:
				color =  self.CheckPlace(row, col)
				num = 1
			if ((row == 0) or (col == 0)):
				# search horiz
				if col < 5:
					if DEBUG > 10: print "start horiz"
					if direction == 1:
						isWon += self.FindFive(row, col + 1, 1, color, num)
					else:
						isWon += self.FindFive(row, col + 1, 1, color, 1)
					if DEBUG > 10: print "end horiz"
				# search vert
				if row < 5:
					if DEBUG > 10: print "start vert"
					if direction == 2:
						isWon += self.FindFive(row + 1, col, 2, color, num)
					else:
						isWon += self.FindFive(row + 1, col, 2, color, 1)
					if DEBUG > 10: print "end vert"
			elif direction == 1:
				if col < 5:
					if DEBUG > 10: print "cont horiz"
					isWon += self.FindFive(row, col + 1, direction, color, num)
					if DEBUG > 10: print "stop horiz"
				else:
					pass
					if DEBUG > 10: print "end of horiz"
			else:
				if row < 5:
					if DEBUG > 10: print "cont vert"
					isWon += self.FindFive(row + 1, col, direction, color, num)
					if DEBUG > 10: print "stop vert"
				else:
					pass
					if DEBUG > 10: print "end of vert"
		if DEBUG > 5: print "Row:", row, "\tCol:", col, "\tNum:", num,"\tColor:", color
		if winner != 0:
			isWon.append(winner)
		return isWon
	
	def FindDiag(self, row, col, direction, color, num):
		isWon = []
		winner = 0
		if direction == 0:
			color = self.CheckPlace(0, 0)
			num = 1
			# Search criss...
			isWon += self.FindDiag(0, 0, 1, color, num)
			# Search cross...
			isWon += self.FindDiag(0, 5, 2, color, num)
		else:
			if self.CheckPlace(row, col) == color:
				num += 1
				if num == 5:
					winner = color
			else:
				color =  self.CheckPlace(row, col)
				num = 1
			if direction == 1:
				if (row < 5) and (col < 5):
					isWon += self.FindDiag(row + 1, col + 1, direction, color, num)
			else:
				if (row < 5) and (col > 0):
					isWon += self.FindDiag(row + 1, col - 1, direction, color, num)
			if (row == 0) and (col == 0):
				isWon += self.FindDiag(0, 1, direction, color, 0)
				isWon += self.FindDiag(1, 0, direction, color, 0)
			elif (row == 0) and (col == 5):
				isWon += self.FindDiag(0, 4, direction, color, 0)
				isWon += self.FindDiag(1, 5, direction, color, 0)
		if winner != 0:
			isWon.append(winner)
		return isWon
	
	def CheckForWinner(self):
		winners = []
		winners += self.FindFive(0, 0, 0, 0, 0)
		winners += self.FindDiag(0, 0, 0, 0, 0)
		if len(winners) > 0:
			if len(winners) == 1:
				return "Won"
			else:
				return "Possible Tie"
		else:
			return "Not Won"

testBoard = Board()

def PlayTest():
	gameBoard = Board()
	turn = 1
	#gameBoard.Print()
	keepPlaying = True
	while (keepPlaying):
		gameWon = ""
		if turn % 2 == 1:
			player = "White [W]"
		else:
			player = "Black [B]"
		print "Turn #" + str(turn) + "  Player: " + player
		turnDone = False
		while not turnDone:
			gameBoard.Print()
			playDone = False
			while not playDone:
				row = 0
				col = 0
				try:
					row = input("What row? (1-6): ")
					col = input("What column? (1-6): ")
				except:
					pass
				#if (row == 0) or (col == 0):
				#	sys.exit()
				if (row != 0) and (col != 0):
					if not (((row < 1) or (row > 6)) or ((col < 1) or (col > 6))):
						if gameBoard.CheckPlace(row - 1, col - 1) == Place.EMPTY:
							if (turn % 2) == 1:
								gameBoard.SetPlace(row - 1, col - 1, Place.WHITE)
							else:
								gameBoard.SetPlace(row - 1, col - 1, Place.BLACK)
							playDone = True
			rotateDone = False
			gameBoard.Print()
			gameWon = gameBoard.CheckForWinner()
			if gameWon != "Not Won":
				print gameWon
			else:
				while not rotateDone:
					quad = 0
					direction = 0
					try:
						quad = input("Which quadrant? (1-4): ")
						direction = input("Which direction? (CW:1 CCW:2): ")
					except:
						pass
					if (quad != 0) and (direction != 0):
						if (((quad >= 1) and (quad <= 4)) and ((direction >= 1) and (direction <= 2))):
							gameBoard.Rotate(quad, direction)
							rotateDone = True
				gameBoard.Print()
				gameWon = gameBoard.CheckForWinner()
				if gameWon != "Not Won":
					print gameWon 
			turnDone = True
		turn += 1
		#answer = raw_input("Continue game? (Y/n): ")
		#if (answer == 'n') or (answer == 'N'):
		#	keepPlaying = False
		if gameWon != "Not Won":
			keepPlaying = False

if __name__=="__main__":
	PlayTest()

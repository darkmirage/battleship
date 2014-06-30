#!/usr/bin/env python

import requests, json, numpy, random

XCOORD = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

HIT = 2
MISS = 1

SHIPS = {
	'carrier': 5,
	'battleship': 4,
	'submarine': 3,
	'destroyer': 3,
	'patrol': 2
}

class Battleship(object):

	SHOOT_URL = "https://student.people.co/api/challenge/battleship/%s/boards/%s/"

	def __init__(self, user_id, board_name):
		self.board = numpy.zeros((10, 10), dtype=numpy.int)
		self.ended = False
		self.ships = [5, 4, 3, 3, 2]
		self.shots = 0
		self.url = Battleship.SHOOT_URL % (user_id, board_name)

	def is_shot(self, x, y):
		if (self.board[x][y] > 0):
			return True

	@staticmethod
	def to_coord(x, y):
		return str(XCOORD[x]) + str(y + 1)

	@staticmethod
	def from_coord(coord):
		y = int(coord[1])
		x = XCOORD.index(coord[0])

	def parse_result(self, result):
		if result['is_finished']:
			self.ended = True
		if result['sunk'] in SHIPS.keys():
			self.ships.remove(SHIPS[result['sunk']])

	def post_shoot(self, coord):
		url = self.url + coord
		r = requests.post(url)
		result = r.json()
		self.parse_result(result)
		return result

	def shoot(self, x, y):
		if x < 0 or y < 0 or x >= 10 or y >= 10:
			return False
		if (self.is_shot(x, y)):
			return False

		self.shots += 1

		coord = self.to_coord(x, y)
		print "Shooting %s" % coord

		result = self.post_shoot(coord)

		if (result['is_hit']):
			self.board[x][y] = HIT
		else:
			self.board[x][y] = MISS

		return result['is_hit']

	def check(self, x, y):
		if x < 0 or y < 0 or x >= 10 or y >= 10:
			return False
		return self.board[x][y] == HIT

	def check_nearby(self, x, y):
		count = 0
		x0 = x+1
		y0 = y
		if (self.check(x0, y0)):
			count += 1
		x0 = x
		y0 = y+1
		if (self.check(x0, y0)):
			count += 1
		x0 = x-1
		y0 = y
		if (self.check(x0, y0)):
			count += 1
		x0 = x
		y0 = y-1
		if (self.check(x0, y0)):
			count += 1
		return count

battleship = Battleship('4d09222d3729', 'live_board_1')

while not battleship.ended:
	x = random.randint(0, 9)
	y = random.randint(0, 9)
	p = random.random()
	n = battleship.check_nearby(x, y)

	if n > 0:
		p += n / 10.0

	if p > 0.9:
		print (x, y, p, n)
		hit = battleship.shoot(x, y)
		if hit:
			battleship.shoot(x-1, y)
			battleship.shoot(x+1, y)
			battleship.shoot(x, y-1)
			battleship.shoot(x, y+1)




print "Won in %i shots" % battleship.shots



# print battleship.board
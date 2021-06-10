from time import process_time
from config import *
from rrt import rrt
import drawing
import events
from time import sleep
import pygame as pg
pg.init()

def main():

	drawing.screen = pg.display.set_mode((WIDTH, HEIGHT))
	gameState = 'waiting'

	while True:
		event = pg.event.poll()
		mousePos = pg.mouse.get_pos()
		gameState = events.mainHandler(event, gameState, mousePos)

		if gameState == 'quit':
			print(gameState)
			return
		elif gameState == 'start-positioning':
			drawing.startPos = mousePos
		elif gameState == 'goal-positioning':
			drawing.goalPos = mousePos
		elif gameState == 'drawing':
			drawing.drawObstacle(mousePos)
		elif gameState == 'erasing':
			drawing.eraseObstacle(mousePos)
		elif gameState == 'clear':
			drawing.clearObstacles()
		elif gameState == 'save':
			drawing.saveObstacles()
		elif gameState == 'load':
			drawing.loadObstacles()
		elif gameState == 'rrt':
			print(gameState)
			drawing.recorder = True
			drawing.clearEdgesPool()
			tree = rrt(drawing.startPos, drawing.goalPos, drawing.obstaclesSurface)
			if tree:  # A path was found:
				drawing.drawPath(tree)
				gameState = 'path-found'
			else:  # User terminated the algorithm's execution:
				drawing.recorder = False
				gameState = 'waiting'		
		
		elif drawing.run_algo:
			drawing.recorder = True
			drawing.clearEdgesPool()
			tree = rrt(drawing.startPos, drawing.goalPos, drawing.obstaclesSurface)
			if tree:  # A path was found:
				drawing.drawPath(tree)
			drawing.run_algo = False
			drawing.update()
			sleep(1)			
			return

		# drawing.update()

if __name__ == '__main__':
	main()

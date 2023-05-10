import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW = 6
COLUMN = 7

def create_board():
	board = np.zeros((ROW,COLUMN))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW):
		if board[r][col] == 0:
			return r
	return False

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN-3):
		for r in range(ROW):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN):
		for r in range(ROW-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diagonals
	for c in range(COLUMN-3):
		for r in range(ROW-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diagonals
	for c in range(COLUMN-3):
		for r in range(3, ROW):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN):
		for r in range(ROW):
			pygame.draw.rect(screen, BLUE, (c*boardsize, r*boardsize+boardsize, boardsize, boardsize))
			pygame.draw.circle(screen, BLACK, (int(c*boardsize+boardsize/2), int(r*boardsize+boardsize+boardsize/2)), RADIUS)
	
	for c in range(COLUMN):
		for r in range(ROW):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*boardsize+boardsize/2), height-int(r*boardsize+boardsize/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*boardsize+boardsize/2), height-int(r*boardsize+boardsize/2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

boardsize = 100

width = COLUMN * boardsize
height = (ROW+1) * boardsize

size = (width, height)

RADIUS = int(boardsize/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:	
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, boardsize))
			posx = event.pos[0]
			color = RED if turn == 0 else YELLOW
			pygame.draw.circle(screen, color, (posx, int(boardsize/2)), RADIUS)
			pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, boardsize))
			posx = event.pos[0]
			col = int(math.floor(posx/boardsize))

			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				if turn == 0:
					player = 1
				else:
					player = 2
				drop_piece(board, row, col, player)

				if winning_move(board, player):
					label = myfont.render(f"PLAYER {player} WINS!", 1, RED if player == 1 else YELLOW)
					screen.blit(label, (40,10))
					game_over = True
				
				#check for if no one wins
				
					if not get_next_open_row(board, 1):
						label = myfont.render(f"DRAW!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

				print_board(board)
				draw_board(board)

				turn = (turn + 1) % 2

			if game_over:
				pygame.time.wait(3000)

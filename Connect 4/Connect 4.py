import numpy as Row_Column
import pygame
import pygame.mixer
import sys
import math
import random

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
CHAMPAGNE = (247,231,206)
ROW_COUNT = 6
COLUMN_COUNT = 7
Empty = 0
Player = 0
AI = 1
ConnectionLength = 4
Player_Checker = 1
AI_Checker = 2
pygame.init()
Font = pygame.font.SysFont("monospace", 75)
ButtonFont = pygame.font.SysFont("freesansbold.ttf", 30)
CopyRightsFont = pygame.font.SysFont("freesansbold.ttf", 20)
Background = pygame.image.load("Images/Connect_4.jpg")
MainMenuSound = pygame.mixer.Sound("Sounds/Main.wav")
CheckerSound = pygame.mixer.Sound("Sounds/Checker.wav")
WinSound = pygame.mixer.Sound("Sounds/Win.wav")
LoseSound = pygame.mixer.Sound("Sounds/Lose.wav")
TieSound = pygame.mixer.Sound("Sounds/Tie.wav")
pygame.display.set_caption("Connect 4")
Icon = pygame.image.load("Images/Connect 4 Logo.png")
pygame.display.set_icon(Icon)
Turn = random.randint(0, 1)
SquareSize = 100
Width = COLUMN_COUNT * SquareSize
Height = (ROW_COUNT + 1) * SquareSize
Size = (Width, Height)
Radius = int(SquareSize/2 - 5)
Diffculty = 1
VS_Player = False
VS_AI = False
Game = True
Main_Menu = True
Game_Over = True
IsBackgroudClear = False
Click = pygame.mouse.get_pressed()

def Create_Board():
	Board = Row_Column.zeros((ROW_COUNT, COLUMN_COUNT))
	return Board
	
def Insert_Checker_Column(Board, Row, Column, Checker):
	Board[Row][Column] = Checker

def Location_Available(Board, Column):
	return Board[ROW_COUNT-1][Column] == 0

def Insert_Checker_Row(Board, Column):
	for r in range(ROW_COUNT):
		if Board[r][Column] == 0:
			return r
			
def Print_Board(Board):
	print(Row_Column.flip(Board, 0))
	
def Win_Move(Board, Checker):
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if Board[r][c] == Checker and Board[r][c+1] == Checker and Board[r][c+2] == Checker and Board[r][c+3] == Checker:
				return True
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if Board[r][c] == Checker and Board[r+1][c] == Checker and Board[r+2][c] == Checker and Board[r+3][c] == Checker:
				return True
	
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if Board[r][c] == Checker and Board[r+1][c+1] == Checker and Board[r+2][c+2] == Checker and Board[r+3][c+3] == Checker:
				return True
	
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if Board[r][c] == Checker and Board[r-1][c+1] == Checker and Board[r-2][c+2] == Checker and Board[r-3][c+3] == Checker:
				return True
				
def Draw_Board(Board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SquareSize, r*SquareSize+SquareSize, SquareSize, SquareSize))
			pygame.draw.circle(screen, BLACK, (int(c*SquareSize+SquareSize/2), int(r*SquareSize+SquareSize+SquareSize/2)), Radius)    
			pygame.draw.circle(screen, WHITE, (int(c*SquareSize+SquareSize/2), int(r*SquareSize+SquareSize+SquareSize/2)), 42)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT): 
			if Board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SquareSize+SquareSize/2), Height-int(r*SquareSize+SquareSize/2)), 42)    
			
			elif Board[r][c] == 2:
				pygame.draw.circle(screen, YELLOW, (int(c*SquareSize+SquareSize/2), Height-int(r*SquareSize+SquareSize/2)), 42)
		
def Evaluate_Connection(Connection, Checker):
	Score = 0
	Opponent_Checker = Player_Checker

	if Diffculty == 1:
		if Checker == Player_Checker:
			Opponent_Checker = AI_Checker
	
		if Connection.count(Checker) == 4:
			Score += 100

		elif Connection.count(Checker) == 3 and Connection.count(Empty) == 1:
			Score += 5

		elif Connection.count(Checker) == 2 and Connection.count(Empty) == 2:
			Score += 2

		if Connection.count(Opponent_Checker) == 3 and Connection.count(Empty) == 1:
			Score -= 4

	return Score

def Board_AI(Board, Checker):
	Score = 0
	Center_Array = [int(i) for i in list(Board[:, COLUMN_COUNT//2])]
	Center_Count = Center_Array.count(Checker)
	Score += Center_Count * 3

	for r in range(ROW_COUNT):
		Row_Array = [int(i) for i in list(Board[r,:])]
		for c in range(COLUMN_COUNT-3):
			Connection = Row_Array[c:c+ConnectionLength]
			Score += Evaluate_Connection(Connection, Checker)

	for c in range(COLUMN_COUNT):
		Column_Array = [int(i) for i in list(Board[:, c])]
		for r in range(ROW_COUNT-3):
			Connection = Column_Array[r:r+ConnectionLength]
			Score += Evaluate_Connection(Connection, Checker)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			Connection = [Board[r+i][c+i] for i in range(ConnectionLength)]
			Score += Evaluate_Connection(Connection, Checker)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			Connection = [Board[r+3-i][c+i] for i in range(ConnectionLength)]
			Score += Evaluate_Connection(Connection, Checker)

	return Score

def If_Terminal_Node(Board):
	return Win_Move(Board, Player_Checker) or Win_Move(Board, AI_Checker) or len(Get_Valid_Locations(Board)) == 0

def Minimax(Board, Depth, Alpha, Beta, MaxPlayer):
	Valid_Locations = Get_Valid_Locations(Board)
	If_Terminal = If_Terminal_Node(Board)
	
	if Depth == 0 or If_Terminal:
		if If_Terminal:
			if Win_Move(Board, AI_Checker):
				return (None, 10000000000)

			elif Win_Move(Board, Player_Checker):
				return (None, -100000000000)
		
			else:
				return (None, 0)

		else:
			return (None, Board_AI(Board, AI_Checker))
	
	if MaxPlayer:
		Value = -math.inf
		Col = random.choice(Valid_Locations)

		for Column in Valid_Locations:
			Row = Insert_Checker_Row(Board, Column)
			Board_Copy = Board.copy()
			Insert_Checker_Column(Board_Copy , Row, Column, AI_Checker)
			New_Score = Minimax(Board_Copy, Depth-1, Alpha, Beta, False)[1]
			if New_Score > Value:
				Value = New_Score
				Col = Column

			Alpha = max(Alpha, Value)

			if Alpha >= Beta:
				break
			
		return Col, Value

	else:
		Value = math.inf
		Col = random.choice(Valid_Locations)

		for Column in Valid_Locations:
			Row = Insert_Checker_Row(Board, Column)
			Board_Copy = Board.copy()
			Insert_Checker_Column(Board_Copy , Row, Column, Player_Checker)
			New_Score = Minimax(Board_Copy, Depth-1, Alpha, Beta, True)[1]
			if New_Score < Value:
				Value = New_Score
				Col = Column

			Beta = min(Beta, Value)

			if Alpha >= Beta:
				break

		return Col, Value            

def Get_Valid_Locations(Board):
	Valid_Locations = []

	for Column in range(COLUMN_COUNT):
		if Location_Available(Board, Column):
			Valid_Locations.append(Column)
	return Valid_Locations

def AI_Move(Board, Checker):
	Valid_Locations = Get_Valid_Locations(Board)
	BestScore = -10000
	BestColumn = random.choice(Valid_Locations)

	for Column in Valid_Locations:
		Row = Insert_Checker_Row(Board, Column)
		TempBoard = Board.copy()
		Insert_Checker_Column(TempBoard, Row, Column, Checker)
		Score = Board_AI(TempBoard, Checker)

		if Score > BestScore:
			BestScore = Score
			BestColumn = Column

	return BestColumn

Board = Create_Board()
Print_Board(Board)
screen = pygame.display.set_mode(Size)
pygame.display.update()

while Game:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	while Main_Menu:

		screen.blit(Background, (0,0))
		MainMenuSound.play()
		Mouse = pygame.mouse.get_pos()

		if 25 + 135 > Mouse[0] > 25 and 150 + 50 > Mouse[1] > 150:
			pygame.draw.rect(screen, CHAMPAGNE, (25, 150 , 135, 50))
		else:
			pygame.draw.rect(screen, WHITE, (25, 150 , 135, 50))

		SinglePlayerText = ButtonFont.render("SinglePlayer", True, BLACK)
		screen.blit(SinglePlayerText, (30, 168))

		if 25 + 135 > Mouse[0] > 25 and 250 + 50 > Mouse[1] > 250:
			pygame.draw.rect(screen, CHAMPAGNE, (25, 250 , 135, 50))
		else:
			pygame.draw.rect(screen, WHITE, (25, 250 , 135, 50))

		MultiPlayerText = ButtonFont.render("MultiPlayer", True, BLACK)
		screen.blit(MultiPlayerText, (35, 268))

		if 25 + 135 > Mouse[0] > 25 and 550 + 50 > Mouse[1] > 550:
			pygame.draw.rect(screen, CHAMPAGNE, (25, 550 , 135, 50))
		else:
			pygame.draw.rect(screen, WHITE, (25, 550 , 135, 50))

		QuitText = ButtonFont.render("QUIT", True, BLACK)
		screen.blit(QuitText, (int(135/2), 568))

		CopyRights = CopyRightsFont.render("© All Rights Reserved", True, BLACK)
		screen.blit(CopyRights, (250, 680))

		if 550 + 135 > Mouse[0] > 550 and 150 + 50 > Mouse[1] > 150 and pygame.mouse.get_pressed()[0]:
			Diffculty = 1

		elif 550 + 135 > Mouse[0] > 550 and 250 + 50 > Mouse[1] > 250 and pygame.mouse.get_pressed()[0]:
			Diffculty = 2

		elif 550 + 135 > Mouse[0] > 550 and 350 + 50 > Mouse[1] > 350 and pygame.mouse.get_pressed()[0]:
			Diffculty = 3

		if Diffculty == 1:
			pygame.draw.rect(screen, CHAMPAGNE, (550, 150 , 135, 50))
			pygame.draw.rect(screen, WHITE, (550, 250 , 135, 50))
			pygame.draw.rect(screen, WHITE, (550, 350 , 135, 50))

		elif Diffculty == 2:
			pygame.draw.rect(screen, WHITE, (550, 150 , 135, 50))
			pygame.draw.rect(screen, CHAMPAGNE, (550, 250 , 135, 50))
			pygame.draw.rect(screen, WHITE, (550, 350 , 135, 50))

		elif Diffculty == 3:
			pygame.draw.rect(screen, WHITE, (550, 150 , 135, 50))
			pygame.draw.rect(screen, WHITE, (550, 250 , 135, 50))
			pygame.draw.rect(screen, CHAMPAGNE, (550, 350 , 135, 50))

		Easy = ButtonFont.render("Easy", True, BLACK)
		screen.blit(Easy, (592, 166))
		
		Medium = ButtonFont.render("Medium", True, BLACK)
		screen.blit(Medium, (578, 266))
		
		Hard = ButtonFont.render("Hard", True, BLACK)
		screen.blit(Hard, (592, 366))

		DiffcultyText = ButtonFont.render("Diffculty", True, BLACK)
		screen.blit(DiffcultyText, (570, 100))
		pygame.display.flip()

		if 25 + 135 > Mouse[0] > 25 and 150 + 50 > Mouse[1] > 150 and pygame.mouse.get_pressed()[0]:
			Main_Menu = False
			VS_AI = True
			Game_Over = False
			MainMenuSound.stop()

		if 25 + 135 > Mouse[0] > 25 and 250 + 50 > Mouse[1] > 250 and pygame.mouse.get_pressed()[0]:
			pygame.draw.rect(screen, WHITE, (25, 600, 135,50))
			Main_Menu = False
			VS_Player = True
			Game_Over = False
			MainMenuSound.stop()

		if 25 + 135 > Mouse[0] > 25 and 550 + 50 > Mouse[1] > 550 and pygame.mouse.get_pressed()[0]:
			sys.exit()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

	while VS_Player and not Game_Over:
		if(IsBackgroudClear == False):
			screen.fill((0,0,0))

		Draw_Board(Board)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK, (0, 0, Width, SquareSize))
				X = event.pos[0]

				if Turn == 0:
					pygame.draw.circle(screen, RED, (X, int(SquareSize/2)), Radius)
				else:
					pygame.draw.circle(screen, YELLOW, (X, int(SquareSize/2)), Radius)
					
			pygame.display.update()
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0, 0, Width, SquareSize))
				print(event.pos)

				if Turn == 0:
					X = event.pos[0]
					Column = int(math.floor(X/SquareSize))
					
					if Location_Available(Board, Column):
						Row = Insert_Checker_Row(Board, Column)
						Insert_Checker_Column(Board, Row, Column, 1)
						CheckerSound.play()
						Turn = Turn + 1
						Turn = Turn % 2
						
						if Win_Move(Board, 1):
							Label = Font.render("Player 1 Win", 1, RED)
							WinSound.play()
							screen.blit(Label, (90, 10))
							Game_Over = True
					
					if (Row_Column.all(Board) == True and (not Win_Move(Board, 1) or not Win_Move(Board, 2))):
						Label = Font.render("Draw", 1, WHITE)
						TieSound.play()
						screen.blit(Label, (250, 10))
						Game_Over = True

				else:
					X = event.pos[0]
					Column = int(math.floor(X/SquareSize))
					
					if Location_Available(Board, Column):
						Row = Insert_Checker_Row(Board, Column)
						Insert_Checker_Column(Board, Row, Column, 2)
						CheckerSound.play()
						Turn = Turn + 1
						Turn = Turn % 2
				
						if Win_Move(Board, 2):
							Label = Font.render("Player 2 Win", 2, YELLOW)
							WinSound.play()
							screen.blit(Label, (90, 10))
							Game_Over = True
							
					if (Row_Column.all(Board) == True and (not Win_Move(Board, 1) or not Win_Move(Board, 2))):
						Label = Font.render("Draw", 2, WHITE)
						TieSound.play()
						screen.blit(Label, (250, 10))
						Game_Over = True

				Print_Board(Board)
				Draw_Board(Board)
				pygame.display.update()

				if Game_Over:
					pygame.time.wait(4000)
					Main_Menu = True
					VS_Player = False
					Board = Row_Column.zeros((ROW_COUNT, COLUMN_COUNT))

	while VS_AI and not Game_Over:
		if(IsBackgroudClear == False):
			screen.fill((0,0,0))

		Draw_Board(Board)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK, (0, 0, Width, SquareSize))
				X = event.pos[0]

				if Turn == Player:
					pygame.draw.circle(screen, RED, (X, int(SquareSize/2)), Radius)
					
			pygame.display.update()
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0, 0, Width, SquareSize))
				print(event.pos)

				if Turn == Player:
					X = event.pos[0]
					Column = int(math.floor(X/SquareSize))
					
					if Location_Available(Board, Column):
						Row = Insert_Checker_Row(Board, Column)
						Insert_Checker_Column(Board, Row, Column, Player_Checker)
						CheckerSound.play()
						Turn = Turn + 1
						Turn = Turn % 2
						
						if Win_Move(Board, Player_Checker):
							WinSound.play()
							Label = Font.render("You Win", 1, RED)
							screen.blit(Label, (190, 10))
							Game_Over = True
							VS_Player =  False

					if (Row_Column.all(Board) == True and (not Win_Move(Board, 1) or not Win_Move(Board, 2))):
						Label = Font.render("Draw", 1, WHITE)
						TieSound.play()
						screen.blit(Label, (250, 10))
						Game_Over = True

					Print_Board(Board)
					Draw_Board(Board)
					pygame.display.update()

		if Turn == AI and not Game_Over:

			if Diffculty == 1:
				Column, Minimax_Score = Minimax(Board, 1, - math.inf, math.inf, True)

			elif Diffculty == 2:
				Column, Minimax_Score = Minimax(Board, 2, - math.inf, math.inf, True)

			elif Diffculty == 3:
				Column, Minimax_Score = Minimax(Board, 4, - math.inf, math.inf, True)

			if Location_Available(Board, Column):
				pygame.time.wait(300)
				Row = Insert_Checker_Row(Board, Column)
				Insert_Checker_Column(Board, Row, Column, AI_Checker)
				CheckerSound.play()
				Turn = Turn + 1
				Turn = Turn % 2

				if Win_Move(Board, AI_Checker):
					LoseSound.play()
					Label = Font.render("You Lose", 2, YELLOW)
					screen.blit(Label, (190, 10))
					Game_Over = True
					VS_AI = False

			if (Row_Column.all(Board) == True and (not Win_Move(Board, 1) or not Win_Move(Board, 2))):
				Label = Font.render("Draw", 2, WHITE)
				TieSound.play()
				screen.blit(Label, (250, 10))
				Game_Over = True

			Print_Board(Board)
			Draw_Board(Board)
			pygame.display.update()

		if Game_Over:
			pygame.time.wait(4000)
			Main_Menu = True
			VS_AI = False
			Board = Row_Column.zeros((ROW_COUNT, COLUMN_COUNT))
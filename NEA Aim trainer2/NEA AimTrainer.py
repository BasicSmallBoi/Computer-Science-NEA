#Importing Libraries
import pygame
import time
import random

#Initilising Pygame
pygame.init()

#Global Variables
#Screen
screen = pygame.display.set_mode((1400,800)) #Defining the screen that will display GUI
screen_caption = pygame.display.set_caption("Games")

#Text/Fonts
font = pygame.font.Font('graphics/Talking.otf', 50)

#Time
clock = pygame.time.Clock()

#Buttons
button_img = pygame.image.load('graphics/button.png').convert_alpha()
target_img = pygame.image.load('graphics/Target1.png').convert_alpha()
bullseye_img = pygame.image.load('graphics/bullseye.png').convert_alpha()

#Sounds
click_sfx = pygame.mixer.Sound('graphics/click1.mp3') #Audio file asignment 
penalty_sfx = pygame.mixer.Sound('graphics/wrong.wav') #Audio file asignment 
correct_sfx = pygame.mixer.Sound('graphics/correct.mp3') #Audio file asignment

#Creating a button class

def data(game, score, operation):
	file = open("data.txt", "r" )
	data = file.readline()
	data = data.split(" ")

	if '' in data:
		data.remove('')

	data_len = len(data)

	if game == "Aim_Trainer":
		game = 0
	elif game == "Game2":
		game = 1
	elif game == "Game3":
		game = 2
	elif game == "Game4":
		game = 3
	else:
		file.close()

	highscore = (data[game])

	if score != 0:
		if operation == "Lower":
			if float(score) < float(data[game]):
				highscore = score
				data[game] = highscore
		if operation == "Higher":
			if float(score) > float(data[game]):
				highscore = score
				data[game] = highscore

	file.close()

	file = open("data.txt", "w")
	for i in range(data_len):
		file.write(str(data[i]) + " ")

	file.close()

	return highscore


class Button():
	def __init__(self, x, y, image, scale): #Assigning the image to the button and giving it coordinates
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect() 
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self): #Draw button on screen

		action = False
		pos = pygame.mouse.get_pos() #Get mouse position

		if self.rect.collidepoint(pos): #Check to see if the mouse is over the button
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
					
		screen.blit(self.image, (self.rect.x, self.rect.y))
		return action

class Target():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.mask = pygame.mask.from_surface(image)
		self.clicked = False

	def draw(self):

		action = False
		pos = pygame.mouse.get_pos()

		mouse = pygame.Surface((1,1))
		mouse_mask = pygame.mask.from_surface(mouse)

		if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
			if self.mask.overlap(mouse_mask, (pos[0] - self.rect.x, pos[1] - self.rect.y)):
				self.clicked = True
				self.rect.x = random.randint(150, 1250)
				self.rect.y = random.randint(150,650)
				correct_sfx.play()
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		screen.blit(self.image, (self.rect.x, self.rect.y))
		return action

#Creating button instances
game1_button = Button(200, 100, button_img, 1)
game2_button = Button(200, 300, button_img, 1)
game3_button = Button(200, 500, button_img, 1)
game4_button = Button(200, 700, button_img, 1)
menu_button = Button(1300, 50, button_img, 0.4)
scores_button = Button(1300, 750, button_img, 0.4)
replay_button = Button(700, 400, button_img, 1)

#Creating a text drawing function
def draw_text(text, font, colour, surface, x, y):
	textobj = font.render(text, 1, colour)
	textrect = textobj.get_rect()
	textrect.center = (x, y)
	surface.blit(textobj, textrect)

def Score(ST):
	TT = int(pygame.time.get_ticks() - ST) #Calculates the time the game took until completion.
	score = float(TT / 1000)
	#if score < ATHS:
		#HS = SC
	return score

#Creating Menu Function State
def Main_Menu():

	while True:

		screen.fill((23, 43, 111))
		draw_text("Main Menu!", font, (32, 200, 2), screen, 700, 200)

		if game1_button.draw():
			Aim_Trainer()

		draw_text("Aim Trainer", font, (255, 255, 255), screen, 200 , 100)

		if game2_button.draw():
			Game2()
		draw_text("Morgan", font, (255, 255, 255), screen, 200 , 300)

		if game3_button.draw():
			Game3()
		draw_text("Game 3", font, (255, 255, 255), screen, 200 , 500)

		if game4_button.draw():
			Game4()
		draw_text("Game 4", font, (255, 255, 255), screen, 200 , 700)

		if scores_button.draw():
			Scores()
		draw_text("Scores", font, (255, 255, 255), screen, 1300 , 750)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		pygame.display.update()
		clock.tick(60)


def Aim_Trainer():
	AT_running = True
	main_game_loop = False

	mouse = pygame.Surface((1,1))
	mouse_mask = pygame.mask.from_surface(mouse)

	count = 0
	i = 0

	target = Target(random.randint(100, 1300), random.randint(100, 700), target_img, 1)
	bullseye = Target(random.randint(100, 1300), random.randint(100, 700), bullseye_img, 1)
	start_time = int(pygame.time.get_ticks())

	while AT_running:

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		mouse_pos = pygame.mouse.get_pos()

		if main_game_loop:
			screen.fill((53, 74, 90))
			draw_text("Aim Trainer", font, (32, 200, 2), screen, 700, 200)

			if target.draw():
				count = count + 1
				print(count)

			if bullseye.draw():
				count = count + 1.2
				print(count)

			if count >= 50:
				main_game_loop = False

			menu_button = Button(1300, 50, button_img, 0.4)

			if menu_button.draw():
				Main_Menu()
			draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

		else:
			screen.fill((160, 254, 136))

			if i < 1:
				ATscore = 0
				ATscore = Score(start_time)
				data("Aim_Trainer", ATscore, "Lower")
				i += 1
			
			draw_text(str(ATscore), font, (32, 200, 2), screen, 700, 200)

			menu_button = Button(1300, 50, button_img, 0.4)

			if menu_button.draw():
				Main_Menu()
			if replay_button.draw():
				count = 0
				i = 0
				start_time = int(pygame.time.get_ticks())
				main_game_loop = True
			draw_text("Replay", font, (255, 255, 255), screen, 700, 400)

			draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

		pygame.display.update()
		clock.tick(60)


def Game2():
	game2_running = True
	while game2_running:
		screen.fill((53, 74, 90))
		draw_text("Game2!", font, (32, 200, 2), screen, 700, 200)

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		menu_button = Button(1300, 50, button_img, 0.4)
		if menu_button.draw():
			Main_Menu()
		draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

		pygame.display.update()
		clock.tick(60)


def Game3():
	game3_running = True
	while game3_running:
		screen.fill((53, 74, 90))
		draw_text("Game3!", font, (32, 200, 2), screen, 700, 200)

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		menu_button = Button(1300, 50, button_img, 0.4)
		if menu_button.draw():
			Main_Menu()
		draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

		pygame.display.update()
		clock.tick(60)


def Game4():
	game4_running = True
	while game4_running:
		screen.fill((53, 74, 90))
		draw_text("Game4!", font, (32, 200, 2), screen, 700, 200)

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		menu_button = Button(1300, 50, button_img, 0.4)
		if menu_button.draw():
			Main_Menu()
		draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

		pygame.display.update()
		clock.tick(60)


def Scores():
	i = 0

	option_running = True
	while option_running:

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		screen.fill((190, 200, 10))
		draw_text("JACSEN!", font, (32, 200, 2), screen, 700, 200)

		AThighscore = data("Aim_Trainer", 0, "Lower")
		Game2highscore = data("Game2", 0, "Lower")
		Game3highscore = data("Game3", 0, "Lower")
		Game4highscore = data("Game4", 0, "Lower")

		if AThighscore == "0":
			AThighscore = "N/A"
		if Game2highscore == "0":
			Game2highscore = "N/A"
		if Game3highscore == "0":
			Game3highscore = "N/A"
		if Game4highscore == "0":
			Game4highscore = "N/A"

		draw_text((AThighscore), font, (32, 200, 2), screen, 300, 400)
		draw_text((Game2highscore), font, (32, 200, 2), screen, 300, 500)
		draw_text((Game3highscore), font, (32, 200, 2), screen, 300, 600)
		draw_text((Game4highscore), font, (32, 200, 2), screen, 300, 700)

		if menu_button.draw():
			Main_Menu()
		draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

		pygame.display.update()
		clock.tick(60)


Main_Menu()

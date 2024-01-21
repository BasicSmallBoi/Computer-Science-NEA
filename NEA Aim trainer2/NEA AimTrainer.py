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

square_png = pygame.image.load('graphics/square.png').convert_alpha()

#Sounds
click_sfx = pygame.mixer.Sound('graphics/click1.mp3') #Audio file asignment 
penalty_sfx = pygame.mixer.Sound('graphics/wrong.wav') #Audio file asignment 
correct_sfx = pygame.mixer.Sound('graphics/correct.mp3') #Audio file asignment

#Background
background_surf = pygame.image.load('graphics/Background.png').convert_alpha() #Loading a background image
background_rect = background_surf.get_rect(topleft = (0,0))

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
	elif game == "Reaction_Time":
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
game1_button = Button(500, 120, button_img, 1)
game2_button = Button(220, 300, button_img, 1)
game3_button = Button(220, 500, button_img, 1)
game4_button = Button(500, 680, button_img, 1)
game5_button = Button(900, 680, button_img, 1)
menu_button = Button(1300, 50, button_img, 0.4)
scores_button = Button(1270, 710, button_img, 0.4)
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
	score = round(score, 2)
	return score

#Creating Menu Function State
def Main_Menu():

	while True:

		screen.blit(background_surf, background_rect)
		draw_text("Main Menu!", font, (255, 255, 255), screen, 700, 400)

		if game1_button.draw():
			Aim_Trainer()

		draw_text("Aim Trainer", font, (255, 255, 255), screen, 500 , 120)

		if game2_button.draw():
			Game2()
		draw_text("Morgan", font, (255, 255, 255), screen, 220 , 300)

		if game3_button.draw():
			Game3()
		draw_text("Game 3", font, (255, 255, 255), screen, 220 , 500)

		if game4_button.draw():
			ReactionTime()
		draw_text("Reaction Time", font, (255, 255, 255), screen, 500 , 680)

		if game5_button.draw():
			Game5()
		draw_text("Game5", font, (255, 255, 255), screen, 900, 680)

		if scores_button.draw():
			Scores()
		draw_text("Scores", font, (255, 255, 255), screen, 1270, 710)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		pygame.display.update()
		clock.tick(60)


def Aim_Trainer():
	AT_running = True
	main_game_loop = True

	game1background_surf = pygame.image.load('graphics/game1background.png').convert_alpha() #Loading a background image
	game1background_rect = background_surf.get_rect(topleft = (0,0))

	ATscore = round(0, 1)

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
			screen.blit(game1background_surf, game1background_rect)
			draw_text("Aim Trainer", font, (255, 255, 255), screen, 700, 200)

			if target.draw():
				count = count + 1
				print(count)

			if bullseye.draw():
				count = count + 1.2
				print(count)

			if count >= 50:
				main_game_loop = False

			menu_button = Button(1270, 90, button_img, 0.4)

			if menu_button.draw():
				Main_Menu()
			draw_text("Menu", font, (255, 255, 255), screen, 1270, 90)

		else:
			screen.blit(game1background_surf, game1background_rect)

			if i < 1:
				ATscore = round(0, 1)
				ATscore = round(Score(start_time), 3)
				data("Aim_Trainer", ATscore, "Lower")
				i += 1
			
			draw_text(str(ATscore), font, (255, 255, 255), screen, 700, 200)

			menu_button = Button(1270, 90, button_img, 0.4)

			if menu_button.draw():
				Main_Menu()
			if replay_button.draw():
				count = 0
				i = 0
				start_time = int(pygame.time.get_ticks())
				main_game_loop = True
			draw_text("Replay", font, (255, 255, 255), screen, 700, 400)

			draw_text("Menu", font, (255, 255, 255), screen, 1270, 90)

		pygame.display.update()
		clock.tick(60)


def Game2():
	game2_running = True
	game2background_surf = pygame.image.load('graphics/game2background.png').convert_alpha() #Loading a background image
	game2background_rect = background_surf.get_rect(topleft = (0,0))
	while game2_running:
		screen.blit(game2background_surf, game2background_rect)
		draw_text("Game2!", font, (255, 255, 255), screen, 700, 200)

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		menu_button = Button(1270, 80, button_img, 0.4)
		if menu_button.draw():
			Main_Menu()
		draw_text("Menu", font, (255, 255, 255), screen, 1270, 80)

		pygame.display.update()
		clock.tick(60)


def Game3():
	game3_running = True
	while game3_running:
		screen.fill((53, 74, 90))
		draw_text("Game3!", font, (255, 255, 255), screen, 700, 200)

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


def ReactionTime():
	RT_running = True
	main_game_loop = True
	reaction_test = True
	start_time = int(pygame.time.get_ticks())
	change_time = start_time + (random.randint(2000,5000))
	i = 0
	x = 0
	repeats = 0
	scores = []
	penalty = 0
	clicked = True

	while RT_running:
		if main_game_loop:
			if reaction_test:
				screen.fill((200, 20, 20))
				draw_text("CLICK WHEN BACKGROUND CHANGES FROM RED TO GREEN...", font, (255, 255, 255), screen, 700, 200)

				new_time = int(pygame.time.get_ticks())
				if change_time <= new_time:
					print ("bababooby")
					reaction_test = False


				if clicked == False and pygame.mouse.get_pressed()[0] == 1:
					penalty += 25
					clicked = True
					print("Penalty")

				if pygame.mouse.get_pressed()[0] == 0:
					clicked = False

			else:
				clicked = False

				screen.fill((20, 200, 20))
				draw_text("CLICK!", font, (255, 255, 255), screen, 700, 200)
				if i != 1:
					time_delay = int(pygame.time.get_ticks())
					i += 1

				if pygame.mouse.get_pressed()[0] == 1:
					clicked = True
					time_clicked = int(pygame.time.get_ticks())
					score = time_clicked - time_delay 
					scores.append(score)
					print (scores)

					start_time = int(pygame.time.get_ticks())
					change_time = start_time + (random.randint(2000,10000))
					repeats += 1
					i = 0

					if repeats < 5: 
						reaction_test = True

					else:
						main_game_loop = False

				if pygame.mouse.get_pressed()[0] == 0:
					clicked = False

		else:
			i = 0
			x = 0
			screen.fill((44, 44, 200))

			A = scores[0]
			B = scores[1]
			C = scores[2]
			D = scores[3]
			E = scores[4]
			reaction_time_score = ((A+B+C+D+E)/5) + penalty

			draw_text("Your score is: " + str(reaction_time_score) + "ms", font, (255, 255, 255), screen, 700, 200)
			if penalty > 0:
				draw_text("You got a penalty of " + str(penalty) +"ms" + " becuase you clicked while it was still red", font, (255, 255, 255), screen, 700, 250)

			if x < 1:
				data("Reaction_Time", reaction_time_score, "Lower")
				x += 1

			if replay_button.draw():
				repeats = 0
				i = 0
				penalty = 0
				x = 0
				start_time = int(pygame.time.get_ticks())
				change_time = start_time + (random.randint(2000,6000))
				ReactionTime()
		
			draw_text("Replay", font, (255, 255, 255), screen, 700, 400)

		menu_button = Button(1300, 50, button_img, 0.4)
		if menu_button.draw():
			Main_Menu()
		draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)
	
		pygame.display.update()
		clock.tick(60)

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()


class SimonSaysButton():
	def __init__(self, x, y, image, scale): #Assigning the image to the button and giving it coordinates
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect() 
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self): #Draw button on screen
	
		screen.blit(self.image, (self.rect.x, self.rect.y))

	def collision(self):
		action = False
		pos = pygame.mouse.get_pos() #Get mouse position

		if self.rect.collidepoint(pos): #Check to see if the mouse is over the button
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		return action

def Game5():

	main_game_loop = True
	game5_running = True
	numbers = []
	next_number = random.randint(1,9)
	numbers.append(next_number)

	while game5_running:

		if main_game_loop:

			screen.fill((130, 34, 34))
			draw_text("GAME 5", font, (255, 255, 255), screen, 700, 50)

			square1 = SimonSaysButton(500, 200, square_png, 1)
			square1.draw()

			square2 = SimonSaysButton(700, 200, square_png, 1)
			square2.draw()

			square3 = SimonSaysButton(900, 200, square_png, 1)
			square3.draw()

			square4 = SimonSaysButton(500, 400, square_png, 1)
			square4.draw()

			square5 = SimonSaysButton(700, 400, square_png, 1)
			square5.draw()

			square6 = SimonSaysButton(900, 400, square_png, 1)
			square6.draw()

			square7 = SimonSaysButton(500, 600, square_png, 1)
			square7.draw()

			square8 = SimonSaysButton(700, 600, square_png, 1)
			square8.draw()

			square9 = SimonSaysButton(900, 600, square_png, 1)
			square9.draw()
		




			if menu_button.draw():
				Main_Menu()
			draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)



		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

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
		draw_text("These are your Highscores", font, (32, 200, 2), screen, 700, 200)

		AThighscore = data("Aim_Trainer", 0, "Lower")
		Game2highscore = data("Game2", 0, "Lower")
		Game3highscore = data("Game3", 0, "Lower")
		RThighscore = data("Reaction_Time", 0, "Lower")

		if AThighscore == "9999": #Because it is a lower data factor so default will be 9999 not 0
			AThighscore = "N/A"
		if Game2highscore == "0":
			Game2highscore = "N/A"
		if Game3highscore == "0":
			Game3highscore = "N/A"
		if RThighscore == "9999": #Because it is a lower data factor so default will be 9999 not 0
			RThighscore = "N/A"

		draw_text("Your Aim Trainer highscore is " + (AThighscore), font, (32, 200, 2), screen, 700, 400)
		draw_text((Game2highscore), font, (32, 200, 2), screen, 700, 500)
		draw_text((Game3highscore), font, (32, 200, 2), screen, 700, 600)
		draw_text("Your Reaction Time highscore is " + (RThighscore) + "ms", font, (32, 200, 2), screen, 700, 700)

		if menu_button.draw():
			Main_Menu()
		draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

		pygame.display.update()
		clock.tick(60)


Main_Menu()


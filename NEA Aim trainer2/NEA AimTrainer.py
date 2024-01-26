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
	elif game == "Simon_Says":
		game = 4
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
game5_button = Button(1180, 500, button_img, 1)
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
			SimonSays()
		draw_text("Simon Says", font, (255, 255, 255), screen, 1180, 500)

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
					print(repeats)
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
		self.clicked = True

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


#Creating Square instances for Simon says
square1 = SimonSaysButton(500, 200, square_png, 1)
square2 = SimonSaysButton(700, 200, square_png, 1)
square3 = SimonSaysButton(900, 200, square_png, 1)
square4 = SimonSaysButton(500, 400, square_png, 1)
square5 = SimonSaysButton(700, 400, square_png, 1)
square6 = SimonSaysButton(900, 400, square_png, 1)
square7 = SimonSaysButton(500, 600, square_png, 1)
square8 = SimonSaysButton(700, 600, square_png, 1)
square9 = SimonSaysButton(900, 600, square_png, 1)
 

def numbers_check(array1, array2, button):
	array1.append(button)
	array2.append(random.randint(1,9))

def show_button(button):
	square_next_surf = pygame.image.load('graphics/squareNext.png').convert_alpha()
	square_next_rect = square_next_surf.get_rect(center = (0,0))

	background_surf = pygame.image.load('graphics/fakebackground.png').convert_alpha()
	background_rect = background_surf.get_rect(topleft = (-1,1))

	screen.blit(background_surf, background_rect)

	if button == 1:
		square_next_rect = square_next_surf.get_rect(center = (500, 200))
		screen.blit(square_next_surf, square_next_rect)
	if button == 2:
		square_next_rect = square_next_surf.get_rect(center = (700, 200))
		screen.blit(square_next_surf, square_next_rect)
	if button == 3:
		square_next_rect = square_next_surf.get_rect(center = (900, 200))
		screen.blit(square_next_surf, square_next_rect)
	if button == 4:
		square_next_rect = square_next_surf.get_rect(center = (500, 400))
		screen.blit(square_next_surf, square_next_rect)
	if button == 5:
		square_next_rect = square_next_surf.get_rect(center = (700, 400))
		screen.blit(square_next_surf, square_next_rect)
	if button == 6:
		square_next_rect = square_next_surf.get_rect(center = (900, 400))
		screen.blit(square_next_surf, square_next_rect)
	if button == 7:
		square_next_rect = square_next_surf.get_rect(center = (500, 600))
		screen.blit(square_next_surf, square_next_rect)
	if button == 8:
		square_next_rect = square_next_surf.get_rect(center = (700, 600))
		screen.blit(square_next_surf, square_next_rect)
	if button == 9:
		square_next_rect = square_next_surf.get_rect(center = (900, 600))
		screen.blit(square_next_surf, square_next_rect)

	pygame.display.update()
	clock.tick(60)
	
def SimonSays():

	replay_button = Button(1300, 750, button_img, 0.5)
	main_game_loop = True
	game5_running = True
	waitingForInput = False

	sequence = []
	selected_numbers = []
	current_step = 0
	score = 0

	while game5_running:

		pos = pygame.mouse.get_pos()

		if main_game_loop:

			len_sequence = len(sequence)
			screen.fill((130, 34, 34))
			draw_text("GAME 5", font, (255, 255, 255), screen, 700, 50)

			if not waitingForInput:
				pygame.display.update()
				sequence.append(random.randint(1,9))
				for button in sequence:
					show_button(button)
					pygame.time.wait(1000)
				waitingForInput = True
				
			if square1.draw():
				if 1 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False
				print("BUTTON 1")

			if square2.draw():
				if 2 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False
				print("BUTTON 2")

			if square3.draw():
				if 3 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False
				print("BUTTON 3")

			if square4.draw():
				if 4 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False
				print("BUTTON 4")

			if square5.draw():
				if 5 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False
				print("BUTTON 5")

			if square6.draw():
				if 6 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False
				print("BUTTON 6")

			if square7.draw():
				if 7 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False
				print("BUTTON 7")

			if square8.draw():
				if 8 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False

				print("BUTTON 8")

			if square9.draw():
				if 9 == sequence[current_step]:
					current_step += 1
				else:
					main_game_loop = False

				print("BUTTON 9")

			if current_step == len(sequence):
				current_step = 0
				score += 1
				waitingForInput = False

			if menu_button.draw():
				Main_Menu()
			draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

		else:
			screen.fill((130, 34, 34))
			data("Simon_Says", score, "Higher")

			if menu_button.draw():
				Main_Menu()
			draw_text("Menu", font, (255, 255, 255), screen, 1300, 50)

			draw_text("Your score is " + str(score), font, (255, 255, 255), screen, 700, 50)

			if replay_button.draw():
				sequence = []
				selected_numbers = []
				current_step = 0
				score = 0
				SimonSays()
			draw_text("Replay", font, (255, 255, 255), screen, 1300, 750)

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		pygame.display.update()
		clock.tick(60)

def Scores():
	i = 0

	menu_button = Button(1250, 100, button_img, 0.4)

	scorebackground_surf = pygame.image.load('graphics/scorebackground.png').convert_alpha() #Loading a background image
	scorebackground_rect = scorebackground_surf.get_rect(topleft = (0,0))

	option_running = True
	while option_running:

		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #Exit Program
				exit()

		screen.blit(scorebackground_surf, scorebackground_rect)
		draw_text("These are your Highscores", font, (255, 255, 255), screen, 700, 100)

		AThighscore = data("Aim_Trainer", 0, "Lower")
		Game2highscore = data("Game2", 0, "Lower")
		Game3highscore = data("Game3", 0, "Lower")
		RThighscore = data("Reaction_Time", 0, "Lower")
		SShighscore = data("Simon_Says", 0, "Higher")

		if AThighscore == "9999": #Because it is a lower data factor so default will be 9999 not 0
			AThighscore = "N/A"
		if Game2highscore == "0":
			Game2highscore = "N/A"
		if Game3highscore == "0":
			Game3highscore = "N/A"
		if RThighscore == "9999": #Because it is a lower data factor so default will be 9999 not 0
			RThighscore = "N/A"
		if SShighscore == "0":
			SShighscore = "N/A"

		draw_text("Your Aim Trainer highscore is " + (AThighscore), font, (255, 255, 255), screen, 700, 200)
		draw_text("Your Game2 highscore is 0 " + (Game2highscore), font, (255, 255, 255), screen, 700, 300)
		draw_text("Your Game3 highscore is 0 " + (Game3highscore), font, (255, 255, 255), screen, 700, 400)
		draw_text("Your Reaction Time highscore is " + (RThighscore) + "ms", font, (255, 255, 255), screen, 700, 500)
		draw_text("Your Simon Says highscore is " + (SShighscore), font, (255, 255, 255), screen, 700, 600)

		if menu_button.draw():
			Main_Menu()
		draw_text("Menu", font, (255, 255, 255), screen, 1250, 100)

		pygame.display.update()
		clock.tick(60)


Main_Menu()


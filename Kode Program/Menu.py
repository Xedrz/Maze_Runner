import pygame, sys
from stage1 import main_1
from stage2 import main_2
from stage3 import main_3


pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("MAZE RUNNER")

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
    return pygame.font.Font("font/font.ttf", size)

def select_stage():
    while True:
        STAGE_MOUSE_POS = pygame.mouse.get_pos()
        BG = pygame.image.load("image/background_menu.jpg").convert_alpha()
        BG = pygame.transform.scale(BG, (800, 600))
        
        SCREEN.blit(BG, (0, 0))

        STAGE_TEXT = get_font(45).render("SELECT STAGE", True, "#D8D9DA")
        STAGE_RECT = STAGE_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(STAGE_TEXT, STAGE_RECT)
        STAGE1_BUTTON = Button(image=None, pos=(400, 200), 
                            text_input="STAGE 1", font=get_font(50), base_color="#D8D9DA", hovering_color="#FFF6E0")
        STAGE2_BUTTON = Button(image=None, pos=(400, 300), 
                            text_input="STAGE 2", font=get_font(50), base_color="#D8D9DA", hovering_color="#FFF6E0")
        STAGE3_BUTTON = Button(image=None, pos=(400, 400), 
                            text_input="STAGE 3", font=get_font(50), base_color="#D8D9DA", hovering_color="#FFF6E0")

        for button in [STAGE1_BUTTON, STAGE2_BUTTON, STAGE3_BUTTON]:
            button.changeColor(STAGE_MOUSE_POS)
            button.update(SCREEN)

        PLAY_BACK = Button(image=None, pos=(400, 500), 
                            text_input="BACK", font=get_font(50), base_color="#D8D9DA", hovering_color="#FFF6E0")

        PLAY_BACK_POS = pygame.mouse.get_pos()
        PLAY_BACK.changeColor(STAGE_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if STAGE1_BUTTON.checkForInput(STAGE_MOUSE_POS):
                    main_1()
                    main_menu()

                elif STAGE2_BUTTON.checkForInput(STAGE_MOUSE_POS):
                    main_2()
                    main_menu()

                elif STAGE3_BUTTON.checkForInput(STAGE_MOUSE_POS):
                    main_3()
                    main_menu()
                elif PLAY_BACK.checkForInput(PLAY_BACK_POS):
                    main_menu()

                
        pygame.display.update()

def play():
    select_stage()
    
def about():
    while True:
        ABOUT_MOUSE_POS = pygame.mouse.get_pos()

        BG = pygame.image.load("image/background_menu.jpg").convert_alpha()
        BG = pygame.transform.scale(BG, (800, 600))
        
        SCREEN.blit(BG, (0, 0))

        ABOUT_TEXT = get_font(55).render("MAZE RUNNER", True, "#D8D9DA")
        ABOUT_RECT = ABOUT_TEXT.get_rect(center=(SCREEN.get_width() // 2, 100))
        SCREEN.blit(ABOUT_TEXT, ABOUT_RECT)

        about_text = [
            "Maze Runner adalah game labirin",
            "dimana pemain dapat memilih karakter",
            "dan tema labirin sesuai dengan selera",
            "masing-masing. Pemain juga dapat",
            "menikmati gameplay yang berbeda di setiap",
            "stagenya. Setiap tahap menawarkan",
            "pengalaman yang unik, dengan labirin yang", 
            "rumit dan berbagai rintangan yang harus",
            "diatasi. Bisakah Anda menaklukkan setiap",
            "tahap dan keluar dari labirin dengan sukses",
            "Ayo mulai petualangan Anda di Maze Runner sekarang!",
        ]

        y_position = 200  # Posisi awal Y untuk pusatkan teks di layar

        for line in about_text:
            text_surface = get_font(15).render(line, True, "#D8D9DA")  # Buat surface teks untuk setiap baris
            text_rect = text_surface.get_rect(center=(SCREEN.get_width() // 2, y_position))  # Atur posisi teks di tengah layar
            SCREEN.blit(text_surface, text_rect)
            y_position += 20  # Spasi antar baris teks              
        
        ABOUT_BACK = Button(image=None, pos=(100, 550), 
                            text_input="BACK", font=get_font(30), base_color="#D8D9DA", hovering_color="#FFF6E0")

        ABOUT_BACK.changeColor(ABOUT_MOUSE_POS)
        ABOUT_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ABOUT_BACK.checkForInput(ABOUT_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    

def main_menu():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.mixer.music.load("music/Sost.mp3")
    pygame.mixer.music.play(-3)
    while True:
        BG = pygame.image.load("image/background_menu.jpg").convert_alpha()
        BG = pygame.transform.scale(BG, (800, 600))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(55).render("MAZE RUNNER", True, "#D8D9DA")
        MENU_RECT = MENU_TEXT.get_rect(center=(420, 100))

        PLAY_BUTTON = Button(image=None, pos=(400, 250), 
                            text_input="PLAY", font=get_font(55), base_color="#D8D9DA", hovering_color="#FFF6E0")
        ABOUT_BUTTON = Button(image=None, pos=(400, 350), 
                            text_input="ABOUT", font=get_font(55), base_color="#D8D9DA", hovering_color="#FFF6E0")
        QUIT_BUTTON = Button(image=None, pos=(400, 450), 
                            text_input="QUIT", font=get_font(55), base_color="#D8D9DA", hovering_color="#FFF6E0")

        SCREEN.blit(BG, (0, 0))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    about()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            pygame.mixer.music.fadeout(1000)
        if keys[pygame.K_1]:
            pygame.mixer.music.play(-3)

        pygame.display.update()

main_menu()

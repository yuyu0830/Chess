import pygame


# 화면 크기 설정
screen_width = 800 # 가로 크기
screen_height = 450
screen = pygame.display.set_mode((screen_width, screen_height))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
to_x = 0
to_y = 0
gun_speed = 0

# 캐릭터
character_1 = pygame.image.load("BLACK_BISHOP.png")
gun_1 = pygame.image.load("BLACK_BISHOP.png")
pygame.transform.scale(gun_1, [50, 50])

class gun:
    def __init__(self, character, screen_width, screen_height):
        self.character = character
        self.character_width = self.character.get_width()
        self.character_height = self.character.get_height()
        self.center_pos = [screen_width // 2, screen_height // 2]
        
    # 캐릭터 중앙 좌표, 스크린 중앙 좌표
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_x_center = self.screen_width / 2
        self.screen_y_center = self.screen_height / 2
        self.screen_center = self.screen_x_center, self.screen_y_center

        self.character_x = self.character_width / 2
        self.character_y = self.character_height / 2
        self.character_center = self.character_x, self.character_y
    
        self.screen_center_blit_pos = (self.screen_x_center - self.character_x), (self.screen_y_center  - self.character_y)# 스크린 중앙에 캐릭터 중앙 배치 좌표

    # 스크린의 pos좌표에 캐릭터 그리기
    def character_blit(self, screen, character, pos):
        self.screen = screen
        self.charater = character
        self.pos = pos
        self.screen.blit(self.character, self.pos)

    # 총알 rect와 시작 위치
    def gun_pos(self, gun):
        self.gun = gun
        self.gun_rect = gun.get_rect()
        self.gun_width = gun.get_width()
        self.gun_height = gun.get_height()
        self.gun_start_pos = self.character_center

    # 총알을 프레임 위치 그리기
    def gun_frame_circle(self, character_width, border, circle_pos):
        self.circle_pos = circle_pos
        self.circle_radius = 120
        pygame.draw.circle(self.screen, WHITE, circle_pos, self.circle_radius, border)
        
####################  문제가 되는 부분..
    # 총 그리기
    def gun_draw(self, screen):
        self.screen = screen
        self.mouse_point_blit = (self.to_x), (self.to_y)
        pygame.draw.circle(self.screen,(255, 255, 255), self.mouse_point_blit, 30)
    
    def gun_shoot(self, mouse_point):
        cen_to_mos = [mouse_point[0] - self.center_pos[0], self.center_pos[1] - mouse_point[1]]
        tri = (cen_to_mos[0]**2) + (cen_to_mos[1]**2)
        if tri < self.circle_radius**2: #원 안에 마우스 있음
            self.to_x = mouse_point[0]
            self.to_y = mouse_point[1]
        else: #원 밖에 마우스 있음
            temp = (self.circle_radius / tri**(1/2))

            self.to_x = self.center_pos[0] + (cen_to_mos[0] * temp)
            self.to_y = self.center_pos[1] - (cen_to_mos[1] * temp)
        
        # self.w_max = (self.screen_width / 2) - self.circle_radius + self.gun_width / 2
        # self.w_min = (self.screen_width / 2) + self.circle_radius - self.gun_width / 2
        # self.h_min = (self.screen_height / 2) + self.circle_radius - self.gun_width / 2
        # self.h_max = (self.screen_height / 2) - self.circle_radius + self.gun_width / 2
        # self.left_top_x = (self.screen_width / 2) - self.circle_radius / 2
        # self.left_bottom_y = (self.screen_height / 2) + self.circle_radius / 2
        # self.left_top_y = (self.screen_height / 2) - self.circle_radius / 2

        # self.a = (self.to_x - self.left_top_x) / 2
        
        # if self.to_x < self.screen_center[0]:
        #     if self.to_y < self.screen_center[1]:
                
        #         if self.to_x > self.left_top_x:
        #             self.to_y = self.to_y - self.a + self.gun_height / 2
        #         if self.to_x < self.left_top_x:
        #             self.to_y = self.to_y - self.a + self.gun_height / 2
        #         # if self.to_y > self.lef_top_y:


        #         if self.to_y < self.h_max:
        #             self.to_y = self.h_max
        #         if self.w_max > self.to_x: 
        #             self.to_x = self.w_max
        #             self.to_y = self.to_y
        #         else:
        #             self.to_y = self.to_y
        #         # if self.w_min < self.to_x:
        #         #     self.to_x = self.w_min 
        #         # if self.h_max > self.to_y:
        #         #     self.to_y = self.h_max 

#################### 
        


pygame.init() # 초기화 (반드시 필요)




# 화면 타이틀 설정
pygame.display.set_caption("S_H_ Game") # 게임 이름
c = gun(character_1, screen_width, screen_height)
# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임이 진행중이 아님

    screen.fill(BLACK)
    
    c.character_blit(screen, character_1, c.screen_center_blit_pos)
    m = c.gun_frame_circle(c.character_width, 2, c.screen_center)
    mouse_point = pygame.mouse.get_pos()
    c.gun_pos(gun_1)
    c.gun_shoot(mouse_point)
    c.gun_draw(screen)
    pygame.display.update()
pygame.quit()
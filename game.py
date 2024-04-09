import pygame , sys, random 
from pygame.math import Vector2


class Fruit:
    def __init__(self):
        self.randomize()
        

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size , self.pos.y*cell_size , cell_size, cell_size)
        screen.blit(apple,fruit_rect)
        #pygame.draw.rect(screen , (250, 0 , 0) , fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x , self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction =Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha() 
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()
    
    def draw_snake(self):
        self.update_head()
        self.update_tail()
        for index,block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)

            elif index == len(self.body)-1:
                screen.blit(self.tail , block_rect)
            
            else : 
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x :
                    screen.blit(self.body_vertical,block_rect)

                elif previous_block.y == next_block.y :
                    screen.blit(self.body_horizontal,block_rect)

                else : 
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1 :  
                        screen.blit(self.body_tl,block_rect)                
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1  : 
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1  : 
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1  : 
                        screen.blit(self.body_br,block_rect)


    def update_direction(self,d):
        if not self.body[0] + d == self.body[1]:
            self.direction = d

    
    def update_head(self):
        head_dir = self.body[1] - self.body[0]
        if head_dir == Vector2(1,0): self.head = self.head_left
        elif head_dir == Vector2(-1,0): self.head = self.head_right
        elif head_dir == Vector2(0,1): self.head = self.head_up
        elif head_dir == Vector2(0,-1): self.head = self.head_down


    def update_tail(self):
        tail_dir = self.body[len(self.body) - 2 ] - self.body[len(self.body) - 1]
        if tail_dir == Vector2(1,0): self.tail = self.tail_left
        elif tail_dir == Vector2(-1,0): self.tail = self.tail_right
        elif tail_dir == Vector2(0,1): self.tail = self.tail_up
        elif tail_dir == Vector2(0,-1): self.tail = self.tail_down


    def move_snake(self):
        if self.new_block == True :
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
            
        else :    
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True


class Main: 
    def __init__(self):
        self.fruit = Fruit ()
        self.snake = Snake()
        self.score = 0
        self.fail = False
        
    def update(self):
        self.check_fail()
        if self.fail==False :
            self.snake.move_snake()
            self.check_collision()

       

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.check_fail()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score = self.score + 1

        for block in self.snake.body[1:]:
            if block == self.fruit.pos : 
                self.fruit.randomize()
    
    def check_fail(self):
        if (not 0 <= self.snake.body[0].x < cell_number) or  (not 0 <= self.snake.body[0].y < cell_number) :
            self.game_over()
            self.fail=True
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                self.fail=True

    def reset(self):
        self.snake.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.score = 0

    def game_over(self):

        game_over_text = '''GAME OVER IF YOU WANT TO RESET PRESS ANY KEY'''
        game_over_surface = game_font.render(game_over_text, True , (56,74,12))
        game_over_rect = game_over_surface.get_rect(center =((cell_number * cell_size)/2 , (cell_number * cell_size)/2))

        screen.blit(game_over_surface,game_over_rect)


    def draw_score(self):
        score_text = "score : " + str(self.score)
        score_surface = game_font.render(score_text, True , (56,74,12))
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number -40
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        bg_rect = pygame.Rect(score_rect.left - 5 , score_rect.top - 5 , score_rect.width + 10 , score_rect.height + 10)

        screen.blit(score_surface,score_rect)
        pygame.draw.rect(screen , (56,74,12) , bg_rect , 2)

pygame.init()
cell_size = 40
cell_number = 20
screen=pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number))
clock = pygame.time.Clock()
main_game = Main ()
apple_img = pygame.image.load('graphics/apple.png').convert_alpha()
apple = pygame.transform.scale(apple_img, (cell_size, cell_size))
game_font = pygame.font.Font(None , 25)
d=main_game.snake.direction

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            dpred=d
            if main_game.fail == True :
                main_game.fail = False
                main_game.reset()
                d=Vector2(1,0)
                main_game.snake.update_direction(d)
                pass

            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    d = Vector2(0,-1)
            elif event.key == pygame.K_DOWN:
                if  main_game.snake.direction.y != -1:
                    d = Vector2(0,1)
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    d = Vector2(1,0)
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    d = Vector2(-1,0)
            main_game.snake.update_direction(d)

            

    screen.fill((123,182,101))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
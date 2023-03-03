import pygame 
import math

pygame.init()

WIDTH, HEIGHT = 1000, 500
BAR_WIDTH, BAR_HEIGHT = 10, 150
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong game")

class Line: 
	win = screen 
	width, height = 8, 20
	color = WHITE

	def draw(self):
		for i in range(0, HEIGHT, 2):
			self.rect = [WIDTH // 2 - self.width // 2, self.height * i, self.width, self.height]
			pygame.draw.rect(self.win, self.color, self.rect)

class Ball:
	speed = 8
	epsilon = 10
	win = screen

	def __init__(self, color, x, y, radius):
		self.color = color 
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.radius = radius
		self.x_speed = self.speed
		self.y_speed = 0

	def draw(self):
		ball = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

	def move(self): 
		self.x += self.x_speed 
		self.y += self.y_speed

	def collision_of_ball(self, right_bar, left_bar):
		self.move()

		#reflex with ceiling
		if self.y - self.radius <= 0:
			self.y_speed *= -1
		#reflex with floor
		if self.y +  self.radius >= HEIGHT:
			self.y_speed *= -1

		#reflex with right bar
		if self.y >= right_bar.y and self.y <= right_bar.y + right_bar.HEIGHT:
			if (self.x + self.radius) >= (right_bar.x): 
				self.x_speed *= -1 
				right_bar_y_center = right_bar.y + right_bar.HEIGHT / 2 
				speed_adjustment_right = (right_bar_y_center - self.y) // self.epsilon 
				self.y_speed = speed_adjustment_right * -1

		#reflex with left bar
		if self.y >= left_bar.y and self.y <= left_bar.y + left_bar.HEIGHT:
			if (self.x - self.radius) <= (left_bar.x + left_bar.WIDTH):
				self.x_speed *= -1
				left_bar_y_center = left_bar.y + left_bar.HEIGHT / 2 
				speed_adjustment_left = (left_bar_y_center - self.y) // self.epsilon
				self.y_speed = speed_adjustment_left * -1

	def reset_after_one_game(self):
		self.x = self.original_x
		self.y = self.original_y
		self.y_speed = 0
		self.x_speed *= -1

	def reset_after_one_set(self):
		self.x = self.original_x
		self.y = self.original_y
		self.y_speed = 0
		self.x_speed *= 1

class Bar: 
	speed = 15
	win = screen

	def __init__(self, color, x, y, WIDTH, HEIGHT):
		self.color = color  
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.WIDTH = WIDTH
		self.HEIGHT = HEIGHT

	def draw(self):
		pygame.draw.rect(self.win, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))

	def reset(self):
		self.x = self.original_x
		self.y = self.original_y


class Score(Ball, Bar):
	SCORE_FONT = pygame.font.SysFont("Comicsans", 50)
	right_score = 0
	left_score = 0 
	win = screen

	def draw_score(self):
		if ball.x <= 0:
			Score.right_score += 1
			ball.reset_after_one_set()
		if ball.x >= WIDTH:
			Score.left_score += 1
			ball.reset_after_one_set()

		right_score_text = Score.SCORE_FONT.render(f"{Score.right_score}", 1, WHITE) 
		left_score_text = Score.SCORE_FONT.render(f"{Score.left_score}", 1, WHITE) 
		Score.win.blit(right_score_text, ((WIDTH * (3/4)) - right_score_text.get_width() // 2, 20))
		Score.win.blit(left_score_text, ((WIDTH * (1/4)) - left_score_text.get_width() // 2, 20))

		if Score.right_score > 4: 
			winning_text_right = Score.SCORE_FONT.render("Right Player Win", 1, WHITE)
			Score.win.blit(winning_text_right, (WIDTH // 2 - winning_text_right.get_width() // 2, HEIGHT //2 - winning_text_right.get_height() // 2))
			pygame.display.update()
			pygame.time.delay(5000)
			ball.reset_after_one_game()
			right_bar.reset()
			Score.right_score = 0
			Score.left_score = 0

		elif Score.left_score > 4: 
			winning_text_left = Score.SCORE_FONT.render("Left Player Win", 1, WHITE)
			Score.win.blit(winning_text_left, (WIDTH // 2 - winning_text_left.get_width() // 2, HEIGHT //2 - winning_text_left.get_height() // 2))
			pygame.display.update()
			pygame.time.delay(5000)
			ball.reset_after_one_game()
			left_bar.reset()
			Score.left_score = 0
			Score.right_score = 0

def move_of_bar(keys, left_bar, right_bar):
	if keys[pygame.K_w]:
		if left_bar.y > 0 or left_bar.y == 0:
			left_bar.y -= left_bar.speed
	if keys[pygame.K_s]:
		if left_bar.y + left_bar.HEIGHT < HEIGHT or left_bar.y + left_bar.HEIGHT == HEIGHT:  
			left_bar.y += left_bar.speed

	if keys[pygame.K_UP]:
		if right_bar.y > 0 or right_bar.y == 0:
			right_bar.y -= right_bar.speed
	if keys[pygame.K_DOWN]:
		if right_bar.y + right_bar.HEIGHT < HEIGHT or right_bar.y + right_bar.HEIGHT == HEIGHT:  
			right_bar.y += right_bar.speed


			
def draw(screen):
	screen.fill(BLACK)
	line = Line()
	ball.draw()
	left_bar.draw()
	right_bar.draw()
	line.draw()




left_bar = Bar(WHITE, 0, HEIGHT // 2 - BAR_HEIGHT // 2, BAR_WIDTH, BAR_HEIGHT)
right_bar = Bar(WHITE, WIDTH - BAR_WIDTH, HEIGHT // 2 - BAR_HEIGHT // 2, BAR_WIDTH, BAR_HEIGHT)
ball = Ball(WHITE, WIDTH//2, HEIGHT//2, 8)

def main():
	clock = pygame.time.Clock()
	RUNNING = True 
	while RUNNING:
		clock.tick(60)
		draw(screen)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUNNING = False
				break
		keys = pygame.key.get_pressed()
		
		move_of_bar(keys, left_bar, right_bar)

		ball.collision_of_ball(right_bar, left_bar)

		Score.draw_score(ball)

		pygame.display.update()

	pygame.quit()

if __name__ == '__main__':
	main()




		
		

	








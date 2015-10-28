# made by zakx <sg@unkreativ.org> at 0hgamejam @ chaosdorf
import sys
import pygame
from helpers import load_image, load_sound

if not pygame.font:
	print('Fonts disabled')
if not pygame.mixer:
	print('Sound disabled')


class Gamestate:
	S_DEFAULT = 0
	S_GAME_NOLIMIT = 1
	S_GAME_LIMIT = 2
	S_GAME_OVER = 3

	def __init__(self):
		self.points = 0
		self.ratelimit = 0
		self.level = 0
		self.timer = 400
		self.state = self.S_DEFAULT

	def step(self):
		if self.state == self.S_DEFAULT:
			return True
		if self.state != self.S_GAME_OVER:
			self.timer -= 1
			if self.timer <= 0:
				self.state = self.S_GAME_OVER
				return False
		if self.state == self.S_GAME_LIMIT:
			self.ratelimit -= 1
			if self.ratelimit <= 0:
				self.state = self.S_GAME_NOLIMIT
			return True
		elif self.state == self.S_GAME_NOLIMIT:
			return True

	def set_limit(self):
		self.state = self.S_GAME_LIMIT
		self.ratelimit = 4 * self.level
		self.level += 1
		self.points += 2 * self.level
		print("level = ", self.level)
		print("limit = ", self.ratelimit)
		print("points = ", self.points)


class HatelimitMain:
	def __init__(self, width=800, height=600):
		pygame.init()
		self.width = width
		self.height = height

		self.screen = pygame.display.set_mode((self.width, self.height))
		self.airhorn_sprites = pygame.sprite.Group()
		self.nope_sprites = pygame.sprite.Group()
		self.clock = pygame.time.Clock()
		self.airhorn_sound = load_sound('airhorn.wav')
		self.derf_sound = load_sound('derf.wav')
		self.font = pygame.font.Font(None, 36)
		self.state = Gamestate()

	def main_loop(self):
		while True:
			self.clock.tick(25)
			self.animate_airhorns()
			self.animate_nope()
			if self.state.state == Gamestate.S_DEFAULT:
				gotext = self.font.render("press space to feel the hate", 1, (255, 255, 255))
				gotextpos = gotext.get_rect(centerx=self.width/2, centery=self.height/2)
				self.screen.blit(gotext, gotextpos)
				pygame.display.update()
			if not self.state.step():
				self.screen.fill((0, 0, 0))
				gotext = self.font.render("YOU WILL NOW FEEL THE HATE", 1, (255, 0, 0))
				gotextpos = gotext.get_rect(centerx=self.width/2, centery=self.height/2)
				self.screen.blit(gotext, gotextpos)
				fstext = self.font.render("Final Score: {}".format(self.state.points), 1, (255, 0, 0))
				fstextpos = fstext.get_rect(centerx=self.width/2, centery=self.height/2+50)
				self.screen.blit(fstext, fstextpos)
				pygame.display.flip()
			else:
				text = self.font.render("Score: {}".format(self.state.points), 1, (255, 255, 255))
				textpos = text.get_rect(centerx=self.width/2)
				self.screen.blit(text, textpos)
				pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						# game logic, top kek
						if self.state.state == Gamestate.S_GAME_NOLIMIT:
							self.new_airhorn()
							self.state.set_limit()
						elif self.state.state == Gamestate.S_GAME_LIMIT:
							self.new_nope()
							self.state.points -= 2
						elif self.state.state == Gamestate.S_DEFAULT:
							self.state.state = Gamestate.S_GAME_NOLIMIT
							self.screen.fill((0, 0, 0))
					elif event.key == pygame.K_LEFT:
						self.new_nope()
					elif event.key == pygame.K_RIGHT:
						self.new_airhorn()

	def animate_airhorns(self):
		for sprite in self.airhorn_sprites.sprites():
			self.airhorn_sprites.clear(self.screen, lambda s, r: s.fill((0, 0, 0), r))
			if sprite.rect.left < 0 and sprite.rect.top > 600:
				self.airhorn_sprites.remove(sprite)
				print("removed sprite")
				continue
			sprite.step()
			self.airhorn_sprites.draw(self.screen)

	def new_airhorn(self):
		airhorn = Airhorn()
		self.airhorn_sprites.add(pygame.sprite.RenderClear((airhorn)))
		self.airhorn_sound.play()

	def animate_nope(self):
		for sprite in self.nope_sprites.sprites():
			self.nope_sprites.clear(self.screen, lambda s, r: s.fill((0, 0, 0), r))
			sprite.cycles += 1
			if sprite.cycles > 5:
				self.nope_sprites.remove(sprite)
				print("removed nope sprite")
				continue
			self.nope_sprites.draw(self.screen)

	def new_nope(self):
		nope = Nope()
		self.nope_sprites.add(pygame.sprite.RenderClear((nope)))
		self.derf_sound.play()


class Airhorn(pygame.sprite.Sprite):
	def __init__(self, west=True):
		super().__init__()
		self.image, self.rect = load_image("airhorn2.png", -1)
		if west:
			self.image = pygame.transform.flip(self.image, True, False)
		self.rect.move_ip(800, 0)

	def step(self):
		self.rect.move_ip(-30, 10)


class Nope(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image, self.rect = load_image("derf.jpg", None)
		self.image = pygame.transform.scale(self.image, (int(500*0.80), int(707*0.80)))
		self.rect.move_ip(200, 0)
		self.cycles = 0

if __name__ == "__main__":
	main_window = HatelimitMain()
	main_window.main_loop()

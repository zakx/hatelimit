import os
import pygame


def load_image(name, colorkey=None):
	fullname = os.path.join('assets', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error as message:
		print('Cannot load image:', name)
		raise SystemExit(message)
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image, image.get_rect()


def load_sound(name):
	class NoneSound:
		def play(self):
			pass
	if not pygame.mixer:
		return NoneSound()
	fullname = os.path.join('assets', name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error as message:
		print(('Cannot load sound:', fullname))
		raise SystemExit(message)
	return sound

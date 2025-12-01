import pygame


def draw(WIDHT=500, HEIGHT=500, cmp_image_list=None):
	pygame.init()

	screen = pygame.display.set_mode((WIDHT, HEIGHT))

	run = True

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		screen.fill((50, 50, 50))

		# pygame.draw.rect(screen, (111.2, 0, 0), (10.3, 10, 10, 10))
		if cmp_image_list is not None:
			for i in range(len(cmp_image_list)):
				pixel = cmp_image_list[i]
				# print(pixel.color)
				pygame.draw.rect(screen, pixel.color, (pixel.x, pixel.y, pixel.size, pixel.size), 0)

		pygame.display.update()

	pygame.quit()


if __name__ == '__main__':
	draw()
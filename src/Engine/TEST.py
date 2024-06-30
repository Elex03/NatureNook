import pygame as pg
import sys

class Button:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pg.Rect(x, y, width, height)
        try:
            self.image = pg.image.load(image_path).convert_alpha()
            print(f"Button image loaded successfully from '{image_path}'")
        except Exception as e:
            print(f"Error loading image from '{image_path}': {e}")
            raise
        self.image = pg.transform.scale(self.image, (width, height))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    pg.init()
    win_size = (630, 480)
    screen = pg.display.set_mode(win_size)
    clock = pg.time.Clock()
    button = Button(10, 10, 150, 50, 'resources/textures/button_image2.png')
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button.is_clicked(event.pos):
                    print("Button clicked!")

        screen.fill((0, 0, 0))
        button.draw(screen)
        pg.display.flip()
        clock.tick(60)

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()

import pygame

class Tile:
    def __init__(self, x:int, y:int, tile_size:int):
        self.tile_size = tile_size
        self.x = x * self.tile_size
        self.y = y * self.tile_size

        self.color = 'dark' if (x + y) % 2 else 'light'
        self.draw_color = (220, 189, 194) if self.color == 'light' else (92, 75, 75)
        self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 200, 10)
        self.highlight = False

        self.piece = None

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.tile_size,
            self.tile_size
        )

    def draw(self, display):
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.piece is not None:
            cRect = self.piece.img.get_rect()
            cRect.center = self.rect.center
            display.blit(self.piece.img, cRect.topleft)
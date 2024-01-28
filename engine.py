import pygame
from cell import Cell
from color import hsl_to_rgb


class Engine:
    fps = 60
    tW, tH = 16, 16
    gW, gH = 54, 54
    sW, sH = tW * gW + 240, tH * gH

    def __init__(self):
        self.frame_mode = True
        self.screen = pygame.display.set_mode((self.sW, self.sH), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.grid = [[Cell(x, y) for y in range(self.gW)] for x in range(self.gH)]
        self.color_key = 1
        self.mouse_down = False
        self.cell_border = True

    def toggle_frame_mode(self):
        if self.frame_mode:
            self.screen = pygame.display.set_mode((self.sW, self.sH), pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode((self.sW, self.sH))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_b:
                    self.cell_border = not self.cell_border
                elif event.key == pygame.K_f:
                    self.frame_mode = not self.frame_mode
                    self.toggle_frame_mode()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
                    self.handle_mouse_event()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    self.color_key += 1 / 72
                elif event.y == -1:
                    self.color_key -= 1 / 72
                if self.color_key > 1:
                    self.color_key = 0
                if self.color_key < 0:
                    self.color_key = 1
        return True

    def handle_mouse_event(self):
        x, y = pygame.mouse.get_pos()
        row, col = int(x / self.tW), int(y / self.tH)
        if 0 <= row < self.gH and 0 <= col < self.gW:
            self.grid[row][col].k = self.color_key
            self.grid[row][col].a = True

    def draw(self):
        for i in range(self.gW):
            for j in range(self.gH):
                if self.grid[i][j].a:
                    if self.cell_border:
                        rect = (i * self.tW + 1, j * self.tH + 1, self.tW - 2, self.tH - 2)
                    else:
                        rect = (i * self.tW, j * self.tH, self.tW, self.tH)
                    pygame.draw.rect(self.screen, hsl_to_rgb(self.grid[i][j].k), rect)
        pygame.draw.rect(self.screen, hsl_to_rgb(self.color_key),
                         (self.sW - 120 - self.tW * 6 / 2, self.sH / 2 - self.tH * 6 / 2, self.tW * 6, self.tH * 6))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            if self.mouse_down:
                self.handle_mouse_event()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)

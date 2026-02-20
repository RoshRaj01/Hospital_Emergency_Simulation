import pygame

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, (30, 144, 255), self.rect, border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=6)

        label = font.render(self.text, True, (255, 255, 255))
        screen.blit(label, (
            self.rect.centerx - label.get_width() // 2,
            self.rect.centery - label.get_height() // 2
        ))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

import pygame

class Doctor:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.status = "free"

    def draw(self, screen, camera_y):
        screen.blit(self.image, (self.x, self.y - camera_y))


class Patient:
    def __init__(self, severity, standing_img, lying_img):
        self.severity = severity
        self.standing_img = standing_img
        self.lying_img = lying_img

    def draw_standing(self, screen, x, y, camera_y):
        screen.blit(self.standing_img, (x, y - camera_y))

    def draw_lying(self, screen, x, y, camera_y):
        screen.blit(self.lying_img, (x, y - camera_y))

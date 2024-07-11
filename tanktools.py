import pygame as p


def getRotatedImage(image, rect, new_angle):
    new_image = p.transform.rotate(image, new_angle)
    new_rect = new_image.get_rect(center=rect.center)
    return new_image, new_rect

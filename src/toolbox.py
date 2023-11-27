import pygame
import math
import socket

def rotate(image, rect, angle):
    """
    rotate returns the rotated version of image and the rotated image's rectangle.
    """
    # Get a new imagae that is the original image but rotated
    new_image = pygame.transform.rotate(image, angle)
    # Get a new rect with the center of the old rect
    new_rect = new_image.get_rect(center=rect.center)
    return new_image, new_rect


def angleBetweenPoints(x1, y1, x2, y2):
    """
    angleBetweenPoints returns the angle between two points.
    """
    x_difference = x2-x1
    y_differnece = y2-y1
    return math.degrees(math.atan2(-y_differnece, x_difference))


def centeringCoords(thing, screen):
    """
    centeringCoords returns the coords that will put thing in the center of the screen.
    """
    new_x = screen.get_width()/2 - thingy.get_width()/2
    new_y = screen.get_height()/2 - thingy.get_height()/2
    return new_x, new_y


class keyDownListener():
    """
    keyDownListener keeps track of one key and says when it gets pressed down.
    self.down will be True once every time the key is pressed and False otherwise.
    """
    def __init__(self):
        self.down = False
        self.is_up = False
        
    def update(self, key_pressed):
        if not key_pressed:
            self.is_up = True
            self.down = False
        else:
            if self.is_up:
                self.down = True
            else:
                self.down = False
            self.is_up = False


def getMyIP():
    """
    getMyIP returns the IP address on the computer you run it on.
    This may not work properly if you're not connected to the internet.
    (If this code seems super complicated, don't worry.. I don't understand it either  -Andy)
    """
    return str((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
             or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]])
            + ["no IP found"])[0])







"""
The goal is to create an easy to use image system, to open images, and make certain they're in the correct
shape for use with numpy and or keras. There should be a system to display images easily, and to update the screen.
"""

import pygame, numpy as np
from PIL import Image

class ImageBench:
    """
    A system to easily and correctly draw points and images on the screen
    :param current_image: A numpy array of the current image
    :param points: A list containing tuples or lists of tuples, each tuple in (x, y) format
    :param surface: The location that things will be drawn to.
    :param camera: Possible camera to use as the image source
    :param color: pygame color
    """
    current_image = None
    points = []
    surface = None
    camera = None
    color = pygame.Color(100, 170, 250, 170)

    def __init__(self, surface, current_image=None, points=None):
        """
        Creates an ImageBench object
        :param surface: The location to be drawn to
        :param current_image: An image in the form of a numpy array, a PIL Image, or a pygame surface, or a path string
        :param points: A list of points or point lists
        """
        self.surface = surface
        self.redraw(current_image, points)


    def redraw(self, new_source=None, new_points=None, new_surface=None):
        """

        :param new_source: An image in the form of a numpy array, a PIL Image, or a pygame surface, or a path string
        :param new_points: This is a list of (x, y) tuples, or if instead of a tuple used at any point in the list
                           there is another list lines will be drawn in order between those (x, y) tuples
        :param new_surface: The target to be drawn to, pygame surface
        :return: The screen that is drawn to
        """

        '''
        If there is no new image, the screen should just be rendered with the old image
        If there are no points then the old points will be used
        If surf is passed in then all things should be done to that surface rather than the surface contained within
        '''

        self.update_image(new_source)
        self.update_points(new_points)
        self.update_surface(new_surface)

        self.draw_image()
        self.draw_points()


    def draw_lines(self, points):

        pygame.draw.lines(self.surface, self.color, False, points, 1)


    def draw_point(self, xy_tuple):
        """
        Draws a point on the internal surface
        :param xy_tuple: Length 2 tuple of ints
        :return: None
        """
        x, y = xy_tuple

        points = []
        size = 2
        points.append((x-size, y-size))
        points.append((x+size, y-size))
        points.append((x+size, y+size))
        points.append((x-size, y+size))
        points.append((x-size, y-size))
        pygame.draw.lines(self.surface, self.color, True, points, 1)

    def draw_points(self):
        """
        Takes no arguments, it just draws all of the internal points
        :return: None
        """
        if self.points is not None:
            for item in self.points:
                if isinstance(item, tuple) and len(item) == 2:
                    self.draw_point(item)
                elif isinstance(item, list):
                    self.draw_lines(item)

    def draw_image(self):
        """
        Takes no arguments, just draws the current internal image
        :return: None
        TODO: add the ability to specify the location of the blit
        """

        self.surface.fill((0, 0, 0))
        if self.current_image is not None:
            image_surface = to_surface(self.current_image) #Converts the internal array to a drawable form (pygame surface)

            self.surface.blit(image_surface, (0,0))


    def update_image(self, img_source):
        """
        Updates the internal image
        :param img_source: An image in the form of a numpy array, a PIL Image, or a pygame surface, or a path string
                            if the value is None or any falsey value nothing is done
        :return: None
        """
        if img_source is not None:
            img_array = to_array(img_source)
            self.current_image = img_array

    def update_points(self, new_points):
        """
        Updates the current list of points to be drawn
        :param new_points: List of point tuples or lists of point tuples
                           if the value is None or any falsey value nothing is done
        :return: None
        """
        if new_points != None:
            self.points = new_points

    def update_surface(self, new_surface):
        """
        Updates the internala reference of the target surface
        :param new_surface: Pygame surface to be drawn to
                           if the value is None or any falsey value nothing is done
        :return: None
        """
        if new_surface:
            self.surface = new_surface

    def update_color(self, r, g, b, a):
        self.color = pygame.Color(r, g, b, a)



def to_array(origin):
    """

    :param origin: Origin should be a PIL image, a path string, or a pygame surface
    :return: A numpy array
    """
    if isinstance(origin, Image.Image):
        """
        Check if the origin is a PIL image
        """
        print(origin.size)
        #origin = origin.rotate(90, expand=True)
        origin = np.asarray(origin, dtype=np.uint8)
        print(origin.shape)
        return origin
    elif isinstance(origin, str):
        return to_array(Image.open(origin))

    elif isinstance(origin, type(pygame.Surface((1,1)))):
        """
        Pygame surfaces are worked with in the same way as PIL images
        They have their axes swapped
        So on output to pygame surfaces they swapped again
        """

        return np.swapaxes(pygame.surfarray.array3d(origin), 0, 1)
    elif isinstance(origin, np.ndarray):
        """
        Return the array if it is already an array
        """
        return origin
    else:
        raise Exception('Incompatible Type of Object')

def to_PIL(origin):
    if not isinstance(origin, np.ndarray):
        origin = to_array(origin)
    return Image.fromarray(origin)

def to_surface(origin):
    if not isinstance(origin, np.ndarray):
        origin = to_array(origin)
    return pygame.surfarray.make_surface(np.swapaxes(origin, 0, 1))

def rgb_to_grey(array):
    raise Exception("Not currently implemented")

def grey_to_rgb(array):
    raise Exception("Not currently implemented")


if __name__ == '__main__':
    # to_array(Image.open('test.jpg'))
    # to_array('test.jpg')
    # to_array(pygame.Surface((2,1)))
    #
    # img = Image.open('rgba.png')
    # img.show()
    img = pygame.image.load("rgba.png")
    # input('waiting...')
    # to_PIL(to_array('rgba.png')).show()

    pygame.init()
    size = w, h = 500, 400
    screen = pygame.display.set_mode(size)

    bench = ImageBench(screen, img, [(30, 30), [(30, 30), (60, 60), (90, 70)], (60, 60), (90, 70)])

    pygame.display.flip()
    input('waiting ...')
    bench.update_image(to_array('test.jpg'))
    bench.redraw()
    pygame.display.flip()
    input('waiting ...')

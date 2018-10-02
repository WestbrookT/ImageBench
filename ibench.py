

"""
The goal is to create an easy to use image system, to open images, and make certain they're in the correct
shape for use with numpy and or keras. There should be a system to display images easily, and to update the screen.
"""

import pygame, numpy as np, numbers, random
from PIL import Image, ImageEnhance

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
    top_left = (0,0)

    def __init__(self, surface, current_image=None, points=None, center=None):
        """
        Creates an ImageBench object
        :param surface: The location to be drawn to
        :param current_image: An image in the form of a numpy array, a PIL Image, or a pygame surface, or a path string
        :param points: A list of points or point lists
        """
        self.surface = surface
        self.redraw(current_image, points)


    def redraw(self, new_source=None, new_points=None, new_surface=None, top_left=None):
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
        self.update_TL(top_left)

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
        x = x + self.top_left[0]
        y = y + self.top_left[1]
        # x = self.image_center[0] - width // 2 + x
        # y = self.image_center[1] - height // 2 + x

        points = []
        size = 2
        points.append((x-size, y-size))
        points.append((x+size, y-size))
        points.append((x+size, y+size))
        points.append((x-size, y+size))
        points.append((x-size, y-size))
        pygame.draw.lines(self.surface, self.color, True, points, size)
        #print(points)

    def draw_points(self):
        """
        Takes no arguments, it just draws all of the internal points
        :return: None
        """
        if self.points is not None:
            cur_point = []
            flat = False
            for item in self.points:

                if flat and not isinstance(item, numbers.Number):
                    raise Exception('Points mismatch, got a single number for coordinates {}'.format(item))

                if (isinstance(item, tuple) or isinstance(item, list)) and len(item) == 2:
                    self.draw_point(item)
                elif isinstance(item, list):

                    self.draw_lines(item)
                elif isinstance(item, numbers.Number):
                    cur_point.append(item)
                    if len(cur_point) == 2:

                        self.draw_point(tuple(cur_point))
                        cur_point = []
                        flat = False
                    else:
                        flat = True
                else:
                    raise Exception('Invalid type for drawing points')

    def draw_image(self):
        """
        Takes no arguments, just draws the current internal image
        :return: None
        TODO: add the ability to specify the location of the blit
        """

        #self.surface.fill((0, 0, 0))
        if self.current_image is not None:
            image_surface = to_surface(self.current_image) #Converts the internal array to a drawable form (pygame surface)
            # print(self.current_image.shape)
            # pygame.surfarray.blit_array(self.surface, self.current_image)




            # x = self.image_center[0] - width//2
            # y = self.image_center[1] - height//2
            self.surface.blit(image_surface, self.top_left)


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
        if new_points is not None:
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

    def update_TL(self, x=None, y=None):

        if isinstance(x, tuple):
            self.top_left = x
        elif isinstance(x, int) and isinstance(y, int):

            self.top_left = (x, y)
        elif x is None and y is None:
            pass
        else:
            raise Exception("First parameter must be an (x, y) tuple, or both x, and y must be ints, got {}".format(type(x)))

def unflatten(points):

    out_points = []

    for i in range(len(points)):
        if i % 2 == 0:
            point = (points[i], points[i+1])
            out_points.append(point)
        else:
            continue 
    return out_points

def to_array(origin):
    """

    :param origin: Origin should be a PIL image, a path string, or a pygame surface
    :return: A numpy array
    """
    if isinstance(origin, Image.Image):
        """
        Check if the origin is a PIL image
        """
        #print(origin.size)
        #origin = origin.rotate(90, expand=True)
        origin = np.asarray(origin, dtype=np.uint8)
        #print(origin.shape)
        return origin
    elif isinstance(origin, str):
        return to_array(Image.open(origin).convert(mode='RGB'))

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
        raise Exception('Incompatible Type of Object: {}'.format(type(origin)))

def to_PIL(origin):
    if not isinstance(origin, np.ndarray):
        origin = to_array(origin)
    return Image.fromarray(origin)

def to_surface(origin):
    if not isinstance(origin, np.ndarray):
        origin = to_array(origin)
    return pygame.surfarray.make_surface(np.swapaxes(origin, 0, 1))

def rgb_to_grey(array):

    pil_img = to_PIL(array)

    return to_array(pil_img.convert('L'))

def grey_to_rgb(array):
    raise Exception("Not currently implemented")

def softmax_filter(pil_img):
    '''
        If the image passed in is rgb, then every pixel's r g and b values are divided by their sum and multipled by 255
        If the image is greyscale then all values are relative to the min and max pixel values
    :param pil_img:
    :return: numpy array of the image with given transforms
    '''

    pil_img = to_PIL(pil_img)

    if pil_img.mode == 'L':
        pix_min, pix_max = pil_img.getextrema()


        range = pix_max - pix_min


        out_img = pil_img.point(lambda intensity: (intensity-pix_min)/range*255)
        return np.asarray(out_img.convert('RGB'), dtype=np.uint8)
    elif pil_img.mode == 'RGB':


        pixels = pil_img.getdata()
        # bands = np.array(pil_img.getdata()).swapaxes(0, 1)
        #
        # ra = sum(bands[0]) / len(bands[0])
        # ga = sum(bands[1]) / len(bands[1])
        # ba = sum(bands[2]) / len(bands[2])
        #
        # aa = (ra + ga + ba) / 3


        out_pixels = []

        for i, pixel in enumerate(pixels):

            total = sum(pixel)

            r = int(pixel[0] / total * 255)
            g = int(pixel[1] / total * 255)
            b = int(pixel[2] / total * 255)

            out_pixels.append((r, g, b))

        new_image = Image.new(pil_img.mode, pil_img.size)
        new_image.putdata(out_pixels)
        return np.asarray(new_image, dtype=np.uint8)


def flip(origin, points, flat):
    """

    :param origin: Can be an image in array, pil, or surface format
    :param points: List of (x, y) tuples
    :return: A new array of the image, and the new point set
    """

    if flat and isinstance(points[0], int):
        tmp_points = []
        for i, x in enumerate(points):
            if i % 2 == 1:
                continue
            tmp_points.append((x, points[i+1]))
        points = tmp_points

    if not isinstance(origin, Image.Image):
        origin = to_PIL(origin)

    origin = origin.transpose(Image.FLIP_LEFT_RIGHT)
    width, height = origin.size

    out = []
    for i, point in enumerate(points):

        #print('here', point)
        xp, yp = point[0], point[1]

        if xp == 0 and yp == 0:
            pass
        else:
            inside = (xp >= 0 and xp < width) and (yp >= 0 and yp < height)

            xp = (width - xp -1) if inside else 0
        #yp = (height ) if inside else 0
        if flat:
            out.append(xp)
            out.append(yp)
        else:
            out.append((xp, yp))




    return to_PIL(origin), out


def rotate_data(origin, points, angle):

    origin = to_PIL(origin)

    width, height = origin.size

    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    rot_matrix = np.array([[c, -s], [s, c]])

    out_points = np.dot(np.array(points)-(width//2, height//2), rot_matrix)

    out_image = origin.rotate(angle)

    return out_image, (out_points+(width//2, height//2)).tolist()

def crop_data(pil_image, points, size, center=None):


    if not isinstance(pil_image, Image.Image):
        pil_image = to_PIL(pil_image)

    new_width, new_height = int(pil_image.width), int(pil_image.height)

    pil_image = pil_image.resize((new_width, new_height), resample=Image.LANCZOS)

    x = 0
    y = 0
    if center is None:
        x = pil_image.width//2
        y = pil_image.height//2
    else:
        x, y = center

    outimgs = []
    outpoints = []



    left = x - size//2 - size
    right = x + size//2 + size
    top = y - size//2 - size
    bottom = y + size//2 + size

    cropped = pil_image.crop((left, top, right, bottom))

    outimgs.append(cropped)

    curpts = []

    for point in points:

        xp, yp = point
        xp, yp = int(xp), int(yp)

        inside = (xp >= left and xp < right) and (yp >= top and yp < bottom)

        xp = (xp - left) if inside else 0
        yp = (yp - top) if inside else 0
        curpts.append((xp, yp))







    return outimgs[0], curpts


def crop_aug(pilimg, points, crop_size=50, center=None, size=1000, flatten=False, scale=1, intensity_fuzz=.1, flip_image=True, random_drop=0):
    """

    :param pilimg: A pillow image object
    :param points: A list of (x,y) tuples
    :param crop_size: Amount of pixels to crop off
    :param center: The location of the area to crop around
    :param size: The height and width of the end image
    :return: a tuple of two lists, one with the cropped images, another with its corresponding points
    """

    if not isinstance(pilimg, Image.Image):
        pilimg = to_PIL(pilimg)

    new_width, new_height = int(pilimg.width*scale), int(pilimg.height*scale)

    pilimg = pilimg.resize((new_width, new_height), resample=Image.LANCZOS)

    x = 0
    y = 0
    if center is None:
        x = pilimg.width//2
        y = pilimg.height//2
    else:
        x, y = center

    outimgs = []
    outpoints = []




    for xmod in [0, -1, 1]:

        for ymod in [0, -1, 1]:

            if random.random() < random_drop:
                continue


            left = x - size//2 + xmod*crop_size
            right = x + size//2 + xmod*crop_size
            top = y - size//2 + ymod*crop_size
            bottom = y + size//2 + ymod*crop_size

            cropped = pilimg.crop((left, top, right, bottom))

            outimgs.append(to_array(cropped))

            curpts = []

            for point in points:

                xp, yp = point
                xp, yp = int(xp*scale), int(yp*scale)

                inside = (xp >= left and xp < right) and (yp >= top and yp < bottom)

                xp = (xp - left) if inside else 0
                yp = (yp - top) if inside else 0


                if flatten:
                    curpts.append(xp)
                    curpts.append(yp)
                else:
                    curpts.append((xp, yp))
            outpoints.append(curpts)

    if flip_image:
        length = len(outimgs)
        for i, image in enumerate(outimgs):
            if i == length:
                break
            img, newpts = flip(image, outpoints[i], flatten)
            outimgs.append(img)
            outpoints.append(newpts)

    return outimgs, outpoints

def augment_images(img_list, point_list, crop_size=50, center=None, size=1000, flatten=True, scale=1, scale_fuzz=.01,
                   intensity_fuzz=.5, flip_image=False, softmax_grey=False, softmax_normal=False, rotate=True, angle=30,
                   random_drop=0):
    """
    Uses the crop_aug function to create a keras ready dataset
    :param img_list: Can be a list of images in array, pil, or surface format
    :param point_list: List of lists of point tuples (x, y) corresponding to each image
    :return: A tuple (images, points) where images is a numpy array of numpy arrays of images,
                and points is a numpy array of numpy arrays of points
    """
    out_images = []
    out_points = []
    exfuzz = .02

    cropped_images = []
    cropped_points = []



    if rotate:
        length = len(img_list)

        for i in range(length):

            new_image, new_points = rotate_data(img_list[i], point_list[i], angle)
            img_list.append(new_image)
            point_list.append(new_points)

            new_image, new_points = rotate_data(img_list[i], point_list[i], -angle)
            img_list.append(new_image)
            point_list.append(new_points)

            new_image, new_points = rotate_data(img_list[i], point_list[i], angle//2)
            img_list.append(new_image)
            point_list.append(new_points)

            new_image, new_points = rotate_data(img_list[i], point_list[i], -angle//2)
            img_list.append(new_image)
            point_list.append(new_points)

    # (3 * 9) * 5





    print('Length of uncropped set:', len(img_list))
    for i, image in enumerate(img_list):

        if softmax_grey:
            image = softmax_filter(rgb_to_grey(image))
        elif softmax_normal:
            image = softmax_filter(image)

        new_images, new_points = crop_aug(image, point_list[i], crop_size, center, size, flatten, scale, flip_image=flip_image, random_drop=random_drop)

        out_images += new_images
        out_points += new_points

        new_images, new_points = crop_aug(image, point_list[i], crop_size, center, size, flatten, scale+scale_fuzz, flip_image=flip_image, random_drop=random_drop)

        out_images += new_images
        out_points += new_points

        new_images, new_points = crop_aug(image, point_list[i], crop_size, center, size, flatten, scale+scale_fuzz, flip_image=flip_image, random_drop=random_drop)

        out_images += new_images
        out_points += new_points

        new_images, new_points = crop_aug(image, point_list[i], crop_size, center, size, flatten, scale + scale_fuzz + exfuzz,
                                          flip_image=flip_image, random_drop=random_drop)

        out_images += new_images
        out_points += new_points

        new_images, new_points = crop_aug(image, point_list[i], crop_size, center, size, flatten, scale + scale_fuzz + exfuzz,
                                          flip_image=flip_image, random_drop=random_drop)

        out_images += new_images
        out_points += new_points

        # image, pts = flip(image, point_list[i])
        #print(point_list[i], pts)

        # new_images, new_points = crop_aug(image, pts, crop_size, center, size, flatten, scale)
        #
        # out_images += new_images
        # out_points += new_points
    img_list = None
    print('Images in cropped set:', len(out_images))
    length = len(out_images)
    for i in range(length):

        out_images.append(darken(out_images[i], intensity_fuzz))
        out_images.append(lighten(out_images[i], intensity_fuzz))

        out_points.append(out_points[i])
        out_points.append(out_points[i])

    if flatten:
        out_points = np.array(out_points)

    return np.array(out_images), out_points

def darken(image, fuzz):

    image = to_PIL(image)

    enhancer = ImageEnhance.Brightness(image)

    new_image = enhancer.enhance(1-fuzz)

    return to_array(new_image)

def lighten(image, fuzz):
    return darken(image, -fuzz)


def resize(origin, width, height):
    origin_original = origin
    if not isinstance(origin, Image.Image):
        origin = to_PIL(origin)

    origin = origin.resize((width, height), resample=Image.LANCZOS)

    if isinstance(origin_original, Image.Image):
        return origin
    elif isinstance(origin_original, type(pygame.Surface((1,1)))):
        return to_surface(origin)
    elif isinstance(origin_original, np.ndarray):
        return to_array(origin)
    elif isinstance(origin_original, str):
        return to_array(origin)
    else:
        raise Exception('Got {} expected a surface, ndarray, or a pil image, or a str path'.format(type(origin_original)))

def scale_data(origin, points, delta):
    '''
        Expects points to be in form [(x,y), ...]
        delta is a float representing the % size of the original
    '''


    origin = to_PIL(origin)

    out_points = []
    for point in points:
        nx = int(point[0] * delta) 
        ny = int(point[1] * delta) 
        out_points.append((nx, ny))
    
    return resize(origin, int(origin.width*delta), int(origin.height*delta)), out_points



if __name__ == '__main__':
    # to_array(Image.open('test.jpg'))
    # to_array('test.jpg')
    # to_array(pygame.Surface((2,1)))
    #
    # img = Image.open('rgba.png')
    # img.show()
    img = pygame.image.load("face.JPG")

    # input('waiting...')
    # to_PIL(to_array('rgba.png')).show()
    import time

    pygame.init()
    size = w, h = 1500, 1000
    screen = pygame.display.set_mode(size)
    pts = [(300, 300), (600, 600), (900, 700)]

    print(flip(img, pts, False))

    cimgs, cpts = augment_images([img, img], [pts, pts], size=100, crop_size=5, scale=.125)

    bench = ImageBench(screen, img, pts)

    bench.redraw()
    pygame.display.flip()
    input('waiting...')



    img, pts = crop_data(img, pts, 200)
    print(pts)
    bench.redraw(img, pts)
    pygame.display.flip()
    input('waiting')


    print('yar', cpts[0])
    for i in range(len(cimgs)):
        bench.redraw(new_source=cimgs[i], new_points=cpts[i])
        pygame.display.flip()
        time.sleep(2)

def shuffle_examples(inputs, outputs, seed=1):

    np.random.seed(seed)
    print(inputs.shape)
    np.random.shuffle(inputs)
    print(inputs.shape)
    np.random.seed(seed)
    print(outputs.shape)
    np.random.shuffle(outputs)
    print(outputs.shape)



def permute(pathname, points, size=50, rescale=.4, max_angle=10, max_scale=30, max_translate=20):

    # rotate first
    # scale
    # translate
    # crop

    img = to_PIL(pathname)

    img, points = scale_data(img, points, rescale)

    angle = random.randint(-max_angle, max_angle)
    scale = random.randrange(100-max_scale,100+max_scale-10)/100
    flip_bool = random.random() < .5
    

    xc = 0
    yc = 0
    count = 0
    for point in points:
        if point[0] == 0 and point[1] == 0:
            continue
        xc += point[0]
        yc += point[1]
        count += 1
    center = xc/count, yc/count

    center = center[0] + random.randint(-max_translate, max_translate), center[1] + random.randint(-max_translate, max_translate)

    img, points = rotate_data(img, points, angle)
    img, points = scale_data(img, points, scale)
    #img, points = resize(img, int(img.width*scale), int(img.height*scale))
    img, points = crop_data(img, points, size, center=center)

    if flip_bool:
        img, points = flip(img, points, flat=False)

    return img, points


def create_data_generator(pathnames, points, size, batch_size, rescale=.4, max_angle=10, max_scale=30, max_translate=20):

    while True:
        images = []
        out_points = []
        for _ in range(batch_size):
            
            i = random.randint(0, len(pathnames)-1)

            img, ipoints = permute(pathnames[i], points[i], size, rescale, max_angle, max_scale, max_translate)
            images.append(to_array(img))
            out_points.append(np.array(ipoints).flatten())

        if batch_size == 0:
            i = random.randint(0, len(pathnames)-1)
            img, ipoints = permute(pathnames[i], points[i], size, rescale, max_angle, max_scale, max_translate)
            images.append(to_array(img))
            out_points.append(ipoints)
            yield np.array(images)[0], out_points[0]

        yield np.array(images), np.array(out_points)
    

def create_dataset(pathnames, points, size, count, rescale=.4, max_angle=10, max_scale=30, max_translate=20):

    images = []
    out_points = []
    for _ in range(count):
        
        i = random.randint(0, len(pathnames)-1)


        try:
            img, ipoints = permute(pathnames[i], points[i], size, rescale, max_angle, max_scale, max_translate)
            
            if ipoints[0][0] == 0 and ipoints[0][1] == 0:
                #print(ipoints)
                continue

        except IndexError:
            print(len(pathnames), len(points), i)
            exit()
        images.append(to_array(img))
        out_points.append(np.array(ipoints).flatten())

    if count == 0:
        i = random.randint(0, len(pathnames)-1)
        try:
            img, ipoints = permute(pathnames[i], points[i], size, rescale, max_angle, max_scale, max_translate)
            iters = 0
            while ipoints[0][0] == 0 and ipoints[0][1] == 0:
                #print(ipoints)
                img, ipoints = permute(pathnames[i], points[i], size, rescale, max_angle, max_scale, max_translate)
                iters += 1
                if iters > 100:
                    break
        except IndexError:
            print(len(pathnames), len(points), i)
            exit()
        images.append(to_array(img))
        out_points.append(ipoints)
        return np.array(images)[0], out_points[0]

    X = np.array(images)
    y = np.array(out_points)

    shuffle_examples(X, y)

    return X, y
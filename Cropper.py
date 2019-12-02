from PIL import Image, ImageOps
import os


class Cropper:
    def __init__(self, image):
        self._image: Image = Image.open(image)

    def crop(self, x, y, width, height):
        """
        Method crop image by predefined offsets and size
        :param x: offset left
        :param y: offset top
        :param width: right corner
        :param height: bottom corner
        :return: Cropper
        """
        self._image = self._image.crop((x, y, width, height))
        return self

    def resize(self, width, height):
        """
        Resize image
        :param width:
        :param height:
        :return: Cropper
        """
        self._image = self._image.resize((width, height), Image.ANTIALIAS)
        return self

    def add_border(self, thickness, color):
        """
        Add border to image
        :param thickness: border width in pixels
        :param color: border color
        :return: Cropper
        """
        self._image = self._image.resize((self._image.width - thickness * 5, self._image.height - thickness * 5),
                                         Image.ANTIALIAS)
        self._image = ImageOps.expand(self._image, border=thickness, fill=color)
        return self

    def crop_center(self, width, height):
        """
        Scale image to height and width by small side and cut off piece of image that not fit in predefined box size
        :param width:
        :param height:
        :return: Cropper
        """
        # self._image.thumbnail((width, height), Image.ANTIALIAS)
        self._image = ImageOps.fit(self._image, (width, height), Image.ANTIALIAS)
        return self

    def fit_to_container(self, width, height):
        """
        Put image into center of box and fit it by largest side
        :param width:
        :param height:
        :return: Cropper
        """
        #self._image.thumbnail((width, height), Image.ANTIALIAS)
        if self._image.height / self._image.width < height / width:
            self._image = self._image.resize((width, int(width / self._image.width * self._image.height)),
                                             Image.ANTIALIAS)
        elif self._image.height / self._image.width > height / width:
            self._image = self._image.resize((int(height / self._image.height * self._image.width), height),
                                             Image.ANTIALIAS)

        blank_image = Image.new('RGB', (width, height), (255, 255, 255))
        blank_image.paste(self._image, (int((blank_image.width - self._image.width) / 2),
                                        int((blank_image.height - self._image.height) / 2)))
        self._image = blank_image
        return self

    def save(self, path, filename):
        """
        Save image on disk
        :param path:
        :param filename:
        :return: Cropper
        """
        if not os.path.exists(path):
            os.makedirs(path)
        self._image.save(os.path.join(path, filename))

    def start_processing(self):
        self.crop_center(500, 500).fit_to_container(500, 500).add_border(10, "#acbdab").save('uploads', "testxx.jpg")

from PIL import Image

class ImageConverter:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.image = Image.open(input_path)

    def convert(self, output_format, quality=95):
        """
        Converts the image to the specified format.
        """
        # RGBA -> RGB for JPEG
        if output_format.upper() == 'JPEG' and self.image.mode == 'RGBA':
            self.image = self.image.convert('RGB')
            
        self.image.save(self.output_path, format=output_format, quality=quality)

    def resize(self, width, height, keep_aspect_ratio=True):
        """
        Resizes the image.
        """
        if keep_aspect_ratio:
            self.image.thumbnail((width, height))
        else:
            self.image = self.image.resize((width, height))

    def rotate(self, angle):
        """
        Rotates the image.
        """
        self.image = self.image.rotate(angle, expand=True)

    def flip(self, direction):
        """
        Flips the image.
        """
        if direction == 'horizontal':
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
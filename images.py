import base64
import io
import textwrap
from typing import Optional

from PIL import Image, ImageFont, ImageDraw
from faker import Faker

from constants import IMAGES_DIR


def create_image(
    title: str,
    font_size: int,
    font_file: str,
    x_size: int,
    y_size: int,
    text: str = None,
) -> Image:
    """
    The create_image function creates a new image with the given title, font
    size, and font file. It also takes in an x_size and y_size to determine
    the dimensions of the image. The function returns an Image object that can
    be saved as a .png or .jpg file.

    :param title: str: Specify the title of the image
    :param font_size: int: Set the size of the font
    :param font_file: str: Specify the font file to use
    :param x_size: int: Specify the width of the image
    :param y_size: int: Determine the height of the image
    :param text: str: Add text to the image
    :return: The image object
    """
    img = Image.new('RGB', (x_size, y_size), color='white')
    draw = ImageDraw.Draw(img)
    title = title.upper()
    title_color, text_color = get_random_colors()

    draw_title(title, img, draw, font_file, font_size, title_color)
    if text:
        draw_text(text, img, draw, font_file, font_size, text_color)

    return img


def get_random_colors() -> tuple:
    """
    The get_random_colors function returns a tuple of two random colors.

    :return: A tuple of two random colors
    """
    faker = Faker()
    return faker.color(), faker.color()


def save_image_to_disk(img: Image, title: str, format: str = 'PNG') -> None:
    """
    The save_image_to_disk function saves an image to disk.

    :param img: Image: Specify the type of the parameter
    :param title: str: Name the image file
    :param format: str: Specify the file format
    :return: None, because it has no return statement
    """
    filename = f"{title}.{format.lower()}"
    IMAGES_DIR.mkdir(exist_ok=True)
    img.save(IMAGES_DIR / filename, format=format)


def encode_image(img: Image, format: str = 'PNG') -> str:
    """The encode_image function takes an image and returns a string that can
    be used in HTML to display the image.

    :param img: Image: Specify the image that is to be encoded
    :param format: str: Specify the format of the image
    :return: A string
    """
    buffered = io.BytesIO()
    img.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/{format.lower()};base64,{img_str}"


def gen_image(
    title: str,
    font_size=80,
    font='arial',
    x_size=500,
    y_size=500,
    to_file=False,
    format='PNG',
    text=None,
) -> Optional[str]:
    """
    The gen_image function creates an image with the given title, font size,
    font type, x and y sizes. The function can either save the image to disk or
    return a base64 encoded string of the image.

    :param title: str: Name the image
    :param font_size: Set the size of the font used in the image
    :param font: Specify the font to use when generating the image
    :param x_size: Set the width of the image
    :param y_size: Set the height of the image
    :param to_file: Determine whether the image should be saved to disk or returned as a string
    :param format: Specify the format of the image
    :param text: Specify the text to be displayed on the image
    :param : Specify the title of the image
    :return: Either a string or none
    """
    img = create_image(title, font_size, font, x_size, y_size, text)

    if to_file:
        save_image_to_disk(img, title, format=format)
    else:
        return encode_image(img, format=format)


def get_title_position(img_size: tuple, title_size: tuple) -> tuple:
    """
    The get_title_position function takes in the size of an image and the size of a title,
    and returns a tuple containing the x and y coordinates for where to place that title on top
    of that image. The x coordinate is calculated by taking half of the difference between
    the widths of both images, so that it will be centered horizontally. The y coordinate is
    calculated by taking half of the difference between their heights, then subtracting one-fourth
    of their height from this value so that it will be placed above center vertically.

    :param img_size: tuple: Get the size of the image that we are going to put text on
    :param title_size: tuple: Get the size of the title text
    :return: The x and y coordinates of the title
    """
    x = (img_size[0] - title_size[0]) // 2
    y = (img_size[1] - title_size[1]) // 2 - img_size[1] // 4
    return x, y


def get_text_position(img_size: tuple, text_size: tuple) -> tuple:
    """
    The get_text_position function takes in the size of an image and the size of a text,
    and returns a tuple containing x and y coordinates for where to place the text.
    The x coordinate is calculated by taking half of the difference between
    the widths of both images. The y coordinate is calculated by taking half
    of the difference between heights, plus one fourth height.

    :param img_size: tuple: Get the width and height of the image
    :param text_size: tuple: Get the size of the text
    :return: The x and y coordinates of the text
    """
    x = (img_size[0] - text_size[0]) // 2
    y = (img_size[1] - text_size[1]) // 2 + img_size[1] // 4
    return x, y


def draw_title(
    title: str,
    img: Image,
    draw: ImageDraw,
    font_file: str,
    font_size: int,
    color: str,
) -> None:
    """
    The draw_title function draws a title on an image.

    :param title: str: Specify the title that will be drawn
    :param img: Image: Get the image size
    :param draw: ImageDraw: Draw on the image
    :param font_file: str: Specify the font file to use
    :param font_size: int: Set the font size of the title
    :param color: str: Set the color of the title text
    :return: None, but we can still use the draw object to
    """
    font = get_font(font_file, font_size)
    *_, text_width, text_height = draw.textbbox((0, 0), title, font=font)
    x, y = get_title_position(img.size, (text_width, text_height))
    draw.text((x, y), title, font=font, fill=color)


def draw_text(
    text: str,
    img: Image,
    draw: ImageDraw,
    font_file: str,
    font_size: int,
    color: str,
) -> None:
    """
    The draw_text function takes in a string of text, an image object,
    a draw object, the path to a font file (as a string), the size of
    the font (as an int), and the color of the text. It then returns None.
    The function first creates a new ImageFont object using get_font() with
    the given font file and 1/3rd of its size as arguments. Then it uses
    textwrap to wrap lines at 24 characters each and joins them together with \n's.

    :param text: str: Specify the text to be drawn
    :param img: Image: Get the size of the image
    :param draw: ImageDraw: Draw the text on the image
    :param font_file: str: Specify the font file to be used
    :param font_size: int: Set the size of the font
    :param color: str: Specify the color of the text
    :return: None
    """
    font = get_font(font_file, round(font_size / 3))
    text = '\n'.join(textwrap.wrap(text, width=24))
    *_, text_width, text_height = draw.textbbox((0, 0), text, font=font)
    x, y = get_text_position(img.size, (text_width, text_height))

    draw.text((x, y), text, font=font, fill=color)


def get_font(font_file: str, font_size: int):
    """
    The get_font function takes a font file and size as arguments,
    and returns an ImageFont object. If the font file cannot be loaded,
    it will return the default system font instead.

    :param font_file: str: Specify the font file to be used
    :param font_size: int: Set the size of the font
    :return: A pil
    """
    try:
        return ImageFont.truetype(font_file, font_size)
    except OSError:
        print(f"Error: Could not load font file '{font_file}'")
        return ImageFont.load_default()

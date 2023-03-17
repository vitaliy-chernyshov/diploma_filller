import base64
import io
from typing import Optional

from PIL import Image, ImageFont, ImageDraw

from constants import IMAGES_DIR


def create_image(title: str, font_size: int, font: str, color: tuple[int, int, int], x_size: int, y_size: int) -> Image:
    img = Image.new('RGB', (x_size, y_size), color=color)
    font = ImageFont.truetype(font, font_size)
    draw = ImageDraw.Draw(img)
    *_, text_width, text_height = draw.textbbox((0, 0), title, font=font)
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 16
    draw.text((x, y), title, font=font, fill=(0, 0, 0))
    return img


def save_image_to_disk(img: Image, title: str, format: str = 'PNG') -> None:
    filename = f"{title}.{format.lower()}"
    IMAGES_DIR.mkdir(exist_ok=True)
    img.save(IMAGES_DIR / filename, format=format)


def encode_image(img: Image, format: str = 'PNG') -> str:
    buffered = io.BytesIO()
    img.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/{format.lower()};base64,{img_str}"


def gen_image(
        title: str,
        font_size=50,
        font='arial',
        color=(255, 255, 255),
        x_size=500,
        y_size=500,
        to_file=False,
        format='PNG'
) -> Optional[str]:
    """
    The gen_image function takes in a string, and generates an image with the
    text centered. The function also takes in optional parameters for font size,
    font type, background color (default white), and x and y sizes of the image
    (default 500x500). The function saves the generated images to a folder
    called 'images'

    :param title: str: Pass in the text that will be used to generate the image
    :param font_size: Set the size of the text
    :param font: Set the font of the text
    :param color: Set the background color of the image
    :param x_size: Set the width of the image
    :param y_size: Set the height of the image
    :param to_file: Whether to save the image to disk or not
    :param format: The image format to use (default PNG)
    :return: Optional[str]
    """
    img = create_image(title, font_size, font, color, x_size, y_size)

    if to_file:
        save_image_to_disk(img, title, format=format)
    else:
        return encode_image(img, format=format)

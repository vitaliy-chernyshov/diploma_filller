import base64
import io
import textwrap
from typing import Optional

from PIL import Image, ImageFont, ImageDraw
from faker import Faker

from constants import IMAGES_DIR


def create_image(title: str, font_size: int, font_file: str,
                 x_size: int, y_size: int, text: str = None) -> Image:
    img = Image.new('RGB', (x_size, y_size), color='white')
    draw = ImageDraw.Draw(img)
    title = title.upper()
    title_color, text_color = get_random_colors()

    draw_title(title, img, draw, font_file, font_size, title_color)
    if text:
        draw_text(text, img, draw, font_file, font_size, text_color)

    return img


def get_random_colors() -> tuple:
    faker = Faker()
    return faker.color(), faker.color()


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
        font_size=80,
        font='arial',
        x_size=500,
        y_size=500,
        to_file=False,
        format='PNG',
        text=None,
) -> Optional[str]:
    img = create_image(title, font_size, font, x_size, y_size, text)

    if to_file:
        save_image_to_disk(img, title, format=format)
    else:
        return encode_image(img, format=format)


def get_title_position(img_size: tuple, title_size: tuple) -> tuple:
    x = (img_size[0] - title_size[0]) // 2
    y = (img_size[1] - title_size[1]) // 2 - img_size[1] // 4
    return x, y


def get_text_position(img_size: tuple, text_size: tuple) -> tuple:
    x = (img_size[0] - text_size[0]) // 2
    y = (img_size[1] - text_size[1]) // 2 + img_size[1] // 4
    return x, y


def draw_title(title: str, img: Image, draw: ImageDraw, font_file: str,
               font_size: int, color: str) -> None:
    font = get_font(font_file, font_size)
    *_, text_width, text_height = draw.textbbox((0, 0), title, font=font)
    x, y = get_title_position(img.size, (text_width, text_height))
    draw.text((x, y), text, font=font, fill=color)


def draw_text(text: str, img: Image, draw: ImageDraw, font_file: str,
              font_size: int, color: str) -> None:
    font = get_font(font_file, round(font_size / 3))
    text = '\n'.join(textwrap.wrap(text, width=24))
    *_, text_width, text_height = draw.textbbox((0, 0), text, font=font)
    x, y = get_text_position(img.size, (text_width, text_height))

    draw.text((x, y), text, font=font, fill=color)


def draw_text_with_font(text: str, draw: ImageDraw,
                        font: ImageFont.FreeTypeFont, color: str,
                        position: tuple) -> None:
    draw.text(position, text, font=font, fill=color)


def get_font(font_file: str, font_size: int):
    try:
        return ImageFont.truetype(font_file, font_size)
    except OSError:
        print(f"Error: Could not load font file '{font_file}'")
        return ImageFont.load_default()


if __name__ == '__main__':
    faker = Faker()
    text = faker.sentence(nb_words=4, variable_nb_words=False)
    gen_image('title', text=text, to_file=True)
    print(text)

import asyncio
import random

import aiohttp
from faker import Faker
from tqdm import tqdm

from api import post_recipe, create_user, get_token, get_all_tags, get_all_ingredients
from constants import RECIPES_NUMBER
from images import gen_image
from models import User


async def create_json_for_recipe(
        recipe_name,
        session,
        ingredients=None,
        tags=None,
        ingredients_count=4):
    """
    The create_json_for_recipe function creates a JSON object for a recipe.

    :param recipe_name: Generate the name of the recipe
    :param ingredients: Specify the ingredients for a recipe
    :param tags: Specify the tags that should be added to the recipe
    :param ingredients_count: Specify how many ingredients a recipe should have
    :return: A dictionary
    """
    if tags is None:
        tags = [tag['id'] for tag in random.choices(await get_all_tags(session))]
    if ingredients is None:
        ingredients = random.choices(await get_all_ingredients(session), k=ingredients_count)

    recipe_text = ' '.join([random.choice(ingredient['name'].split())
                            for ingredient in ingredients])
    json = dict(
        ingredients=[{**ingredient, 'amount': random.randint(1, 100)}
                     for ingredient in ingredients],
        tags=tags,
        name=recipe_name,
        text=recipe_text,
        image=gen_image(title=recipe_name, text=recipe_text),
        cooking_time=random.randint(1, 100))
    return json


def create_random_person():
    faker = Faker(['ru-ru'])
    json = dict(
        email=faker.email(),
        username=faker.user_name(),
        first_name=faker.first_name_male(),
        last_name=faker.last_name_male(),
        password=faker.password()

    )
    return json


async def main(RECIPES_NUMBER):
    async with aiohttp.ClientSession() as session:
        user = User(**create_random_person())
        await create_user(user, session)
        token = await get_token(user, session)
        all_ingredients = await get_all_ingredients(session)
        all_tags = await get_all_tags(session)
        tasks = []
        for i in tqdm(range(RECIPES_NUMBER)):
            recipe_name = f'recipe_{i}'
            ingredients = random.choices(all_ingredients, k=5)
            tags = [tag['id'] for tag in random.choices(all_tags, k=len(all_tags) // 2)]
            json = await create_json_for_recipe(recipe_name, session, ingredients, tags)
            task = asyncio.ensure_future(post_recipe(token, json, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main(RECIPES_NUMBER))

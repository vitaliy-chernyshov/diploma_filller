import asyncio
import logging
import random

import aiohttp
from faker import Faker
from tqdm import tqdm

from api import (
    post_recipe,
    create_user,
    get_token,
    get_all_tags,
    get_all_ingredients,
)
from constants import RECIPES_NUMBER
from exceptions import DatabaseLookupError
from images import gen_image
from models import User


async def create_json_for_recipe(
    recipe_name, session, ingredients=None, tags=None, ingredients_count=4
):
    """
    The create_json_for_recipe function creates a JSON object for a recipe.

    :param recipe_name: Generate a random recipe name
    :param session: Make sure that the session is not closed
    :param ingredients: Pass in a list of ingredients to be used for the recipe
    :param tags: Specify which tags should be assigned to the recipe
    :param ingredients_count: Specify the number of ingredients
    :return: A dictionary with the following keys:
    """
    if tags is None:
        tags = [
            tag['id'] for tag in random.sample(await get_all_tags(session), k=1)
        ]
    if ingredients is None:
        ingredients = random.sample(
            await get_all_ingredients(session), k=ingredients_count
        )

    recipe_text = ' '.join(
        [
            random.choice(ingredient['name'].split())
            for ingredient in ingredients
        ]
    )
    json = dict(
        ingredients=[
            {**ingredient, 'amount': random.randint(1, 100)}
            for ingredient in ingredients
        ],
        tags=tags,
        name=recipe_name,
        text=recipe_text,
        image=gen_image(title=recipe_name, text=recipe_text),
        cooking_time=random.randint(1, 100),
    )
    return json


def create_random_person():
    """
    function creates a random person with the following attributes:
        email, username, first_name, last_name and password.


    :return: A dictionary
    """
    faker = Faker(['ru-ru'])
    json = dict(
        email=faker.email(),
        username=faker.user_name(),
        first_name=faker.first_name_male(),
        last_name=faker.last_name_male(),
        password=faker.password(),
    )
    return json


async def main(recipes_number: int):
    """
    The main function creates a user, gets the token for that user,
    gets all ingredients and tags from the database. Then it creates
    a list of tasks to post recipes with random names and random
    ingredients/tags. The number of recipes is specified by RECIPES_NUMBER.

    :param recipes_number: Specify the number of recipes to be created
    :return: A coroutine which is a future-like object
    """
    async with aiohttp.ClientSession() as session:
        user = User(**create_random_person())
        await create_user(user, session)
        token = await get_token(user, session)

        all_ingredients = await get_all_ingredients(session)
        if not all_ingredients:
            raise DatabaseLookupError('No ingredients found in database')

        all_tags = await get_all_tags(session)
        if not all_tags:
            raise DatabaseLookupError('No tags found in database')

        tags_used = 1 if len(all_tags) == 1 else len(all_tags) // 2
        tasks = []
        for i in tqdm(range(recipes_number)):
            recipe_name = f'recipe_{i}'
            ingredients = random.sample(all_ingredients, k=5)
            tags = [
                tag['id']
                for tag in random.sample(all_tags, k=tags_used)
            ]
            recipe = await create_json_for_recipe(
                recipe_name, session, ingredients, tags
            )
            task = asyncio.ensure_future(post_recipe(token, recipe, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    try:
        asyncio.run(main(RECIPES_NUMBER))
    except DatabaseLookupError as error:
        logger.error(msg=error)
    else:
        logger.info(f"All {RECIPES_NUMBER} recipes were created successfully.")

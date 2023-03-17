import random
from dataclasses import asdict, dataclass
from urllib.parse import urljoin

import requests
from faker import Faker
from tqdm import tqdm

from constants import API_URL
from images import gen_image


@dataclass
class User:
    username: str
    username: str
    password: str
    email: str
    first_name: str
    last_name: str


def create_user(user: User):
    """
    The create_user function takes a User object and creates it in the database.
    It returns nothing.

    :param user: User: Specify the type of the parameter
    :return: A response object
    """
    response = requests.post(url=(API_URL + 'users/'), json=asdict(user))
    response.raise_for_status()


def get_token(user: User) -> str:
    """
    The get_token function takes a User object and returns an auth_token string.
    The function makes a POST request to the /api/auth/token/login endpoint
    with the User object as JSON data. The response is checked for errors,
    and if none are found, the auth_token is returned.

    :param user: User: Specify the type of object that is passed to the function
    :return: The token for the user
    """
    response = requests.post(url=urljoin(API_URL, '/api/auth/token/login/'),
                             json=asdict(user))
    response.raise_for_status()
    return response.json().get('auth_token')


def get_all_ingredients() -> list[dict]:
    """
    returns a list of all ingredients in the database.

    :return: A list of dictionaries
    """
    response = requests.get(urljoin(API_URL, '/api/ingredients/'))
    response.raise_for_status()
    return response.json()


def get_all_tags() -> list[dict]:
    """Returns a list of all tags in the database.

    :return: A list of dictionaries"""
    response = requests.get(urljoin(API_URL, '/api/tags/'))
    response.raise_for_status()
    return response.json()


def create_json_for_recipe(
        recipe_name,
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
        tags = [tag['id'] for tag in random.choices(get_all_tags())]
    if ingredients is None:
        ingredients = random.choices(get_all_ingredients(), k=ingredients_count)

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


def post_recipe(token, json):
    """
    The post_recipe function takes a token and json as arguments.
    The function then creates headers with the token and content type,
    and posts the recipe to the API using requests.post().

    :param token: Authenticate the user
    :param json: Pass the recipe data to the api
    :return: A json object containing the recipe

    """

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(urljoin(API_URL, '/api/recipes/'),
                             headers=headers, json=json)
    response.raise_for_status()
    return response.json()


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


if __name__ == '__main__':

    user = User(**create_random_person())
    create_user(user)
    token = get_token(user)
    all_ingredients = get_all_ingredients()
    all_tags = get_all_tags()

    for i in tqdm(range(20)):
        recipe_name = f'recipe_{i}'
        ingredients = random.choices(all_ingredients, k=5)
        tags = [tag['id'] for tag in random.choices(all_tags, k=len(all_tags) // 2)]
        json = create_json_for_recipe(recipe_name, ingredients, tags)
        post_recipe(token, json)

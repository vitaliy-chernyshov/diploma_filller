from dataclasses import asdict
from urllib.parse import urljoin

from constants import API_URL
from models import User


async def get_token(user: User, session) -> str:
    """The get_token function takes a user object and a session object as
    arguments. It then converts the user to JSON, and sends it to the API's
    auth/token/login endpoint. If successful, it returns an authentication token.

    :param user: User: Pass the user object to the function
    :param session: Pass the session object to the function
    :return: A token that can be used to authenticate with the api
    """
    json = asdict(user)
    async with session.post(
        urljoin(API_URL, 'auth/token/login/'), json=json
    ) as response:
        response.raise_for_status()
        json = await response.json()
        return json.get('auth_token')


async def create_user(user: User, session):
    """The function creates a new user in the database.

    :param user: User: Pass in the user object that we want to create
    :param session: Make the request
    :return: A response object
    """
    json = asdict(user)
    async with session.post(urljoin(API_URL, 'users/'), json=json) as response:
        response.raise_for_status()


async def get_all_ingredients(session) -> list[dict]:
    """The get_all_ingredients function returns a list of all ingredients in
    the database.

    :param session: Make the request to the api
    :return: A list of dictionaries
    """
    async with session.get(urljoin(API_URL, 'ingredients/')) as response:
        response.raise_for_status()
        return await response.json()


async def get_all_tags(session) -> list[dict]:
    """The function returns a list of dictionaries containing all tags in the
    database.

    :param session: Make the request to the api
    :return: A list of dictionaries
    """
    async with session.get(urljoin(API_URL, 'tags/')) as response:
        response.raise_for_status()
        return await response.json()


async def post_recipe(token, json, session):
    """The post_recipe function takes a token, json, and session as arguments.
    It then creates a headers dictionary with the Authorization key set to
    Token {token} and the Content-Type key set to application/json. It then
    uses an async with statement to post the 'recipes/').
    The response is raised for status and returned as await response.json().

    :param token: Authenticate the user
    :param json: Pass the recipe data to the api
    :param session: Make the request
    :return: The recipe object
    """
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
    }
    async with session.post(
        urljoin(API_URL, 'recipes/'), headers=headers, json=json
    ) as response:
        response.raise_for_status()
        return await response.json()

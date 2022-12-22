"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
import os
import requests
import db.bot_info as bi
import db.reviews as rev
import db.user as usr
import sys
from flask import Flask, request
from flask_restx import Resource, Api, fields
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv
# need an add bot endpoint to add to cart as well as a delete user endpoint


app = Flask(__name__)
api = Api(app)


sys.path.append('../')


LIST = '/listbots'
LISTBOTS = 'Data'
SHOWBOTDETAILS = '/show_bot_details'
SHOWBOTIDS = '/show_bot_ids'
BOTIDS = 'Data'
BOTMETADATA = 'Data'


SHOWREVIEW = '/show_review'
REVIEW = 'Data'
CREATEREVIEW = '/add_review'
DELETEREVIEW = '/delete_review'
UPDATEREVIEW = '/update_review'

CREATEUSER = '/create_user'
SHOWUSERS = '/show_users'
USERLIST = 'Data'
UPDATEUSER = '/update_user'
DELETEUSER = '/delete_user'


MOVIERW = '/moviereview'
MOVIERWRESPONSE = 'response'
NEWS = '/news'
NEWSRESPONSE = 'response'


CRYPTOPRICE = '/crypto'
CRYPTOPRICERESPONSE = 'response'

MAIN_MENU_ROUTE = '/main_menu'
MAIN_MENU_NM = 'Coldbrew Bot Menu'

load_dotenv()
COIN_API = os.getenv('COINMARKETCAP_API_KEY')
COIN_URL = os.getenv('CMC_URL')
PRICE = 'crypto_price'


@api.route(f'{CRYPTOPRICE}/<symbol>')
class CryptoPrice(Resource):
    pass


@api.route(f'{MOVIERW}/<movie_name>')
class MovieReview(Resource):
    """
    Endpoint description
    """
    def get(self, movie_name):
        """
        Returns
        """
        nyt_api_1 = "https://api.nytimes.com"
        nyt_api_2 = "/svc/movies/v2/reviews/search.json?query="
        nyt_api_3 = "&api-key=ydFNAxCapwZOAgyxQ9cPIkacUTD8QnWx"

        try:
            url = nyt_api_1 + nyt_api_2 + movie_name + nyt_api_3
            response = requests.get(url)
            print(response.json())

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return {MOVIERWRESPONSE: response.json()}


@api.route(f'{NEWS}/<keyword>')
class News(Resource):
    """
    Endpoint description
    """
    def get(self, keyword):
        """
        Returns
        """
        nyt_api_1 = "https://api.nytimes.com"
        nyt_api_2 = "/svc/search/v2/articlesearch.json?q="
        nyt_api_3 = "&api-key=ydFNAxCapwZOAgyxQ9cPIkacUTD8QnWx"
        try:
            url = nyt_api_1 + nyt_api_2 + keyword + nyt_api_3
            response = requests.get(url)
            print(response.json())

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return {NEWSRESPONSE: response.json()}


@api.route(LIST)
class ListBot(Resource):
    """
    This will get a list of bot names
    """
    def get(self):
        """
        Returns a list of bot names
        """
        return {'Data': bi.get_bot_names(),
                'Type': 'Data', 'Title': 'Bot Names'}


@api.route(SHOWBOTDETAILS)
class ShowBotDetails(Resource):
    """
    This will get a list of bot descriptions
    """
    def get(self):
        """
        Returns a list of bot descriptions
        """
        return {'Data': bi.get_bot_descs(),
                'Type': 'Data', 'Title': 'Bot Descriptions'}


@api.route(SHOWBOTIDS)
class ShowBotIDs(Resource):
    """
    This will get a list of bot ids
    """

    def get(self):
        """
        Returns a list of bot ids
        """
        return {BOTIDS: bi.get_bot_ids(),
                'Type': 'Data', 'Title': 'Bot IDs'}


@api.route(SHOWREVIEW)
class ShowReview(Resource):
    """
    This will get a json object of bot reviews
    """
    def get(self):
        """
        Returns a json of all bot reviews
        """
        return {'Data': rev.get_all_reviews(),
                'Type': 'Data', 'Title': 'Review'}


review_fields = api.model('NewReview', {
    rev.BOT_NAME: fields.String,
    rev.RATING: fields.Integer,
    rev.COMMENT: fields.String,
    rev.USERNAME: fields.String,
})
@api.route(CREATEREVIEW)
class CreateReview(Resource):
    """
    Add a review
    """
    @api.expect(review_fields)
    def post(self):
        """
        Returns nothing, posts review to database.
        """
        print(f'{request.json=}')
        rev.create_review(request.json)


@api.route(DELETEREVIEW)
class DeleteReview(Resource):
    """
    Deletes a review
    """
    @api.expect(review_fields)
    def post(self):
        """
        Returns nothing, deletes review on database.
        """
        print(f'{request.json=}')
        rev.delete_review(request.json)


@api.route(UPDATEREVIEW)
class UpdateReview(Resource):
    """
    Updates review on database
    """
    @api.expect(review_fields)
    def post(self):
        """
        Returns nothing, updates review on database.
        """
        print(f'{request.json=}')
        username = request.json[rev.USERNAME]
        bot_name = request.json[rev.BOT_NAME]
        new_comment = request.json[rev.COMMENT]
        rev.update_review(username, bot_name, new_comment)


user_fields = api.model('NewUser', {
    usr.USERNAME: fields.String,
    usr.PASSWORD: fields.String,
    usr.EMAIL: fields.String,
    usr.FIRST_NAME: fields.String,
    usr.LAST_NAME: fields.String,
    usr.CART: fields.List(fields.String)
})
@api.route(CREATEUSER)
class CreateUser(Resource):
    """
    Add a new user
    """
    @api.expect(user_fields)
    def post(self):
        """
        Returns nothing, adds a new user on database.
        """
        print(f'{request.json=}')
        usr.create_user(request.json)


@api.route(SHOWUSERS)
class UserList(Resource):
    """
    Shows a list of users
    """
    def get(self):
        """
        Returns a list of usernames
        """
        return {'Data': {'Users':
                [temp for temp in usr.get_users_dict().keys()]},
                'Type': 'Data', 'Title': 'User List'}


@api.route(UPDATEUSER)
class UpdateUser(Resource):
    """
    Updates user password information on database
    """
    @api.expect(user_fields)
    def post(self):
        """
        Returns nothing, updates user information on database
        """
        username = request.json[usr.USERNAME]
        password = request.json[usr.PASSWORD]
        usr.update_user(username, password)


@api.route(DELETEUSER)
class DeleteUser(Resource):
    """
    Deletes a User
    """
    @api.expect(user_fields)
    def post(self):
        """
        Returns nothing, deletes user on database.
        """
        print(f'{request.json=}')
        usr.delete_user(request.json)


@api.route(MAIN_MENU_ROUTE)
class MainMenu(Resource):
    """
    Our Main Menu
    """
    def get(self):
        """
        Returns a json object for the Main Menu
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 1,
                'Choices': {
                    '1': {'url': SHOWBOTDETAILS, 'method': 'get',
                          'text': 'List Bots'},
                    '2': {'url': SHOWBOTIDS, 'method': 'get',
                          'text': 'List Bots IDS'},
                    '3': {'url': SHOWUSERS,
                          'method': 'get', 'text': 'List Users'},
                    'X': {'text': 'Exit'},
                }}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = ''
        return {"Available endpoints": endpoints}

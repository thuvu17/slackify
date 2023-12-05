"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields

import werkzeug.exceptions as wz

import data.songs as songs
import data.users as users

app = Flask(__name__)
api = Api(app)

DELETE = 'delete'
DEFAULT = 'Default'
MENU = 'menu'
SONG_ID = 'Song ID'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'

# EP names
MAIN_MENU_NM = "Welcome to Slackify!"
USER_MENU_NM = 'User Menu'
SONG_MENU_NM = 'Song Menu'
HELLO_RESP = 'hello'

# Endpoints
HELLO_EP = '/hello'
MAIN_MENU_EP = '/MainMenu'
USERS_EP = '/users'
SONGS_EP = '/songs'
DEL_USER_EP = f'{USERS_EP}/{DELETE}'
USER_MENU_EP = '/user_menu'
DEL_SONG_EP = f'{SONGS_EP}/{DELETE}'
SONG_MENU_EP = '/song_menu'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


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
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(f'{MAIN_MENU_EP}')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main SONG menu.
        """
        return {TITLE: MAIN_MENU_NM,
                DEFAULT: 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Available Characters'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Active Songs'},
                    '3': {'url': f'{SONGS_EP}',
                          'method': 'get', 'text': 'List Songs'},
                    '4': {'url': '/',
                          'method': 'get', 'text': 'Illustrating a Point!'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'{USER_MENU_EP}')
class UserMenu(Resource):
    """
    This will deliver our user menu.
    """
    def get(self):
        """
        Gets the user menu.
        """
        return {
                   TITLE: USER_MENU_NM,
                   DEFAULT: '0',
                   'Choices': {
                       '1': {
                            'url': '/',
                            'method': 'get',
                            'text': 'Get User Details',
                       },
                       '0': {
                            'text': 'Return',
                       },
                   },
               }


user_fields = api.model('NewUser', {
    users.NAME: fields.String,
    users.EMAIL: fields.String,
})


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all songs.
    """
    def get(self):
        """
        This method returns all users.
        """
        # return users.get_users()
        return {
           TYPE: DATA,
           TITLE: 'Current Songs',
           DATA: users.get_users(),
           MENU: USER_MENU_EP,
           RETURN: MAIN_MENU_EP,
        }

    @api.expect(user_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user.
        """
        name = request.json[users.NAME]
        email = request.json[users.EMAIL]
        new_user = {
            'name': name,
            'email': email,
        }
        try:
            user_added = users.add_user(new_user)
            if not user_added:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'User added': f'{user_added}'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_USER_EP}/<email>')
class DelUser(Resource):
    """
    Deletes a user by email.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, email):
        """
        Deletes a user by name and artist.
        """
        try:
            users.del_user(email)
            return {'User with email ' + f'{email}': 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{DEL_SONG_EP}/<name>/<artist>')
class DelSong(Resource):
    """
    Deletes a song by name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, name, artist):
        """
        Deletes a song by name and artist.
        """
        try:
            songs.del_song(name, artist)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


song_fields = api.model('NewSong', {
    songs.NAME: fields.String,
    songs.ARTIST: fields.String,
    songs.ALBUM: fields.String,
    songs.GENRE: fields.String,
    songs.BPM: fields.Integer,
})


@api.route(f'{SONGS_EP}')
class Songs(Resource):
    """
    This class supports various operations on songs, such as
    listing them, and adding a song.
    """
    def get(self):
        """
        This method returns all songs.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Songs',
            DATA: songs.get_songs(),
            MENU: SONG_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(song_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a song.
        """
        name = request.json[songs.NAME]
        artist = request.json[songs.ARTIST]
        album = request.json[songs.ALBUM]
        genre = request.json[songs.GENRE]
        bpm = request.json[songs.BPM]
        new_song = {
            'name': name,
            'artist': artist,
            'album': album,
            'genre': genre,
            'bpm': bpm,
        }
        try:
            song_added = songs.add_song(new_song)
            if not song_added:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'Song added': f'{song_added}'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

from flask import Flask
import unittest
import json

from letterconnect_server.routes.api import api


# https://github.com/aaronjolson/flask-pytest-example/
# https://www.youtube.com/watch?v=sL_PWBOABWo

class TestApi(unittest.TestCase):

    app = Flask("__name__")
    api(app)
    client = app.test_client()
    mock_request_headers = {
        'Content-Type': 'application/json'
    }

    def new_game(self):
        """
        Creates a valid new game.
        :return:
        """
        url = '/new-game'
        mock_request_post_body = {
            "nodes": ["a", "b", "c", "a"]
        }
        return self.client.post(url, data=json.dumps(mock_request_post_body), headers=self.mock_request_headers)

    def test_game_pass(self):
        """
        Get game instance by game id. Test if passes with the right id.
        :return:
        """
        response = self.new_game()

        url = '/games/0'
        response = self.client.get(url, headers=self.mock_request_headers)
        assert response.status_code == 200

    def test_game_fail(self):
        """
        Get game instance bu game id. Test if fails with a wrong id.
        :return:
        """
        response = self.new_game()

        url = '/games/1'
        response = self.client.get(url, headers=self.mock_request_headers)
        assert response.status_code == 404

    def test_move_pass(self):
        """
        Test response of a valid move.
        :return:
        """
        response = self.new_game()
        url = 'games/0/move'
        mock_request_post_body = {
            "from": 2,
            "to": 0
        }
        response = self.client.post(url, data=json.dumps(mock_request_post_body), headers=self.mock_request_headers)
        assert response.status_code == 200

    def test_move_fail1(self):
        """
        Test if the move is valid by connecting same type of letters.
        :return:
        """
        response = self.new_game()
        url = 'games/0/move'
        mock_request_post_body = {
            "from": 1,
            "to": 1
        }
        response = self.client.post(url, data=json.dumps(mock_request_post_body), headers=self.mock_request_headers)
        assert response.status_code == 400

    def test_move_fail2(self):
        """
        Test if the move is valid by connecting same type of letters.
        :return:
        """
        response = self.new_game()
        url = 'games/0/move'
        mock_request_post_body = {
            "from": 0,
            "to": 3
        }
        response = self.client.post(url, data=json.dumps(mock_request_post_body), headers=self.mock_request_headers)
        assert response.status_code == 400

    def test_move_fail3(self):
        """
        Test if the move is valid if one letter tries to connect with a third letter.
        :return:
        """
        response = self.new_game()
        url = 'games/0/move'
        mock_request_post_body = {
            "from": 1,
            "to": 2
        }
        response = self.client.post(url, data=json.dumps(mock_request_post_body), headers=self.mock_request_headers)
        mock_request_post_body = {
            "from": 1,
            "to": 3
        }
        response = self.client.post(url, data=json.dumps(mock_request_post_body), headers=self.mock_request_headers)
        mock_request_post_body = {
            "from": 1,
            "to": 0
        }
        response = self.client.post(url, data=json.dumps(mock_request_post_body), headers=self.mock_request_headers)
        assert response.status_code == 400

    def test_new_game_pass(self):
        """
        Test if a game is valid.
        :return:
        """
        response = self.new_game()
        assert response.status_code == 200

    def test_new_game_fail(self):
        """
        Test if the game is invalid with the letter which is not in ['a','b','c'].
        :return:
        """
        url = '/new-game'
        mock_request_post_body = {
            "nodes": ["a", "b", "c", "d"]
        }
        response = self.client.post(url, data=json.dumps(mock_request_post_body), headers=self.mock_request_headers)
        assert response.status_code == 400

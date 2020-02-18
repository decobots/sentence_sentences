import json

import falcon
from falcon_app.HandleCORS import HandleCORS
from sqlalchemy import func

from preparation.data_base import DataBase, Lines


class Quotes(object):
    def __init__(self, url=None):
        self.db = DataBase(url)

    def on_get(self, req, resp):
        session = self.db.Session()
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        line = get_line(session)
        resp.body = json.dumps(str(line[0]))
        session.close()


def get_line(session):
    return session.query(Lines).order_by(func.random()).limit(1)


def create(url=None):
    api = falcon.API(middleware=[HandleCORS()])
    quotes = Quotes(url)
    api.add_route('/quotes', quotes)
    return api


app = create()

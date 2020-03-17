import json
from typing import Optional

import falcon
from falcon import request as FalconRequest, response as FalconResponse
from falcon_app.HandleCORS import HandleCORS
from preparation.data_base import DataBase, Lines
from sqlalchemy import func
from sqlalchemy.orm.session import Session  as AlchemySession


class Quotes(object):
    def __init__(self, url: str = None):
        self.db = DataBase(url)

    def on_get(self, req: FalconRequest, resp: FalconResponse):
        session = self.db.Session()
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        line = get_line(session)
        resp.body = json.dumps(str(line[0]))
        session.close()


def get_line(session: AlchemySession) -> list:
    return session.query(Lines).order_by(func.random()).limit(1)


def create(url: Optional[str] = None) -> falcon.API:
    api = falcon.API(middleware=[HandleCORS()])
    quotes = Quotes(url)
    api.add_route('/quotes', quotes)
    return api


app = create()

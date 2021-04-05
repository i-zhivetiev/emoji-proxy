import tornado.web
from tornado.httpclient import HTTPRequest

from emoji_proxy.interfaces import Interfaces


class ProxyHandler(tornado.web.RequestHandler):
    def initialize(self, ifaces: Interfaces) -> None:
        self.http_client = ifaces.http_client
        self.content_filter = ifaces.content_filter

    async def get(self, path: str) -> None:
        request = HTTPRequest(f'https://lifehacker.ru/{path}')
        response = await self.http_client.fetch(request)
        body = self.content_filter.add_emojis_to_article(response.body)
        self.write(body)

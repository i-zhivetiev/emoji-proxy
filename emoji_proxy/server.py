import logging

import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

from emoji_proxy.interfaces import Interfaces
from emoji_proxy.page_content_filter import PageContentFilter
from emoji_proxy.proxy_handler import ProxyHandler

log = logging.getLogger(__name__)


def main():
    define('config', default='emoji_proxy.conf')
    define('port', default=9000)
    define('emojis', default=['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣'])
    define('word_length', default=6)
    define('debug', default=False)

    options.parse_command_line()
    options.parse_config_file(options.config, final=True)

    start_server()


def start_server():
    log.info('Staring server on %s', options.port)
    web_app = make_web_app(debug=options.debug)
    server = HTTPServer(web_app)
    server.bind(port=options.port)
    server.start()
    log.info('Server started')
    IOLoop.current().start()
    server.stop()


def make_web_app(debug=False):
    deps = dict(
        ifaces=Interfaces(
            http_client=AsyncHTTPClient(),
            content_filter=PageContentFilter(
                emojis=options.emojis,
                word_length=options.word_length,
            ),
        )
    )
    return tornado.web.Application(
        handlers=[(r'/(.*)', ProxyHandler, deps)],
        debug=debug,
    )


if __name__ == "__main__":
    main()

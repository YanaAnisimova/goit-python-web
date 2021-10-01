import aiohttp_jinja2
from aiohttp_jinja2.helpers import url_for
from aiohttp import web
import aiohttp_session_flash
import jinja2
from crypto_app.middlewares import setup_middlewares
from routes import setup_routes
from settings import TEMPLATE_PATH


app = web.Application()
setup_routes(app)
setup_middlewares(app)
# app["config"] = dict()
env = aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
    context_processors=[aiohttp_session_flash.context_processor])
env.globals.update({'url_for': url_for})

web.run_app(app)




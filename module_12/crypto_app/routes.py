from views import index
from settings import STATIC_PATH


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_static('/static/', path=STATIC_PATH, name='static')


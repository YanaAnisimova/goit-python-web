import aiohttp_jinja2

from settings import handlers


@aiohttp_jinja2.template('crypto/index.html')
async def index(request):
    return {key: await handler for key, handler in handlers.items()}

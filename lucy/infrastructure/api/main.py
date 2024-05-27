from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def heart_beat(request):
    return PlainTextResponse('Heart beat!')


routes = [
    Route('/', endpoint=heart_beat),
]

app = Starlette(routes=routes)

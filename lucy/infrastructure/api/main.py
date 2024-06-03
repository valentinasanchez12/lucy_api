from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount

from lucy.infrastructure.api.v1.endpoints.category.category import category
from lucy.infrastructure.api.v1.endpoints.provider.provider import provider
from lucy.infrastructure.api.v1.endpoints.sanitary_registry.sanitary_registry import sanitary_registry
from lucy.infrastructure.repositories.pg_repositories.pg_pool import initialize_pool


async def heart_beat(request):
    return PlainTextResponse('Heart beat!')


routes = [
    Route('/', endpoint=heart_beat),
    Mount('/api/category', routes=category.routes),
    Mount('/api/provider', routes=provider.routes),
    Mount('/api/sanitary-registry', routes=sanitary_registry.routes),

]

app = Starlette(routes=routes)


@app.on_event('startup')
async def init_db():
    await initialize_pool()

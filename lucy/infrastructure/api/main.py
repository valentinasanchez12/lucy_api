from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount

from lucy.infrastructure.api.v1.endpoints.brand.brand import brand
from lucy.infrastructure.api.v1.endpoints.category.category import category
from lucy.infrastructure.api.v1.endpoints.comments import comment
from lucy.infrastructure.api.v1.endpoints.product import product
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
    Mount('/api/brand', routes=brand.routes),
    Mount('/api/product', routes=product.routes),
    Mount('/api/comments', routes=comment.routes),

]

app = Starlette(routes=routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origen permitido (frontend)
    allow_methods=["*"],                     # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],                     # Headers permitidos
    allow_credentials=True,                  # Permitir credenciales (cookies, Authorization headers)
)


@app.on_event('startup')
async def init_db():
    await initialize_pool()

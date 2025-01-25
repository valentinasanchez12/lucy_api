import os

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse, FileResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

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
    Route('/heart', endpoint=heart_beat),
    Mount('/api/category', routes=category.routes),
    Mount('/api/provider', routes=provider.routes),
    Mount('/api/sanitary-registry', routes=sanitary_registry.routes),
    Mount('/api/brand', routes=brand.routes),
    Mount('/api/product', routes=product.routes),
    Mount('/api/comments', routes=comment.routes),
    Mount('/static', app=StaticFiles(directory='static'), name='static'),

]

app = Starlette(routes=routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173", "http://192.168.0.52:8080"],  # Origen permitido (frontend)
    allow_methods=["*"],  # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Headers permitidos
    allow_credentials=True,  # Permitir credenciales (cookies, Authorization headers)
)

frontend_build_dir = os.path.join('.', 'static')


@app.route('/{path:path}', methods=['GET'])
async def serve_frontend(request):
    if request.url.path.startswith("/api") or request.url.path.startswith("/static"):
        return JSONResponse({"error": "Not found"}, status_code=404)
    file_path = os.path.join(frontend_build_dir, 'index.html')
    return FileResponse(file_path)


@app.on_event('startup')
async def init_db():
    print(frontend_build_dir)
    await initialize_pool()

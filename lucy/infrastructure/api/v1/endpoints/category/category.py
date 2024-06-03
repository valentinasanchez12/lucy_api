import uuid

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.use_case.category.create_category import CreateCategory
from lucy.domain.models.category import Category
from lucy.infrastructure.repositories.pg_repositories.pg_category_repository import PGCategoryRepository


async def save(request):
    fields = ['name']
    data = await request.json()
    if all(key in data for key in fields):
        category_data = Category(
            uuid=uuid.uuid4(),
            name=data.get('name')
        )
        use_case = CreateCategory(repository=PGCategoryRepository(), category=category_data)
        await use_case.create()
        return JSONResponse(status_code=200, content={'success': True, 'response': 'Created category successfully.'})
    else:
        return JSONResponse(status_code=422, content={'success': False, 'response': 'Missing Parameters'})

routes = [
    Route('/category', endpoint=save, methods=['POST'])
]

category = Starlette(routes=routes)

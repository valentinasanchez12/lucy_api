import uuid

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.use_case.brand.create_brand import CreateBrand
from lucy.domain.models.brand import Brand
from lucy.domain.models.provider import Provider
from lucy.infrastructure.repositories.pg_repositories.pg_brand_repository import PGBrandRepository


async def save(request):
    fields = ['name', 'provider_uuid']
    data = await request.json()
    if all(key in data for key in fields):
        provider = Provider(uuid=data.get('provider_uuid'))
        brand_data = Brand(
            uuid=uuid.uuid4(),
            name=data.get('name'),
            provider=provider
        )
        use_case = CreateBrand(repository=PGBrandRepository(), brand=brand_data)
        status_code, success, message = await use_case.create()
        return JSONResponse(status_code=status_code, content={'success': success, 'response': message})
    else:
        return JSONResponse(status_code=422, content={'success': False, 'response': 'Missing Parameters'})

routes = [
    Route('/', endpoint=save, methods=['POST'])
]

brand = Starlette(routes=routes)

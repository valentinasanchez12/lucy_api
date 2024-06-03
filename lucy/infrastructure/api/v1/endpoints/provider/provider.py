import uuid

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.use_case.provider.create_provider import CreateProvider
from lucy.domain.models.provider import Provider
from lucy.infrastructure.repositories.pg_repositories.pg_provider_repository import PGProviderRepository


async def save(request):
    fields = ['name', 'represent', 'phone', 'email']
    data = await request.json()
    if all(key in data for key in fields):
        provider_data = Provider(
            uuid=uuid.uuid4(),
            name=data.get('name'),
            represent=data.get('represent'),
            phone=data.get('phone'),
            email=data.get('email')
        )
        use_case = CreateProvider(repository=PGProviderRepository(), provider=provider_data)
        await use_case.create()
        return JSONResponse(status_code=200, content={'success': True, 'response': 'Created category successfully.'})
    else:
        return JSONResponse(status_code=422, content={'success': False, 'response': 'Missing Parameters'})

routes = [
    Route('/', endpoint=save, methods=['POST'])
]

provider = Starlette(routes=routes)

import uuid

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.use_case.santitary_registry.create_sanitary_registry import CreateSanitaryRegistry
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.infrastructure.repositories.pg_repositories.pg_sanitary_registry_repository import \
    PGSanitaryRegistryRepository


async def save(request):
    fields = ['documents', 'number_registry', 'expiration_date', 'cluster', 'status', 'type_risk']
    data = await request.json()
    if all(key in data for key in fields):
        sanitary_registry_data = SanitaryRegistry(
            uuid=uuid.uuid4(),
            documents=data.get('documents'),
            number_registry=data.get('number_registry'),
            expiration_date=data.get('expiration_date'),
            cluster=data.get('cluster'),
            status=data.get('status'),
            type_risk=data.get('type_risk')

        )
        use_case = CreateSanitaryRegistry(
            repository=PGSanitaryRegistryRepository(),
            sanitary_registry=sanitary_registry_data
        )
        await use_case.create()
        return JSONResponse(status_code=200, content={'success': True, 'response': 'Created category successfully.'})
    else:
        return JSONResponse(status_code=422, content={'success': False, 'response': 'Missing Parameters'})


routes = [
    Route('/', endpoint=save, methods=['POST'])
]

sanitary_registry = Starlette(routes=routes)

import uuid

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.services.file_service import FileService
from lucy.application.use_case.santitary_registry.create_sanitary_registry import CreateSanitaryRegistry
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.infrastructure.repositories.pg_repositories.pg_sanitary_registry_repository import \
    PGSanitaryRegistryRepository


async def save(request):
    fields = ['number_registry', 'expiration_date', 'cluster', 'status', 'type_risk']
    data = await request.json()
    print(data)
    if all(key in data for key in fields):
        file_name = data['file_name']
        file_content_base64 = data['file_content']
        file_service = FileService(upload_dir='static/sanitary_register')
        file_path = file_service.upload_file(file_name, file_content_base64)
        sanitary_registry_data = SanitaryRegistry(
            uuid=uuid.uuid4(),
            documents=file_path,
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

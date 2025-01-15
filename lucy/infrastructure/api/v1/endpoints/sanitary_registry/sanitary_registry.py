import uuid

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.services.file_service import FileService
from lucy.application.use_case.santitary_registry.sanitary_registry_use_case import SanitaryRegistryUseCase
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.infrastructure import validate_data
from lucy.infrastructure.repositories.pg_repositories.pg_sanitary_registry_repository import \
    PGSanitaryRegistryRepository


async def endpoint(request: Request):
    if request.method == "GET":
        return await get_all(request)
    elif request.method == "POST":
        return await save(request)


required_fields = ['number_registry', 'expiration_date', 'cluster', 'status', 'type_risk', 'file_name', 'file_content']


async def save(request: Request):
    try:
        data = await request.json()

        validation = validate_data(data, required_fields)
        if not validation["is_valid"]:
            return JSONResponse(
                status_code=422,
                content={
                    'data': None,
                    "success": False,
                    "response": f"Missing parameters: {', '.join(validation['missing'])}",
                },
            )

        file_service = FileService(upload_dir='static/sanitary_register')
        file_path = file_service.upload_file(data['file_name'], data['file_content'])
        static_url = request.url_for("static", path=file_path)
        sanitary_registry_data = SanitaryRegistry(
            uuid=uuid.uuid4(),
            url=static_url,
            number_registry=data.get('number_registry'),
            expiration_date=data.get('expiration_date'),
            cluster=data.get('cluster'),
            status=data.get('status'),
            type_risk=data.get('type_risk'),
        )

        use_case = SanitaryRegistryUseCase(
            repository=PGSanitaryRegistryRepository(),
            sanitary_registry=sanitary_registry_data,
        )
        sanitary_registry_data = await use_case.create()
        return JSONResponse(
            status_code=200,
            content={
                'data': sanitary_registry_data,
                "success": True,
                "response": "Sanitary registry created successfully.",
            },
        )
    except KeyError as e:
        return JSONResponse(
            status_code=400,
            content={
                'data': None,
                "success": False,
                "response": f"Missing or invalid key in request: {str(e)}",
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                'data': None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}",
            },
        )


async def get_all(request: Request):
    try:
        use_case = SanitaryRegistryUseCase(repository=PGSanitaryRegistryRepository())
        sanitary_registries = await use_case.get_all()

        if sanitary_registries:
            return JSONResponse(
                status_code=200,
                content={
                    "data": sanitary_registries,
                    "success": True,
                    "response": "Sanitary registries fetched successfully.",
                },
            )
        else:
            return JSONResponse(
                status_code=200,
                content={
                    "data": [],
                    "success": True,
                    "response": "No sanitary registries found.",
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}",
            },
        )


async def get_by_id(request: Request):
    try:
        registry_id = request.path_params['registry_id']
        use_case = SanitaryRegistryUseCase(repository=PGSanitaryRegistryRepository())
        sanitary_registry_data = await use_case.get_by_id(registry_id)

        if sanitary_registry_data:
            return JSONResponse(
                status_code=200,
                content={
                    "data": sanitary_registry_data,
                    "success": True,
                    "response": "Sanitary registry fetched successfully.",
                },
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "data": None,
                    "success": False,
                    "response": "Sanitary registry not found.",
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}",
            },
        )


async def update(request: Request):
    try:
        registry_id = request.path_params['registry_id']
        data = await request.json()

        if not data:
            return JSONResponse(
                status_code=400,
                content={
                    "data": None,
                    "success": False,
                    "response": "No data provided for update.",
                },
            )
        static_url = None
        file_service = FileService(upload_dir="static/sanitary_register")
        if "file_name" in data and "file_content" in data:
            file_path = file_service.upload_file(data["file_name"], data["file_content"])
            static_url = request.url_for("static", path=file_path)
        use_case = SanitaryRegistryUseCase(repository=PGSanitaryRegistryRepository())
        updated_registry = await use_case.update(registry_id, data, static_url)

        if updated_registry:
            return JSONResponse(
                status_code=200,
                content={
                    "data": updated_registry,
                    "success": True,
                    "response": "Sanitary registry updated successfully.",
                },
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "data": None,
                    "success": False,
                    "response": "Sanitary registry not found or already deleted.",
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}",
            },
        )


async def delete(request: Request):
    try:
        registry_id = request.path_params['registry_id']

        use_case = SanitaryRegistryUseCase(repository=PGSanitaryRegistryRepository())
        deleted_registry = await use_case.delete(registry_id)

        if deleted_registry:
            return JSONResponse(
                status_code=200,
                content={
                    "data": deleted_registry,
                    "success": True,
                    "response": "Sanitary registry deleted successfully.",
                },
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "data": None,
                    "success": False,
                    "response": "Sanitary registry not found or already deleted.",
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}",
            },
        )


routes = [
    Route('/', endpoint=endpoint, methods=['GET', 'POST']),
    Route('/{registry_id}', endpoint=get_by_id, methods=['GET']),
    Route('/{registry_id}', endpoint=update, methods=['PUT']),
    Route('/{registry_id}', endpoint=delete, methods=['DELETE']),
]

sanitary_registry = Starlette(routes=routes)

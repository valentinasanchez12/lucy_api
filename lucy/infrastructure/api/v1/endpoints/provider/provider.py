import uuid

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.use_case.brand_provider_use_case import BrandProviderUseCase
from lucy.application.use_case.provider.get_amount_use_case import GetAmountUseCase
from lucy.application.use_case.provider.provider_use_case import ProviderUseCase
from lucy.domain.models.brand import Brand
from lucy.domain.models.provider import Provider
from lucy.core.utils import validate_data
from lucy.infrastructure.repositories.pg_repositories.pg_brand_provider_repository import PGBrandProviderRepository
from lucy.infrastructure.repositories.pg_repositories.pg_provider_repository import PGProviderRepository


required_fields = ['name', 'represent', 'phone', 'email', 'brands']


async def endpoint(request: Request):
    if request.method == "GET":
        return await get_all_providers(request)
    elif request.method == "POST":
        return await save(request)


async def save(request: Request):
    try:
        data = await request.json()
        validation = validate_data(data, required_fields)
        if not validation["is_valid"]:
            return JSONResponse(
                status_code=422,
                content={
                    'data': None,
                    'success': False,
                    'response': f"Missing Parameters: {', '.join(validation['missing'])}"
                }
            )
        brand_data = []
        for brand in data['brands']:
            brand_data.append(Brand(**brand))

        provider_data = Provider(
            uuid=str(uuid.uuid4()),
            types_person=data['types_person'],
            nit=data['nit'],
            name=data['name'],
            represent=data['represent'],
            phone=data['phone'],
            email=data['email'],
            brands=brand_data
        )

        use_case = ProviderUseCase(repository=PGProviderRepository(), provider=provider_data)
        provider_add = await use_case.create()
        if provider_add:
            brand_provider = BrandProviderUseCase(PGBrandProviderRepository())
            await brand_provider.save(brands=provider_data.brands, provider=provider_data)
        provider_add['brands'] = [brand.to_dict() for brand in provider_data.brands]
        return JSONResponse(
            status_code=200,
            content={
                'data': provider_add,
                'success': True,
                'response': 'Created provider successfully'
            }
        )

    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=500,
            content={
                'data': None,
                'success': False,
                'response': f"Internal Server Error: {str(e)}"
            }
        )


async def get_all_providers(request: Request):
    try:
        use_case = ProviderUseCase(repository=PGProviderRepository())
        providers = await use_case.get_all()
        return JSONResponse(
            status_code=200,
            content={
                'data': providers,
                'success': True,
                'response': 'Providers fetched successfully.'
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'data': None,
                'success': False,
                'response': f"Internal Server Error: {str(e)}"
            }
        )


async def get_provider_by_id(request: Request):
    try:
        provider_id = request.path_params['provider_id']
        use_case = ProviderUseCase(repository=PGProviderRepository())
        provider_data = await use_case.get_by_id(uuid=provider_id)
        if provider:
            return JSONResponse(
                status_code=200,
                content={
                    'data': provider_data,
                    'success': True,
                    'response': 'Provider fetched successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Provider not found.'
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'data': None,
                'success': False,
                'response': f"Internal Server Error: {str(e)}"
            }
        )


async def update_provider(request: Request):
    try:
        provider_id = request.path_params['provider_id']
        data = await request.json()

        if not data:
            return JSONResponse(
                status_code=400,
                content={
                    'data': None,
                    'success': False,
                    'response': 'No data provided for update.'
                }
            )
        validation = validate_data(data, required_fields)
        if not validation["is_valid"]:
            return JSONResponse(
                status_code=422,
                content={
                    'data': None,
                    'success': False,
                    'response': f"Missing Parameters: {', '.join(validation['missing'])}"
                }
            )
        print(data)
        brand_provider_repository = PGBrandProviderRepository()
        brand_provider_use_case = BrandProviderUseCase(repository=brand_provider_repository)
        provider_use_case = ProviderUseCase(
            repository=PGProviderRepository(),
            brand_provider_use_case=brand_provider_use_case
        )

        updated_provider = await provider_use_case.update(uuid=provider_id, update_data=data)

        if updated_provider:
            return JSONResponse(
                status_code=200,
                content={
                    'data': updated_provider,
                    'success': True,
                    'response': 'Provider updated successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Provider not found or already deleted.'
                }
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                'data': None,
                'success': False,
                'response': f"Internal Server Error: {str(e)}"
            }
        )


async def delete_provider(request: Request):
    try:
        provider_id = request.path_params['provider_id']
        use_case = ProviderUseCase(repository=PGProviderRepository())
        deleted_provider = await use_case.delete(provider_id)

        if deleted_provider:
            return JSONResponse(
                status_code=200,
                content={
                    'data': deleted_provider,
                    'success': True,
                    'response': 'Provider deleted successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Provider not found or already deleted.'
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'data': None,
                'success': False,
                'response': f"Internal Server Error: {str(e)}"
            }
        )

async def get_amount(request: Request):
    try:
        use_case = GetAmountUseCase(PGProviderRepository())
        return JSONResponse(
            status_code=200,
            content={
                'data': await use_case.get_amount(),
                'success': True,
                'response': 'Amount of providers fetched successfully.'
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'data': None,
                'success': False,
                'response': f"Internal Server Error: {str(e)}"
            }
        )

routes = [
    Route('/', endpoint=endpoint, methods=['POST', 'GET']),
    Route('/{provider_id}', endpoint=get_provider_by_id, methods=['GET']),
    Route('/{provider_id}', endpoint=update_provider, methods=['PUT']),
    Route('/{provider_id}', endpoint=delete_provider, methods=['DELETE']),
    Route('/amount', endpoint=get_amount, methods=['GET'])
]

provider = Starlette(routes=routes)

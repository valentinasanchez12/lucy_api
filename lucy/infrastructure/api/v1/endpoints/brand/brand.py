import uuid

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request

from lucy.application.use_case.brand.create_brand import BrandUseCase
from lucy.domain.models.brand import Brand
from lucy.infrastructure import validate_data
from lucy.infrastructure.repositories.pg_repositories.pg_brand_repository import PGBrandRepository


async def endpoint(request: Request):
    if request.method == "GET":
        return await get_all_brands(request)
    elif request.method == "POST":
        return await save(request)


required_fields = ['name']


async def save(request: Request):
    try:
        data = await request.json()
        print(data)
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
        brand_data = Brand(
            uuid=uuid.uuid4(),
            name=data['name']
        )
        use_case = BrandUseCase(repository=PGBrandRepository(), brand=brand_data)
        created_brand = await use_case.create()
        return JSONResponse(
            status_code=201,
            content={
                'data': created_brand,
                'success': True,
                'response': 'Created brand successfully'
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


async def get_all_brands(request: Request):
    try:
        use_case = BrandUseCase(repository=PGBrandRepository())
        return JSONResponse(
            status_code=200,
            content={
                'data': await use_case.get_all(),
                'success': True,
                'response': 'Brands fetched successfully.'
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


async def get_brand_by_id(request: Request):
    try:
        brand_id = request.path_params['brand_id']
        use_case = BrandUseCase(repository=PGBrandRepository())
        data_brand = await use_case.get_by_id(uuid=brand_id)
        if data_brand:
            return JSONResponse(
                status_code=200,
                content={
                    'data': data_brand,
                    'success': True,
                    'response': 'Brand fetched successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Brand not found.'
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


async def update_brand(request: Request):
    try:
        brand_id = request.path_params['brand_id']
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

        use_case = BrandUseCase(repository=PGBrandRepository())
        updated_brand = await use_case.update(uuid=brand_id, update_data=data)

        if updated_brand:
            return JSONResponse(
                status_code=200,
                content={
                    'data': updated_brand,
                    'success': True,
                    'response': 'Brand updated successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Brand not found or already deleted.'
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


async def delete_brand(request: Request):
    try:
        brand_id = request.path_params['brand_id']
        use_case = BrandUseCase(repository=PGBrandRepository())
        deleted_brand = await use_case.delete(brand_id=brand_id)

        if deleted_brand:
            return JSONResponse(
                status_code=200,
                content={
                    'data': deleted_brand,
                    'success': True,
                    'response': 'Brand deleted successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Brand not found or already deleted.'
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
    Route('/{brand_id}', endpoint=get_brand_by_id, methods=['GET']),
    Route('/{brand_id}', endpoint=update_brand, methods=['PUT']),
    Route('/{brand_id}', endpoint=delete_brand, methods=['DELETE']),
]

brand = Starlette(routes=routes)

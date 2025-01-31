import uuid

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.use_case.category.category_use_case import CategoryUseCase
from lucy.application.use_case.category.get_amount_use_case import GetAmountUseCase
from lucy.domain.models.category import Category
from lucy.core.utils import validate_data
from lucy.infrastructure.repositories.pg_repositories.pg_category_repository import PGCategoryRepository


async def endpoint(request: Request):
    if request.method == "GET":
        return await get_all_categories(request)
    elif request.method == "POST":
        return await save(request)


required_fields = ['name']


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
        category_data = Category(
            uuid=uuid.uuid4(),
            name=data['name']
        )
        use_case = CategoryUseCase(repository=PGCategoryRepository(), category=category_data)
        created_brand = await use_case.create()
        return JSONResponse(
            status_code=200,
            content={
                'data': created_brand,
                'success': True,
                'response': 'Created category successfully'
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


async def get_all_categories(request: Request):
    try:
        use_case = CategoryUseCase(repository=PGCategoryRepository())
        return JSONResponse(
            status_code=200,
            content={
                'data': await use_case.get_all(),
                'success': True,
                'response': 'Categories fetched successfully.'
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


async def get_category_by_id(request: Request):
    try:
        category_id = request.path_params['category_id']

        use_case = CategoryUseCase(repository=PGCategoryRepository())
        category = await use_case.get_by_id(category_id)

        if category:
            return JSONResponse(
                status_code=200,
                content={
                    'data': category,
                    'success': True,
                    'response': 'Category fetched successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Category not found.'
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


async def update_category(request: Request):
    try:
        category_id = request.path_params['category_id']
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

        use_case = CategoryUseCase(repository=PGCategoryRepository())
        updated_category = await use_case.update(category_id=category_id, category_data=data)

        if updated_category:
            return JSONResponse(
                status_code=200,
                content={
                    'data': updated_category,
                    'success': True,
                    'response': 'Category updated successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Category not found or already deleted.'
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


async def delete_category(request: Request):
    try:
        category_id = request.path_params['category_id']

        use_case = CategoryUseCase(repository=PGCategoryRepository())
        deleted_category = await use_case.delete(category_id)

        if deleted_category:
            return JSONResponse(
                status_code=200,
                content={
                    'data': deleted_category,
                    'success': True,
                    'response': 'Category deleted successfully.'
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    'data': None,
                    'success': False,
                    'response': 'Category not found or already deleted.'
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
        use_case = GetAmountUseCase(PGCategoryRepository())
        return JSONResponse(
            status_code=200,
            content={
                'data': await use_case.get_amount(),
                'success': True,
                'response': 'Categories fetched successfully.'
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
    Route('/', endpoint=endpoint, methods=['GET', 'POST']),
    Route('/{category_id}', endpoint=get_category_by_id, methods=['GET']),
    Route('/{category_id}', endpoint=update_category, methods=['PUT']),
    Route('/{category_id}', endpoint=delete_category, methods=['DELETE']),
    Route('/amount', endpoint=get_amount, methods=['GET'])
]

category = Starlette(routes=routes)

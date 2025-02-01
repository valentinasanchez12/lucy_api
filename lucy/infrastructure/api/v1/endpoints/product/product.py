import uuid

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from lucy.application.services.file_service import FileService
from lucy.application.use_case.product.get_amount_use_case import GetAmountUseCase
from lucy.application.use_case.product.product_use_case import ProductUseCase
from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.comments import Comments
from lucy.domain.models.product import Product
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.domain.models.technical_sheets import TechnicalSheet
from lucy.core.utils import validate_data, convert_line_breaks_to_pipelines, is_base64
from lucy.infrastructure.repositories.pg_repositories.pg_characteristic_repository import PGCharacteristicRepository
from lucy.infrastructure.repositories.pg_repositories.pg_comment_repository import PGCommentRepository
from lucy.infrastructure.repositories.pg_repositories.pg_product_repository import PGProductRepository
from lucy.infrastructure.repositories.pg_repositories.pg_technical_repository import PGTechnicalSheetRepository

required_fields = [
    "generic_name", "commercial_name", "description", "measurement",
    "formulation", "composition", "reference", "use", "status",
    "sanitize_method", "images", "brand",
    "category", "sanitary_register", "comment", "technical_sheet"
]


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

        file_service = FileService(upload_dir="static/images")
        image_paths = []

        for image in data["images"]:
            image_paths.append(file_service.upload_file(image["file_name"], image["file_content"]))
        technical_sheet_path = file_service.upload_file(
            data["technical_sheet"]["file_name"],
            data["technical_sheet"]["file_content"]
        )

        product_data = Product(
            uuid=uuid.uuid4(),
            generic_name=data["generic_name"],
            commercial_name=data["commercial_name"],
            description=convert_line_breaks_to_pipelines(data["description"]),
            measurement=data["measurement"],
            formulation=data["formulation"],
            composition=convert_line_breaks_to_pipelines(data["composition"]),
            reference=data["reference"],
            use=convert_line_breaks_to_pipelines(data["use"]),
            status=data["status"],
            sanitize_method=data["sanitize_method"],
            images=image_paths,
            brand=Brand(uuid=data["brand"]),
            category=Category(uuid=data["category"]),
            sanitary_register=SanitaryRegistry(uuid=data["sanitary_register"]),
            iva=data['iva']
        )
        comment = Comments(
            uuid=uuid.uuid4(),
            comment=data["comment"]
        )
        technical_sheet = TechnicalSheet(
            uuid=uuid.uuid4(),
            document=technical_sheet_path
        )

        use_case = ProductUseCase(
            product_repository=PGProductRepository(),
            comment_repository=PGCommentRepository(),
            characteristic_repository=PGCharacteristicRepository(),
            technical_sheet_repository=PGTechnicalSheetRepository(),
        )
        created_product = await use_case.create(
            product=product_data,
            comment=comment,
            characteristics=[
                Characteristic(
                    uuid=uuid.uuid4(),
                    characteristic=char["name"],
                    description=char["description"],
                )
                for char in data.get("characteristics", [])
            ],
            technical_sheet=technical_sheet,
        )

        return JSONResponse(
            status_code=200,
            content={
                'data': created_product,
                'success': True,
                'response': 'Created product successfully'
            }
        )
    except KeyError as e:
        return JSONResponse(
            status_code=400,
            content={
                'data': None,
                'success': False,
                'response': f"Missing or invalid key: {str(e)}"
            }
        )
    except Exception as e:
        print(f'error 500 {e}')
        return JSONResponse(
            status_code=500,
            content={
                'data': None,
                'success': False,
                'response': f"Internal Server Error: {str(e)}"
            }
        )


async def get_by_id(request):
    try:
        product_id = request.path_params.get('product_id')

        if not product_id:
            return JSONResponse(
                status_code=400,
                content={
                    "data": None,
                    "success": False,
                    "response": "Product ID is required."
                }
            )

        use_case = ProductUseCase(product_repository=PGProductRepository())
        product_data = await use_case.get_by_id(product_id)

        if product_data:
            return JSONResponse(
                status_code=200,
                content={
                    "data": product_data,
                    "success": True,
                    "response": "Product fetched successfully."
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "data": None,
                    "success": False,
                    "response": "Product not found."
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}"
            }
        )


async def update(request):
    try:
        product_id = request.path_params.get('product_id')
        data = await request.json()
        if not product_id or not data:
            return JSONResponse(
                status_code=400,
                content={
                    "data": None,
                    "success": False,
                    "response": "Product ID and update data are required."
                }
            )
        image_paths = []
        file_service = FileService(upload_dir="static/images")
        for image in data.get('images'):
            if is_base64(image.get('file_content')):
                image_paths.append(file_service.upload_file(image["file_name"], image["file_content"]))
            else:
                image_paths.append(image.get('file_content'))
        technical_sheet_path = ''
        if is_base64(data.get('technical_sheet', {}).get('file_content')):
            technical_sheet_path = file_service.upload_file(
                data["technical_sheet"]["file_name"],
                data["technical_sheet"]["file_content"]
            )
        else:
            technical_sheet_path = data.get('technical_sheet', {}).get('file_content')

        product_data = Product(
            generic_name=data.get("generic_name"),
            commercial_name=data.get("commercial_name"),
            description=convert_line_breaks_to_pipelines(data.get("description")),
            measurement=data.get("measurement"),
            formulation=data.get("formulation"),
            composition=convert_line_breaks_to_pipelines(data.get("composition")),
            reference=data.get("reference"),
            use=convert_line_breaks_to_pipelines(data.get("use")),
            status=data.get("status"),
            sanitize_method=data.get("sanitize_method"),
            brand=Brand(uuid=data["brand"]),
            category=Category(uuid=data["category"]),
            sanitary_register=SanitaryRegistry(uuid=data["sanitary_register"]),
            images=image_paths,
            iva=data.get('iva')
        )

        use_case = ProductUseCase(
            product_repository=PGProductRepository(),
            characteristic_repository=PGCharacteristicRepository(),
            technical_sheet_repository=PGTechnicalSheetRepository()
        )
        updated_product = await use_case.update(
            product_id=product_id,
            product_data=product_data,
            characteristics=[
                Characteristic(
                    characteristic=char["characteristic"],
                    description=char["description"]
                ) for char in data.get("characteristics", [])
            ],
            technical_sheet=TechnicalSheet(
                document=technical_sheet_path
            )
        )

        if updated_product:
            return JSONResponse(
                status_code=200,
                content={
                    "data": updated_product,
                    "success": True,
                    "response": "Product updated successfully."
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "data": None,
                    "success": False,
                    "response": "Product not found."
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}"
            }
        )


async def search(request):
    try:
        query = request.query_params.get("q", "")
        if not query:
            return JSONResponse(
                status_code=400,
                content={
                    "data": None,
                    "success": False,
                    "response": "Search query is required."
                }
            )

        use_case = ProductUseCase(product_repository=PGProductRepository())
        products = await use_case.search(query)

        return JSONResponse(
            status_code=200,
            content={
                "data": products,
                "success": True,
                "response": "Search results retrieved successfully."
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}"
            }
        )


async def get_random(request: Request):
    try:
        use_case = ProductUseCase(product_repository=PGProductRepository())
        products = await use_case.get_random(limit=12)

        return JSONResponse(
            status_code=200,
            content={
                "data": products,
                "success": True,
                "response": "Random products retrieved successfully."
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}"
            }
        )


async def get_amount(request: Request):
    try:
        use_case = GetAmountUseCase(PGProductRepository())

        return JSONResponse(
            status_code=200,
            content={
                "data": await use_case.get_amount(),
                "success": True,
                "response": "Amount of products retrieved successfully."
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "data": None,
                "success": False,
                "response": f"Internal Server Error: {str(e)}"
            }
        )

routes = [
    Route('/', endpoint=save, methods=['POST']),
    Route('/search', endpoint=search, methods=['GET']),
    Route('/random', endpoint=get_random, methods=['GET']),
    Route('/{product_id}', endpoint=get_by_id, methods=['GET']),
    Route('/{product_id}', endpoint=update, methods=['PUT']),
    Route('/amount', endpoint=get_amount, methods=['GET'])

]

product = Starlette(routes=routes)

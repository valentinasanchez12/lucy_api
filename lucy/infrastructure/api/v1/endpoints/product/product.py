import uuid

from starlette.applications import Starlette
from starlette.routing import Route

from lucy.application.services.file_service import FileService
from lucy.application.use_case.product.create_product import CreateProduct
from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.observation import Observation
from lucy.domain.models.product import Product
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.domain.models.technical_sheets import TechnicalSheet
from lucy.infrastructure.repositories.pg_repositories.pg_characteristic_repository import PGCharacteristicRepository
from lucy.infrastructure.repositories.pg_repositories.pg_observation_repository import PGObservationRepository
from lucy.infrastructure.repositories.pg_repositories.pg_product_repository import PGProductRepository
from lucy.infrastructure.repositories.pg_repositories.pg_technical_repository import PGTechnicalRepository


async def save(request):
    data = await request.json()
    brand = Brand(uuid=data['brand']['uuid'])
    category = Category(uuid=data['category']['uuid'])
    sanitary_register = SanitaryRegistry(uuid=data['sanitary_register']['uuid'])
    file_name_image = data['file_name']
    file_content_base64_image = data['file_content']
    file_service = FileService(upload_dir='static/images')
    file_path_image = file_service.upload_file(file_name_image, file_content_base64_image)
    product = Product(
        uuid=data['uuid'],
        generic_name=data['generic_name'],
        commercial_name=data['commercial_name'],
        description=data['description'],
        measurement=data['measurement'],
        formulation=data['formulation'],
        composition=data['composition'],
        reference=data['reference'],
        use=data['use'],
        status=data['status'],
        sanitize_method=data['sanitize_method'],
        image=file_path_image,
        brands=brand,
        categories=category,
        sanitary_register=sanitary_register,
    )
    observations = list()
    characteristics = list()
    technical_sheets = list()
    for observation in data['observations']:
        observations.append(
            Observation(
                uuid=uuid.uuid4(),
                observation=observation['observation'],
            )
        )

    for characteristic in data['characteristics']:
        characteristics.append(
            Characteristic(
                uuid=uuid.uuid4(),
                characteristic=characteristic['characteristic'],
                description=characteristic['description'],
            )
        )
    for document in data['technical_sheets']:
        try:
            file_name = document['file_name']
            file_content_base64 = document['file_content']
            file_service = FileService(upload_dir='static/technical_sheets')
            file_path = file_service.upload_file(file_name, file_content_base64)
            technical_sheets.append(
                TechnicalSheet(
                    uuid=uuid.uuid4(),
                    document=file_path,
                )
            )
        except ValueError as e:
            print(f'error {e}')
    await CreateProduct(
        product_repository=PGProductRepository(),
        observation_repository=PGObservationRepository(),
        characteristic_repository=PGCharacteristicRepository(),
        technical_sheet_repository=PGTechnicalRepository(),
        product=product,
        observation=observations,
        technical_sheet=technical_sheets,
        characteristic=characteristics
    ).create()


routes = [
    Route('/', endpoint=save, methods=['POST'])
]

provider = Starlette(routes=routes)

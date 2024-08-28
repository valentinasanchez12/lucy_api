import uuid

from starlette.applications import Starlette
from starlette.routing import Route

from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.observation import Observation
from lucy.domain.models.product import Product
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.domain.models.technical_sheets import TechnicalSheet


async def save(request):
    data = await request.json()
    brand = Brand(uuid=data['brand']['uuid'])
    category = Category(uuid=data['category']['uuid'])
    sanitary_register = SanitaryRegistry(uuid=data['sanitary_register']['uuid'])
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
        image=data['image'],
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
        technical_sheets.append(
            TechnicalSheet(
                uuid=uuid.uuid4(),
                document=data['document'],
            )
        )


routes = [
    Route('/', endpoint=save, methods=['POST'])
]

provider = Starlette(routes=routes)

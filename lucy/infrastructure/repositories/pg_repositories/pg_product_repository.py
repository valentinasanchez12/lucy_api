import ast

from lucy.application.repositories import ProductRepository
from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.comments import Comments
from lucy.domain.models.product import Product
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.domain.models.technical_sheets import TechnicalSheet
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGProductRepository(ProductRepository):

    async def get_random(self, limit: int = 12):
        if not isinstance(limit, int):
            raise ValueError(f"Invalid limit value: {limit}")
        pool = get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                '''SELECT p.uuid, p.generic_name, p.image, b.uuid AS brand_uuid, b.name AS brand_name
                    FROM products p
                    LEFT JOIN brands b ON p.brand_id::text = b.uuid::text
                    WHERE p.deleted_at IS NULL  
                    ORDER BY RANDOM()
                    LIMIT $1
                ''',
                limit
            )
            return [
                {
                    "uuid": str(row["uuid"]),
                    "generic_name": row["generic_name"],
                    "image": row["image"][0] if row["image"] else None,
                    "brand": {
                        "uuid": str(row["brand_uuid"]),
                        "name": row["brand_name"]
                    }
                }
                for row in rows
            ]

    async def update(self, product_id: str, product: Product):
        pool = get_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    '''
                    UPDATE products
                    SET generic_name = COALESCE($2, generic_name),
                        commercial_name = COALESCE($3, commercial_name),
                        description = COALESCE($4, description),
                        measurement = COALESCE($5, measurement),
                        formulation = COALESCE($6, formulation),
                        composition = COALESCE($7, composition),
                        reference = COALESCE($8, reference),
                        use = COALESCE($9, use),
                        status = COALESCE($10, status),
                        sanitize_method = COALESCE($11, sanitize_method),
                        image = COALESCE($12, image),
                        brand_id = COALESCE($13, brand_id),
                        category_id = COALESCE($14, category_id),
                        sanitary_register_id = COALESCE($15, sanitary_register_id),
                        iva = COALESCE($16, iva),
                        updated_at = LOCALTIMESTAMP
                    WHERE uuid = $1 AND deleted_at IS NULL
                    ''',
                    product_id,
                    product.generic_name,
                    product.commercial_name,
                    product.description,
                    product.measurement,
                    product.formulation,
                    product.composition,
                    product.reference,
                    product.use,
                    product.status,
                    product.sanitize_method,
                    product.images,
                    product.brand.uuid,
                    product.category.uuid,
                    product.sanitary_register.uuid,
                    product.iva
                )
                updated_product = await self.get_by_id(product_id)
                return updated_product

    async def delete(self, product_id: str):
        pass

    async def get_by_id(self, product_id: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT 
                    p.uuid, p.generic_name, p.commercial_name, p.description, p.measurement,
                    p.formulation, p.composition, p.reference, p.use, p.status,
                    p.sanitize_method, 
                    p.image, p.iva,
                    p.created_at, p.updated_at,
                    b.uuid AS brand_uuid, b.name AS brand_name,
                    c.uuid AS category_uuid, c.name AS category_name,
                    sr.uuid AS sanitary_register_uuid, sr.number_registry, sr.url,
                    ARRAY(
                        SELECT json_build_object(
                            'uuid', o.uuid,
                            'comment', o.comment
                        )
                        FROM comments o
                        WHERE o.product_id = p.uuid
                    ) AS comments,
                    ARRAY(
                        SELECT json_build_object(
                            'uuid', ch.uuid,
                            'characteristic', ch.characteristic,
                            'description', ch.description
                        )
                        FROM characteristics ch
                        WHERE ch.product_id = p.uuid
                    ) AS characteristics,
                    ARRAY(
                        SELECT json_build_object(
                            'uuid', ts.uuid,
                            'document', ts.document
                        )
                        FROM technical_sheets ts
                        WHERE ts.product_id = p.uuid
                    ) AS technical_sheets,
                    ARRAY(
                        SELECT json_build_object(
                            'uuid', pr.uuid,
                            'nit', pr.nit,
                            'types_person', pr.types_person,
                            'name', pr.name,
                            'represent', pr.represent,
                            'phone', pr.phone,
                            'email', pr.email
                        )
                        FROM brand_providers bp
                        INNER JOIN providers pr ON bp.provider_uuid = pr.uuid
                        WHERE bp.brand_uuid = b.uuid
                    ) AS providers
                FROM products p
                LEFT JOIN brands b ON p.brand_id = b.uuid
                LEFT JOIN categories c ON p.category_id = c.uuid
                LEFT JOIN sanitary_registry sr ON p.sanitary_register_id = sr.uuid
                WHERE p.uuid = $1 AND p.deleted_at IS NULL
                ''',
                product_id
            )
            if row:
                # Convertir comments, characteristics, technical_sheets y providers
                comments = [
                    ast.literal_eval(comment) if isinstance(comment, str) else comment
                    for comment in row['comments']
                ]
                characteristics = [
                    ast.literal_eval(characteristic) if isinstance(characteristic, str) else characteristic
                    for characteristic in row['characteristics']
                ]
                technical_sheets = [
                    ast.literal_eval(sheet) if isinstance(sheet, str) else sheet
                    for sheet in row['technical_sheets']
                ]
                providers = [
                    ast.literal_eval(provider) if isinstance(provider, str) else provider
                    for provider in row['providers']
                ]

                return Product(
                    uuid=row['uuid'],
                    generic_name=row['generic_name'],
                    commercial_name=row['commercial_name'],
                    description=row['description'],
                    measurement=row['measurement'],
                    formulation=row['formulation'],
                    composition=row['composition'],
                    reference=row['reference'],
                    use=row['use'],
                    status=row['status'],
                    sanitize_method=row['sanitize_method'],
                    images=row['image'],
                    iva=row['iva'],
                    brand=Brand(uuid=row['brand_uuid'], name=row['brand_name']),
                    category=Category(uuid=row['category_uuid'], name=row['category_name']),
                    sanitary_register=SanitaryRegistry(uuid=row['sanitary_register_uuid'],
                                                       number_registry=row['number_registry'],
                                                       url=row['url']),
                    comments=[
                        Comments(uuid=comment['uuid'], comment=comment['comment']).to_dict()
                        for comment in comments
                    ],
                    characteristics=[
                        Characteristic(uuid=ch['uuid'], characteristic=ch['characteristic'],
                                       description=ch['description']).to_dict()
                        for ch in characteristics
                    ],
                    technical_sheets=[
                        TechnicalSheet(uuid=ts['uuid'], document=ts['document']).to_dict()
                        for ts in technical_sheets
                    ],
                    providers=[
                        {
                            "uuid": provider["uuid"],
                            "nit": provider["nit"],
                            "types_person": provider["types_person"],
                            "name": provider["name"],
                            "represent": provider["represent"],
                            "phone": provider["phone"],
                            "email": provider["email"],
                        }
                        for provider in providers
                    ],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                )
            return None

    async def get_all(self):
        pass

    async def save(self, product: Product):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                INSERT INTO products (
                    uuid, generic_name, commercial_name, description, measurement,
                    formulation, composition, reference, use, status, sanitize_method,
                    image, brand_id, category_id, sanitary_register_id, iva, created_at, updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, LOCALTIMESTAMP, LOCALTIMESTAMP)
                RETURNING uuid, generic_name, commercial_name, description, measurement,
                          formulation, composition, reference, use, status, sanitize_method,
                          image, brand_id, category_id, sanitary_register_id, iva, created_at, updated_at
                ''',
                product.uuid,
                product.generic_name,
                product.commercial_name,
                product.description,
                product.measurement,
                product.formulation,
                product.composition,
                product.reference,
                product.use,
                product.status,
                product.sanitize_method,
                product.images,
                product.brand.uuid,
                product.category.uuid,
                product.sanitary_register.uuid,
                product.iva
            )
            if row:
                return Product(
                    uuid=row['uuid'],
                    generic_name=row['generic_name'],
                    commercial_name=row['commercial_name'],
                    description=row['description'],
                    measurement=row['measurement'],
                    formulation=row['formulation'],
                    composition=row['composition'],
                    reference=row['reference'],
                    use=row['use'],
                    status=row['status'],
                    sanitize_method=row['sanitize_method'],
                    images=row['image'],
                    brand=Brand(uuid=row['brand_id']),
                    category=Category(uuid=row['category_id']),
                    sanitary_register=SanitaryRegistry(uuid=row['sanitary_register_id']),
                    iva=row['iva'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                )
            return None

    async def search(self, query: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            filters = self._parse_query(query)
            sql = '''
                SELECT DISTINCT p.uuid, p.generic_name, p.commercial_name, p.description, p.measurement,
                                p.formulation, p.composition, p.reference, p.use, p.status,
                                p.sanitize_method, p.image, p.created_at, p.updated_at,
                                b.uuid AS brand_uuid, b.name AS brand_name,
                                c.uuid AS category_uuid, c.name AS category_name,
                                sr.uuid AS sanitary_register_uuid, sr.number_registry
                FROM products p
                LEFT JOIN brands b ON p.brand_id = b.uuid
                LEFT JOIN categories c ON p.category_id = c.uuid
                LEFT JOIN sanitary_registry sr ON p.sanitary_register_id = sr.uuid
                LEFT JOIN brand_providers bp ON bp.brand_uuid = b.uuid
                LEFT JOIN providers pr ON bp.provider_uuid = pr.uuid
                LEFT JOIN characteristics ch ON ch.product_id = p.uuid
                WHERE p.deleted_at IS NULL
            '''

            conditions = []
            params = []

            # Filtros específicos
            if "brand" in filters:
                conditions.append(f"LOWER(b.name) LIKE ${len(params) + 1}")
                params.append(f"%{filters['brand'].lower()}%")
            if "category" in filters:
                conditions.append(f"LOWER(c.name) LIKE ${len(params) + 1}")
                params.append(f"%{filters['category'].lower()}%")
            if "sanitary_registry" in filters:
                conditions.append(f"LOWER(sr.number_registry) LIKE ${len(params) + 1}")
                params.append(f"%{filters['sanitary_registry'].lower()}%")
            if "provider" in filters:
                conditions.append(f"LOWER(pr.name) LIKE ${len(params) + 1}")
                params.append(f"%{filters['provider'].lower()}%")
            if "general" in filters:
                general_conditions = '''
                    LOWER(p.generic_name) LIKE ${index} OR
                    LOWER(p.commercial_name) LIKE ${index} OR
                    LOWER(p.description) LIKE ${index} OR
                    LOWER(p.measurement) LIKE ${index} OR
                    LOWER(p.formulation) LIKE ${index} OR
                    LOWER(p.composition) LIKE ${index} OR
                    LOWER(p.reference) LIKE ${index} OR
                    LOWER(p.use) LIKE ${index} OR
                    LOWER(p.status) LIKE ${index} OR
                    LOWER(p.sanitize_method) LIKE ${index} OR
                    LOWER(ch.characteristic) LIKE ${index} OR
                    LOWER(ch.description) LIKE ${index}
                '''
                general_conditions = general_conditions.replace("${index}", f"${len(params) + 1}")
                conditions.append(f"({general_conditions})")
                params.append(f"%{filters['general'].lower()}%")

            # Agregar condiciones al SQL
            if conditions:
                sql += " AND " + " AND ".join(conditions)

            # Ejecutar consulta
            rows = await connection.fetch(sql, *params)

            return [
                {
                    "uuid": str(row["uuid"]),
                    "generic_name": row["generic_name"],
                    "commercial_name": row["commercial_name"],
                    "description": row["description"],
                    "image": row["image"],
                    "brand": {"uuid": str(row["brand_uuid"]), "name": row["brand_name"]},
                    "category": {"uuid": str(row["category_uuid"]), "name": row["category_name"]},
                    "sanitary_registry": {"uuid": str(row["sanitary_register_uuid"]),
                                          "number_registry": row["number_registry"]}
                }
                for row in rows
            ]

    def _parse_query(self, query: str):
        filters = {}
        query = query.lower()

        # Identificar los filtros
        if "in: marca" in query:
            brand_value = query.split("in: marca")[1].split("in:")[0].strip().strip("'")
            filters["brand"] = brand_value
        if "in: categoría" in query:
            category_value = query.split("in: categoría")[1].split("in:")[0].strip().strip("'")
            filters["category"] = category_value
        if "in: registro sanitario" in query:
            sanitary_value = query.split("in: registro sanitario")[1].split("in:")[0].strip().strip("'")
            filters["sanitary_registry"] = sanitary_value
        if "in: proveedor" in query:
            provider_value = query.split("in: proveedor")[1].split("in:")[0].strip().strip("'")
            filters["provider"] = provider_value
        if "in: producto" in query:
            product_value = query.split("in: producto")[1].split("in:")[0].strip().strip("'")
            filters["general"] = product_value

        # Si no hay `in:` buscar en general
        if not filters:
            filters["general"] = query.strip()

        return filters
